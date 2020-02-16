#ncnn Int8
- 在每层计算时是需要先将feature map量化到INT8，然后将weights量化到INT8，最后卷积计算得到==INT32==的输出值，==输出值乘以scale（float）值反量化到float==，然后加上浮点格式的bias作为下一层的输入。
- NCNN的quantize.cpp函数里面有其量化的实现，所有的input，weights均是float32的，都通过此方法进行处理.
- 上位机校准程序得到的==scale参数乘以浮点值，给压缩到int8的范围内来，然后直接float2int转换，==最后做下边界处理，这样量化的前处理就处理好了。NCNN的dequantize.cpp==函数里面有其去量化的实现，把卷积最后输出的int32乘以scale值放大回原来的值变为float，然后加上浮点格式的bias，最后输出作为下一层的输入feature map。
Int8 类似高分辨率到低分辨率==

==饱和量化：==
==校验==
```c
        int QuantizeData::threshold_distribution(const std::vector<float> &distribution, const int target_bin) 
        {//distribution 只是一半，在trt中是relu所以才0~2048 此时负半轴没有值 ，量化了也无关紧要

        int target_threshold = target_bin;
        float min_kl_divergence = 1000;
        const int length = distribution.size();
     
        std::vector<float> quantize_distribution(target_bin);
     
        float threshold_sum = 0;
        for (int threshold=target_bin; threshold<length; threshold++) 
        {
            threshold_sum += distribution[threshold];//一次性求饱和的sum,然后迭代时减去就行
        }
     
        for (int threshold=target_bin; threshold<length; threshold++) //开始迭代
        {
     
            std::vector<float> t_distribution(distribution.begin(), distribution.begin()+threshold);
            
            t_distribution[threshold-1] += threshold_sum; 
            threshold_sum -= distribution[threshold];
     
            // get P
            fill(quantize_distribution.begin(), quantize_distribution.end(), 0);//填充0
            
            const float num_per_bin = static_cast<float>(threshold) / target_bin;
     
            for (int i=0; i<target_bin; i++) //目标是128bins
            {
                const float start = i * num_per_bin;
                const float end = start + num_per_bin;
                const int left_upper = ceil(start);//向上取整
                if (left_upper > start) //每个group元素格式大于１
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
     
            // get Q
            std::vector<float> expand_distribution(threshold, 0);// threshold[128:2047]
     
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
     
                const float expand_value = quantize_distribution[i] / count;
     
                if (left_upper > start) 同一个group左边的值
                {
                    if (distribution[left_upper - 1] != 0) 
                    {
                        expand_distribution[left_upper - 1] += expand_value * left_scale;//left_scale为1就是原值
                    }
                }
                if (right_lower < end) 
                {
                    if (distribution[right_lower] != 0) 
                    {
                        expand_distribution[right_lower] += expand_value * right_scale;
                    }
                }
                for (int j=left_upper; j<right_lower; j++) //同一个group两头的，expand_distribution会大于128
                {
                    if (distribution[j] != 0) 
                    {
                        expand_distribution[j] += expand_value;
                    }
                }
            }
     
            // kl
            float kl_divergence = compute_kl_divergence(t_distribution, expand_distribution);
     
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
  
 
其他技巧
==cpu.h 中可以设置 set_cpu_powersave(2) 减轻因为系统线程调度引起的耗时抖动
查看cpu占用
小模型推荐单线程，跑起来会比较稳定 …==
 
