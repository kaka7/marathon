
void longa()
{
    int i, j;
    for (i = 0; i < 1000000; i++)
        j = i; //am I silly or crazy? I feel boring and desperate.
}

void foo2()
{
    int i;
    for (i = 0; i < 10; i++)
        longa();
}

void foo1()
{
    int i;
    for (i = 0; i < 100; i++)
        longa();
}

int main(void)
{
    foo1();
    foo2();
}

/*
perf 如果程序出现非常麻烦的性能问题时，推荐使用 systemtap,iperf是网络
http://www.brendangregg.com/perf.html	wiki

blog 
https://www.ibm.com/developerworks/cn/linux/l-cn-perf1/ 
https://www.ibm.com/developerworks/cn/linux/l-cn-perf2/
https://zhuanlan.zhihu.com/p/21348220
https://dev.to/etcwilde/perf---perfect-profiling-of-cc-on-linux-of
https://perf.wiki.kernel.org/index.php/Tutorial#Source_level_analysis_with_perf_annotate

ubuntu安装perf(yum install perf) https://xiaoyanzhuo.github.io/2019/01/18/Perf-Tool.html
$sudo apt-get update
$sudo apt-get install linux-tools-common linux-tools-generic linux-tools-`uname -r`


#解决报错"Kernel address maps (/proc/{kallsyms,modules}) were restricted. Check /proc/sys/kernel/kptr_restrict before running 'perf record'".
$ sudo sh -c " echo 0 > /proc/sys/kernel/kptr_restrict"

划分为三类：
perf list
Hardware Event 是由 PMU 硬件产生的事件，比如 cache 命中，当您需要了解程序对硬件特性的使用情况时，便需要对这些事件进行采样；
Software Event 是内核软件产生的事件，比如进程切换，tick 数等 ;
Tracepoint event 是内核中的静态 tracepoint 所触发的事件，这些 tracepoint 用来判断程序运行期间内核的行为细节，比如 slab 分配器的分配次数等。

gcc -o t1 test_perf.c -g
perf stat ./t1 
perf top

perf record – e cpu-clock ./t1 
perf report

perf record [-g] ./t1 //生成.data -g调用图
perf report [-g] 生成图,可以进去卡汇编(enter,->)

perf annotate -d //反汇编

*/