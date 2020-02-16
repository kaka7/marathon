https://github.com/flame/how-to-optimize-gemm

MMult1.c //将最内层的循环循环包装成函数,可理解为内联,一般编译器时会自动内联,比较O3 优化后
MMult2.c //将4行做一个pack ,其实没有改变计算顺序,也没有利用cache,并非一次算四列　
MMult_1x4_3.c //还是4行一次计算,没有提高,同上,只是pack 循环
MMult_1x4_4.c //和3一样只是展开了,没有提高
MMult_1x4_5.c //利用A的缓存友好性,k越大越能体现
  for ( p=0; p<k; p++ ){  //相对4是for合并,使得A友好
    C( 0, 0 ) += A( 0, p ) * B( p, 0 );     
    C( 0, 1 ) += A( 0, p ) * B( p, 1 );     
    C( 0, 2 ) += A( 0, p ) * B( p, 2 );     
    C( 0, 3 ) += A( 0, p ) * B( p, 3 );   



Now we start seeing a performance benefit. The reason is that the four loops have been fused and therefore the four inner products are now being performed simultaneously. This has the following benefits:
    The index p needs only be updated once every eight floating point operations.
    Element A( 0, p ) needs only be brought in from memory once instead of four times. (This only becomes a benefit when the matrices no longer fit in the L2 cache.)
MMult_1x4_6.c //顺序读a，将常用的值A( 0, p ) 和累计中间结果都放到寄存器中, 在mnk比较小时比较好，大了就没用了 to reduce traffic between cache and registers.
MMult_1x4_7.c //B放到指针中　mnk小时管用　todo ｗｈｙ
MMult_1x4_8.c //将A的寄存器unrool 4 没有优化
MMult_1x4_9.c //not require the pointer to be updated. 自加变成间接寻址 compiler did this optimization automatically, and hence we see no performance improvement...There is a special machine instruction to then access the element at bp0_pntr+1 that does not require the pointer to be updated.As a result, the pointers that address the elements in the columns of B only need to be updated once every fourth iteration of the loop.

//There is considerable improvement for problem sizes that fit (at least partially) in the L2 cache.

compute a 4 x 4 block of C at a time in order to use vector instructions and vector registers effectively.  There are special instructions as part of the SSE3 instruction set that allow one to perform two 'multiply accumulate' operations (two multiplies and two adds) per clock cycle for a total of four floating point operations per clock cycle. To use these, one has to place data in 'vector registers'. There are sixteen of these, each of which can hold two double precision numbers. So, we can keep 32 double precision numbers in registers. We will use sixteen of these to hold elements of C, a 4 x 4 block.
MMult_4x4_3.c AddDot4x4, which performs sixteen inner products at a time,没有提高（因为实际是1*4 算了四次for）
MMult_4x4_4.c inline the sixteen separate inner products and fuse the loops into one, thereby computing the sixteen inner products simultaneously in one loop ,没有提高（因为实际是1*4 算了四次for）
MMult_4x4_5.c  类似MMult_1x4_5.c //利用A的缓存友好性,k越大越好

when the matrices becomes large, since the data is reused more after being brought into the registers. On the left is the comparison of 4x4_4 and 4x4_5. On the right the comparison of 1x4_5 (computing four elements of C at a time) and 4x4_5 (computing sixteen elements of C at a time).

MMult_4x4_6.c //4*4 A,C都用多个寄存器
MMult_4x4_7.c //B用指针 提高了
MMult_4x4_8.c //B用寄存器 提高了
//We now use registers to store the elements of the current row of B.
//(Notice that we did not do this for the case where we computed C four elements at a time.) The performance actually drops slightly. But this step enables further optimizations.
MMult_4x4_9.c //rearrange the computation so that two rows of 4x4 block of C are computed at a time. From 4x4_8 to 4x4_9 is a subtle change: instead of updating the rows of 4x4 block C a row at a time, we compute them two rows at a time. This sets us up for using vector operations, where we update pairs C( 0,j ) and C( 1,j ) (j =0,...,3) with vector operations.没有提高
MMult_4x4_10.c //x向量寄存器 SIMD/sse mnk小时好,提高了 use the vector registers and vector operations.

Blocking to maintain performance
MMult_4x4_11.c //What we noticed is that for all optimizations so far, performance degraded considerably,when the matrices involved were much bigger than could fit in the L2 cache. In this optimization,we create an extra level of blocking to overcome this. We now have a main routine that calls what is the inner kernel used by the GotoBLAS and BLIS,and then the AddDot4x4 routine is the micro-kernel used by BLIS.mnk大时好

Packing into contiguous memory
MMult_4x4_12.c  //We now pack to 4xk block of A before calling AddDot4x4. We see a performance drop. If one examines the inner kernel one notices that each 4xk block of A is packed repeatedly, once for every time the outer loop is executed.
MMult_4x4_13.c //This version saves the packed blocks of A so that after the first iteration of the outer loop of InnerKernel
//the saved version is used. The performance gain is noticeable! The only change from the last version is the addition of if ( j== 0 ):
MMult_4x4_14.c  pack the kx4 blocks of B. Notice that in this version, the panels are packed repeatedly, adversely affecting performance.没有提高
MMult_4x4_15.c //avoid repacking the kx4 blocks of B.     if ( first_time )

总结：
指针
寄存器
缓存友好性（空间和时间）
Sse
Block
Pack