#include <stdio.h>
int a(void)
{
    int i = 0, g = 0;
    while (i++ < 100000)
    {
        g += i;
    }
    return g;
}
int b(void)
{
    int i = 0, g = 0;
    while (i++ < 400000)
    {
        g += i;
    }
    return g;
}
int main(int argc, char **argv)
{
    int iterations;
    if (argc != 2)
    {
        printf("Usage %s <No of Iterations>\n", argv[0]);
        exit(-1);
    }
    else
        iterations = atoi(argv[1]);
    printf("No of iterations = %d\n", iterations);
    while (iterations--)
    {
        a();
        b();
    }
}
/*
宗旨:尽量优化软件中被频繁调用的部分
gprof:gprof 仅仅是通过以固定的周期对程序运行时间(time命令下的user时间) 进行采样测量来工作的。因此，当程序不运行时，就不会对程序进行采样测量,缺点是不能知道内核调用时间,优点是这意味着剖析不会受到系统中其他事件的影响（例如另外一个用户使用了大量的 CPU 时间）。
gprof 的最大缺陷：它只能分析应用程序在运行 过程中所消耗掉的用户时间。gprof对I/O瓶颈无能为力，耗时甚久的I/O操作很可能只占据极少的CPU时间。
通常来说，应用程序在运行时既要花费一些时间来运行用户代码，也要花费一些时间来运行 “系统代码”(sleep,printf,需要编译系统库加上-pg参数)，例如内核系统调用, sleep 函数实际上是执行了一次对内核空间的调用，从而将应用程序的执行挂起了，然后有效地暂停执行，并等待内核再次将其唤醒
库函数(包括动态/静态/系统)函数调用（例如 printf）在这个输出中都没有出现。
这是因为这些函数都是在 C 运行时库（libc.so）中的，（在本例中）它们都没有使用 -pg 进行编译，因此就没有对这个库中的函数收集剖析信息


调用次数、时间、以及函数调用图
使用GRPOF分为三个步骤

（1）编译时候打开编译开关，-pg

（2）运行程序（程序一定要正常运行完毕才会生成性能报告）

（3）运行性能测试工具来生成报告。
gcc  -pg test_gprof.c  -o test_gprof
./test_gprof 5000
gprof test_gprof gmon.out
还可以分别看 -b -p -q 
  %   cumulative   self              self     total
 time   seconds   seconds    calls  ms/call  ms/call  name
 80.24     63.85    63.85    50000     1.28     1.28  b
 20.26     79.97    16.12    50000     0.32     0.32  a
 百分比  多个函数累计 一个函数时间 次数 单个函数平均耗时

$ sudo apt-get install python graphviz
$ sudo pip install gprof2dot 
$ gprof -b ./hello gmon.out | gprof2dot > hello.dot
然后在windows上查看

ubuntu上
$ sudo apt-get install python graphviz
$ sudo pip install gprof2dot 
$ dot -Tpng hello.dot -o hello.png


系统调用sleep
 #include <stdio.h>
int a(void) {
  sleep(1);
  return 0;
}
int b(void) {
  sleep(4);
  return 0;
}
int main(int argc, char** argv)
{
   int iterations;
   if(argc != 2)
   {
      printf("Usage %s <No of Iterations>\n", argv[0]);
      exit(-1);
   }
   else
      iterations = atoi(argv[1]);
   printf("No of iterations = %d\n", iterations);
   while(iterations--)
   {
      a();
      b();
   }
}

No of iterations = 30
real    2m30.295s
user    0m0.000s 用户态没占用
sys     0m0.004s


*/

