git clone https://github.com/google/benchmark.git
cd benchmark
git clone https://github.com/google/googletest.git
mkdir build
cd build
cmake .. -DCMAKE_BUILD_TYPE=RELEASE
make
sudo make install


每一个benchmark测试用例都是一个类型为std::function<void(benchmark::State&)>的函数，其中benchmark::State&负责测试的运行及额外参数的传递。

随后我们使用for (auto _: state) {}来运行需要测试的内容，state会选择合适的次数来运行循环，时间的计算从循环内的语句开始，所以我们可以选择像例子中一样在for循环之外初始化测试环境
RangeMultiplier(10)->Range(10, 1000000)

#include <benchmark/benchmark.h>
#include <iostream>
#include <string>

using namespace std;

void demo()
{
    string str = "hello world";
    str.size();
}


static void BM_demo(benchmark::State& state) {
    for (auto _ : state)
        demo();
}
// Register the function as a benchmark
BENCHMARK(BM_demo); //用于注册测试函数
BENCHMARK_MAIN(); //程序入口

g++ -o demo demo.cpp -std=c++11  -lbenchmark -lpthread

#include <benchmark/benchmark.h>
#include <cstring>

static void BM_memcpy(benchmark::State& state) {
    char* src = new char[state.range(0)];
    char* dst = new char[state.range(0)];
    memset(src, 'x', state.range(0));
    for (auto _ : state)
        memcpy(dst, src, state.range(0));
    state.SetBytesProcessed(int64_t(state.iterations()) * int64_t(state.range(0)));
    delete[] src;
    delete[] dst;
}
BENCHMARK(BM_memcpy)->Arg(8)->Arg(64)->Arg(512)->Arg(1<<10)->Arg(8<<10);
BENCHMARK_MAIN(); 

#include <benchmark/benchmark.h>
#include <iostream>
#include <string>

using namespace std;

void demo()
{
    string str = "hello world";
    str.size();
}


static void BM_demo(benchmark::State& state) {
    for (auto _ : state)
        demo();
}
// Register the function as a benchmark
BENCHMARK(BM_demo)->Iterations(1000); //指定BM_demo函数中，for循环的迭代次数
BENCHMARK_MAIN(); //程序入口