#核心

    目的:找到scale因子对应的bin index
    方法:贪婪的(For i in range( 128 , 2048 ): 有些是4000
            reference_distribution_P[ i-1 ] += outliers_count),没有舍掉scale因子后面的,而是加到最后一个bin,
            candidate_distribution_Q 将i个binhebing到128,然后再expand(在一个num_per_bin内部的多个bin值用这个bin的均值代替)到i个
            从而找到使得Q去表征p的最合适的分布(KL最小,信息编码丢失最少),从而获得对应的scale因子
==tensorrt 和ncnn的int8 quantize_distribution获得方式貌似不同,trt是同一个num_per_bin内部累加(从ppt了解到),而ncnn是找到边界bin对应的值然后乘以left_scale/right_scale 个数,意思是认为一个bin左右的bin相差不大,具体效果有待进一步实验==
如果直方图左右非常不对称,可考虑:
    1:每一层不同bits 来量化
    2 训练的时候将激活值以及relu等加以限制

#tensorrt int8
tensorrt 

    Entropy Calibration - pseudocode

    Input: FP32 histogram H with 2048 bins: bin[ 0 ], ..., bin[ 2047 ]
    For i in range( 128 , 2048 )://#1
        reference_distribution_P = [ bin[ 0 ] , ..., bin[ i-1 ] ]// take first ‘ i ‘ bins from H #4
        outliers_count = sum( bin[ i ] , bin[ i+1 ] , ... , bin[ 2047 ] ) #5
        reference_distribution_P[ i-1 ] += outliers_count #6
        P /= sum(P) // normalize distribution P

        candidate_distribution_Q = quantize [ bin[ 0 ], ..., bin[ i-1 ] ] into 128 levels // explained later //#2
        expand candidate_distribution_Q to ‘ i ’ bins   // explained later //#3
        Q /= sum(Q)
        // normalize distribution Q
        divergence[ i ] = KL_divergence( reference_distribution_P, candidate_distribution_Q)
    End For
    Find index ‘m’ for which divergence[ m ] is minimal
    threshold = ( m + 0.5 ) * ( width of a bin )


#ncnn Int8
- 在每层计算时是需要先将feature map量化到INT8，然后将weights量化到INT8，最后卷积计算得到==INT32==的输出值，==输出值乘以scale（float）值反量化到float==，然后加上浮点格式的bias作为下一层的输入。
- NCNN的quantize.cpp函数里面有其量化的实现，所有的input，weights均是float32的，都通过此方法进行处理.
- 上位机校准程序得到的==scale参数乘以浮点值，给压缩到int8的范围内来，然后直接float2int转换，==最后做下边界处理，这样量化的前处理就处理好了。NCNN的dequantize.cpp==函数里面有其去量化的实现，把卷积最后输出的int32乘以scale值放大回原来的值变为float，然后加上浮点格式的bias，最后输出作为下一层的输入feature map。
Int8 类似高分辨率到低分辨率==



==饱和量化：==
==校验==:体现对激活值的量化
代码分析:通过获取reference_distribution_P, candidate_distribution_Q,来计算KL,从而得到最小的KL对应的threshold(即为第几个bin,实际上我们要得到这个bin对应的中间值),最终的threshold = ( m + 0.5 ) * ( width of a bin ),这里的#1,#2...对应tensorrt int8伪代码中的步骤
```c
int QuantizeData::threshold_distribution(const std::vector<float> &distribution, const int target_bin) 
        {
            //distribution 只是一半，在trt中是relu所以才0~2048 此时负半轴没有值 ，量化了也无关紧要

        threshold_begin=target_bin

        int target_threshold = target_bin;
        float min_kl_divergence = 1000;
        const int length = distribution.size();
        //#2
        std::vector<float> quantize_distribution(target_bin);//始终长度是128 
     
        float threshold_sum = 0;
        for (int threshold=target_bin; threshold<length; threshold++) 
        {
            threshold_sum += distribution[threshold];//一次性求饱和的sum,然后迭代时减去就行//#5
        }
        //#1
        for (int threshold=threshold_begin; threshold<length; threshold++) //开始迭代
        {
     
            std::vector<float> reference_distribution_P(distribution.begin(), distribution.begin()+threshold);//#4
            
            reference_distribution_P[threshold-1] += threshold_sum; //#6
            threshold_sum -= distribution[threshold];//#5
     
            // get quantize_distribution 循环(长度重128到2047)将distribution 压缩到128个bin
            fill(quantize_distribution.begin(), quantize_distribution.end(), 0);//填充0
            
            const float num_per_bin = static_cast<float>(threshold) / target_bin;//因为quantize_distribution始终是128个bin
            //#2
            for (int i=0; i<target_bin; i++) //目标是128bins,这一步会为每个bin赋值,但在每次num_per_bin不一定为整数,设计到上下边界取整问题,可取num_per_bin=1.2和1.8加深理解(1.5正好在一个bin中间不合适)
            {
                const float start = i * num_per_bin;
                const float end = start + num_per_bin;
                const int left_upper = ceil(start);//向上取整 大于x的最小整数
                if (left_upper > start) //每个group元素个数大于１
                {
                    const float left_scale = left_upper - start;
                    //原始quantize_distribution[i]=0
                    //128个bin的每个值是right_lower对应的索引乘以每个group 的bin个数
                    quantize_distribution[i] += left_scale * distribution[left_upper - 1];
                }
     
                const int right_lower = floor(end);
     
                if (right_lower < end) 
                {
     
                    const float right_scale = end - right_lower;
                    quantize_distribution[i] += right_scale * distribution[right_lower];
                }
                for (int j=left_upper; j<right_lower; j++) 
                {
                    quantize_distribution[i] += distribution[j];
                }
            }
     
            //#3 将quantize_distribution 扩展回threshold个bins
            std::vector<float> candidate_distribution_Q(threshold, 0);// threshold[128:2047]
     
            for (int i=0; i<target_bin; i++) 
            {
                const float start = i * num_per_bin;
                const float end = start + num_per_bin;
                float count = 0;
                const int left_upper = ceil(start);
                float left_scale = 0;
                if (left_upper > start) //同一个bin的左边界
                {
                    left_scale = left_upper - start;
                    if (distribution[left_upper - 1] != 0) 
                    {
                        count += left_scale;//只要非0的
                    }
                }
     
                const int right_lower = floor(end);
                float right_scale = 0;
                if (right_lower < end) //同一个bin的右边界
                {
                    right_scale = end - right_lower;
                    if (distribution[right_lower] != 0) 
                    {
                        count += right_scale;
                    }
                }
     
                for (int j=left_upper; j<right_lower; j++) 
                {
                    if (distribution[j] != 0) 
                    {
                        count++;
                    }
                }
     
                const float expand_value = quantize_distribution[i] / count;//#当前这个bin的均值填充到num_per_bin
     
                if (left_upper > start) 同一个group左边的值
                {
                    if (distribution[left_upper - 1] != 0) 
                    {
                        candidate_distribution_Q[left_upper - 1] += expand_value * left_scale;//left_scale为1就是原值
                    }
                }
                if (right_lower < end) 
                {
                    if (distribution[right_lower] != 0) 
                    {
                        candidate_distribution_Q[right_lower] += expand_value * right_scale;
                    }
                }
                for (int j=left_upper; j<right_lower; j++) //同一个group两头的，candidate_distribution_Q会大于128 #3
                {
                    if (distribution[j] != 0) 
                    {
                        candidate_distribution_Q[j] += expand_value;
                    }
                }
            }
     
            // kl
            float kl_divergence = compute_kl_divergence(reference_distribution_P, candidate_distribution_Q);
     
            // the best num of bin
            if (kl_divergence < min_kl_divergence) 
            {
                min_kl_divergence = kl_divergence;
                target_threshold = threshold;
            }
        }
     
        return target_threshold;
    }
```
 
==量化前==
```c
    for (int i=0; i<size; i++){
    outptr[i] = float2int8(ptr[i] * scale);}
    static inline signed char float2int8(float v){
    int int32 = round(v);
    if (int32 > 127) return 127;
    if (int32 < -128) return -128;
    return (signed char)int32;}
```  

     
ncnn其他技巧
==cpu.h 中可以设置 set_cpu_powersave(2) 减轻因为系统线程调度引起的耗时抖动
查看cpu占用
小模型推荐单线程，跑起来会比较稳定 …==
 
