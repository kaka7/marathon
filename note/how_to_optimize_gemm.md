* 传统计算逻辑优化：硬件相关
    循环展开和分支预测，内联，避免除法，常量替代,	多线程，gpu线程
* 高阶计算：
    滑窗卷积，FFT,GEMM(卷积通过3D->im2col->2D ,从而使用基于gemm的各种blas版本如openblas cublas,mkl加速计算，根据不同的backend极致优化),wragrand（乘法转加法cudnn）,Bottleneck ,depthwise/pointwise conv

* 数据读/写：
    如何取：寄存器，指针
		优化读取：对齐，连续，合并，少用，tile,reorder,局部性(gemm),缓存友好性(packed,reorder B/C),cache miss
		减少读取：定点化，减少存储
		压缩,裁剪：bottleneck,pointwise
* 生成的代码上:(后端)
    汇编(终极)
	  流水线重排
	  simd,sse,寄存器
[toc]
#how-to-optimize-gemm
##x86列主序
https://github.com/flame/how-to-optimize-gemm   
(j*lda)
分支预测可参考perf例子
elso https://www.leiphone.com/news/201704/Puevv3ZWxn0heoEv.html 
pack技巧参考https://blog.csdn.net/just_sort/article/details/108412760

* MMult1.c //将最内层的循环循环包装成函数,可理解为内联,==一般编译器时会自动内联,比较O3 优化后,内联的目的是避免函数的调用==()
* MMult2.c //将4行做一个pack ,其实没有改变计算顺序,也没有利用cache,并非一次算四列　因为是列主序(j),j+1就是跳一行,所以和原来是一样的
* MMult_1x4_3.c //还是4行一次计算,没有提高,同上,只是pack 循环
* MMult_1x4_4.c //和3一样只是展开了,没有提高
* MMult_1x4_5.c //利用A的缓存友好性,k越大越能体现,==A( 0, p ) needs only be brought in from memory once instead of four times,即时间友好性==
  for ( p=0; p<k; p++ ){  //相对4是for合并,使得A友好
    C( 0, 0 ) += A( 0, p ) * B( p, 0 );     
    C( 0, 1 ) += A( 0, p ) * B( p, 1 );     
    C( 0, 2 ) += A( 0, p ) * B( p, 2 );     
    C( 0, 3 ) += A( 0, p ) * B( p, 3 );   



  Now we start seeing a performance benefit. The reason is that the four loops have been fused and therefore the four inner products are now being performed simultaneously. This has the following benefits:
    The index p needs only be updated once every eight floating point operations.
    Element A( 0, p ) needs only be brought in from memory once instead of four times. (This only becomes a benefit when the matrices no longer fit in the L2 cache.)
* MMult_1x4_6.c //顺序读a，==将常用的值A( 0, p ) 和或累计中间结果都放到寄存器中==, 在mnk比较小时比较好，大了就没用了 to reduce traffic between cache and registers.
* MMult_1x4_7.c //==B放到指针中,每次只需要指针++(指针就是地址),而数组会有一个搜索的过程　mnk小时管用==
* MMult_1x4_8.c //将A的寄存器unrool 4 没有优化,==一般编译器有做SIMD==
* MMult_1x4_9.c //not require the pointer to be updated. ==自加变成间接寻址 compiler did this optimization automatically==, and hence we see no performance improvement...There is a special machine instruction to then access the element at bp0_pntr+1 that does not require the pointer to be updated.As a result, the pointers that address the elements in the columns of B only need to be updated once every fourth iteration of the loop.

  //There is considerable improvement for problem sizes that fit (at least partially) in the L2 cache.

  compute a 4 x 4 block of C at a time in order to use vector instructions and vector registers effectively.  There are special instructions as part of the SSE3 instruction set that allow one to perform two 'multiply accumulate' operations (two multiplies and two adds) per clock cycle for a total of four floating point operations per clock cycle. To use these, one has to place data in 'vector registers'. There are sixteen of these, each of which can hold two double precision numbers. So, we can keep 32 double precision numbers in registers. We will use sixteen of these to hold elements of C, a 4 x 4 block.
* MMult_4x4_3.c AddDot4x4, which performs sixteen inner products at a time,没有提高（因为实际是1*4 算了四次for）
* MMult_4x4_4.c inline the sixteen separate inner products and fuse the loops into one, thereby computing the sixteen inner products simultaneously in one loop ,没有提高（因为实际是1*4 算了四次for）
* MMult_4x4_5.c  类似MMult_1x4_5.c //利用A的缓存友好性,k越大越好

when the matrices becomes large, since the data is reused more after being brought into the registers. On the left is the comparison of 4x4_4 and 4x4_5. On the right the comparison of 1x4_5 (computing four elements of C at a time) and 4x4_5 (computing sixteen elements of C at a time).

* MMult_4x4_6.c //4*4 A,C都用多个寄存器
* MMult_4x4_7.c //B用指针 提高了
* MMult_4x4_8.c //B用寄存器 提高了
//We now use registers to store the elements of the current row of B.
//(Notice that we did not do this for the case where we computed C four elements at a time.) The performance actually drops slightly. But this step enables further optimizations.
* MMult_4x4_9.c //rearrange the computation so that two rows of 4x4 block of C are computed at a time. From 4x4_8 to 4x4_9 is a subtle change: instead of updating the rows of 4x4 block C a row at a time, we compute them two rows at a time. This sets us up for using vector operations, where we update pairs C( 0,j ) and C( 1,j ) (j =0,...,3) with vector operations.没有提高
* MMult_4x4_10.c //x向量寄存器 SIMD/sse mnk小时好,提高了 

Blocking to maintain performance
* MMult_4x4_11.c //What we noticed is that for all optimizations so far, performance degraded considerably,when the matrices involved were much bigger than could fit in the L2 cache. In this optimization,we create an extra level of blocking to overcome this. We now have a main routine that calls what is the inner kernel used by the GotoBLAS and BLIS,and then the AddDot4x4 routine is the micro-kernel used by BLIS.mnk大时好

Packing into contiguous memory ==避免重复packed==
* MMult_4x4_12.c  //We now pack to 4xk block of A before calling AddDot4x4. We see a performance drop. If one examines the inner kernel one notices that each 4xk block of A is packed repeatedly, once for every time the outer loop is executed.
* MMult_4x4_13.c //This version saves the packed blocks of A so that after the first iteration of the outer loop of InnerKernel
//the saved version is used. The performance gain is noticeable! The only change from the last version is the addition of if ( j== 0 ):
* MMult_4x4_14.c  pack the kx4 blocks of B. Notice that in this version, the panels are packed repeatedly, adversely affecting performance.没有提高
* MMult_4x4_15.c //avoid repacking the kx4 blocks of B.     if ( first_time )

###总结
==指针
寄存器,向量寄存器(Sse)+SIMD指令
缓存友好性（空间和时间),内存对齐,避免cache miss(cpu stall)
for的unroll(编译器一般会自己优化)
Block
Pack:一次计算四行四列==

arm64环境里，编译选项只要加了-O2就会使能编译器的SIMD化，不像armv7里要写-ftree-vectorize或-O3告诉编译器启用neon。简单的循环结构对编译器优化更有利

    避免乘法,比如位运算
    简化循环:simd
    内存对齐
    指令重排

    cache line 
    L1,L2,AB 矩阵小于 L2 cache 时，gemm只需要从 RAM 读取 AB 大小的内存，不需要做其他的读 RAM 操作；但是当 AB 大于 L2 cache 时，由于行主序的 B 或者列主序的 A 不是内存连续的，gemm 从 RAM 读取的内存数超过 AB 的大小。

https://github.com/flame/blislab

##==arm上==:可用于neon优化
https://github.com/tpoisonooo/how-to-optimize-gemm/blob/master/src/HowToOptimizeGemm 是基于arm
行主序
https://zhuanlan.zhihu.com/p/65436463
https://zhuanlan.zhihu.com/p/69700540
行主序:
先切M
再切K:因为 K 很大会降低 Cache 命中率
最后切N:

  c_reg = vld1q_f32(c_pntr);
  c_reg = vaddq_f32(c_reg, c_1p_sum);

#缓存影响
intel cpu 
http://igoro.com/archive/gallery-of-processor-cache-effects/
The examples are in C#
##Example 1: Memory accesses and performance
cache line=64bytes=16个int
```c#
  How much faster do you expect Loop 2 to run, compared Loop 1?
  int[] arr = new int[64 * 1024 * 1024];
  // Loop 1
  for (int i = 0; i < arr.Length; i++) arr[i] *= 3;
  // Loop 2
  for (int i = 0; i < arr.Length; i += 16) arr[i] *= 3;
```

##Example 2: Impact of cache lines

Let’s explore this example deeper. We will try other step values, not just 1 and 16:

for (int i = 0; i < arr.Length; i += K) arr[i] *= 3;

##Example 3: L1 and L2 cache sizes
32kB L1 data cache, a 32kB L1 instruction cache, and a 4MB L2 data cache. The L1 caches are per-core, and the L2 caches are shared between pairs of cores

##Example 4: Instruction-level parallelism
指令间不能有依赖
Now, let’s take a look at something different. Out of these two loops, which one would you expect to be faster?

int steps = 256 * 1024 * 1024;
int[] a = new int[2];

// Loop 1
for (int i=0; i<steps; i++) { a[0]++; a[0]++; }

// Loop 2
for (int i=0; i<steps; i++) { a[0]++; a[1]++; }

##Example 5: Cache associativity
Direct mapped cache,N-way set associative cache ,Fully associative cache
N-way set associative caches are the typical solution for processor caches, as they make a good trade off between implementation simplicity and good hit rate.

##Example 6: False cache line sharing
多核时L1缓存是每个处理器各自的,L2是共享的,所以当多个线程对同一个cache line 一个一个位置修改时,会导致每个线程都发生cache miss
When one processor modifies a value in its cache, other processors cannot use the old value anymore. That memory location will be invalidated in all of the caches. Furthermore, since caches operate on the granularity of cache lines and not individual bytes, the entire cache line will be invalidated in all caches!
To demonstrate this issue, consider this example:
```c#
  private static int[] s_counter = new int[1024];
  private void UpdateCounter(int position)
  {
      for (int j = 0; j < 100000000; j++)
      {
          s_counter[position] = s_counter[position] + 3;
      }
  }
```
On my quad-core machine, if I call UpdateCounter with parameters 0,1,2,3 from four different threads, it will take 4.3 seconds until all threads are done.
On the other hand, if I call UpdateCounter with parameters 16,32,48,64 the operation will be done in 0.28 seconds!

#TVM优化
##reduce cpu
分块:A,B分块,然后由于C要作为下一个的输入,并非缓存友好,所以提前定义C的layout
向量化:数据格式一样,,cache 友好
行重新排列
packed:A*B,让B转置后B就缓存友好
线程
cache miss


##scheduler
一个for split多个,或者多个合并为一个
多个for reorder
GPU并行
compute_inline:合并中间结果,减少中间存储
compute_at,多个for合并(原始的for非嵌套)

#c语言优化
参考word笔记
##一、引用传递　值传递　指针传递
##二、++i和i++引申出的效率问题
##三、循环引发的讨论1（循环内定义，还是循环外定义对象）
##四、循环引发的讨论2（避免过大的循环,是否可以合并）
##五、局部变量VS静态变量
##六、避免使用多重继承
##七、尽量少使用dynamic_cast
##八、减少除法运算的使用
##九、将小粒度函数声明为内联函数（inline）
##十、多用直接初始化(避免拷贝)

系统调用
程序通过系统调用和内核交互，耗时仍大约在(如read指令)200ns+
进程上下文切换
平均每次上下文切换耗时3.5us左右（进程级别）
软中断 
一次软中断CPU开销大约3.4us左右


TLB:translation lookaside buffer:改进虚拟地址到物理地址转换的速度

#arm
https://github.com/Ewenwan/MVision/blob/master/CNN/HighPerformanceComputing/ARM_NEON_CNN%E7%BC%96%E7%A8%8B.md
6 https://mxnet.incubator.apache.org/api/python/gluon/
(e.g. 45× slower than us for ResNet-152 on AMD) for un-
model_zoo.html
https://github.com/Ewenwan/MVision/blob/master/CNN/Deep_Compression/readme.md
https://github.com/Ewenwan/MVision/blob/master/CNN/Deep_Compression/quantization/int8/readme.md
https://github.com/Ewenwan/MVision/blob/master/CNN/HighPerformanceComputing/%E5%BF%AB%E9%80%9F%E7%9F%A9%E9%98%B5%E4%B9%98%E6%B3%95.md
https://github.com/Ewenwan/MVision/blob/master/CNN/HighPerformanceComputing/doc/NEON%E7%BC%96%E7%A8%8B-%E4%BC%98%E5%8C%96%E5%BF%83%E5%BE%97%E5%8F%8A%E5%86%85%E8%81%94%E6%B1%87%E7%BC%96%E4%BD%BF%E7%94%A8%E5%BF%83%E5%BE%97.pdf
https://github.com/Ewenwan/MVision/tree/master/CNN/HighPerformanceComputing/doc
https://github.com/Ewenwan/MVision/blob/master/CNN/HighPerformanceComputing/readme.md
https://github.com/Ewenwan/MVision/blob/master/CNN/HighPerformanceComputing/example/optimination/arm_neon_sse_introduction.cpp
https://github.com/Ewenwan/MVision/blob/master/CNN/HighPerformanceComputing/ARM_NEON_CNN%E7%BC%96%E7%A8%8B.md
最优的加速方法是 利用局部性原理 和 向量指令进行卷积操作. 速度达到了无任何优化的30倍! 并且已达到内存IO的极限.

仅使用局部性原理和4线程的做法达到了 13倍 的加速 , 已经达到了很高的加速比.

局部性原理,多线程,向量指令 都在卷积操作上达到了至少3倍的加速,组合的加速比受限于内存的IO速度.利用cache减少IO次数和使用向量指令提高IO速度是卷积操作性能优化最重要的策略.