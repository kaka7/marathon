#include <list>
#include <mutex>
#include <thread>
#include <condition_variable>
#include <iostream>
#include <list>
#include <thread>
#include <functional>
#include <memory>
#include <atomic>
#include "ThreadPool.hpp"
#include "SyncQueue.hpp"

using namespace std;
void testThdPool()
{
    ThreadPool pool;
    // pool.Start(2);
    
    thread thd1([&pool] {//lambda创建10个线程
        for (int i = 0; i < 2; i++)
        {
            auto thID = this_thread::get_id();
            auto func = [thID] { cout << "同步线程池1的线程ID:" << thID << endl; };
            pool.AddTask(func);
        }
    });


    // thread thd2([&pool] {
    //     for (int i = 0; i < 10; i++)
    //     {
    //         auto thID = this_thread::get_id();
    //         auto func = [thID] { cout << "同步线程池2的线程ID:" << thID << endl; };
    //         pool.AddTask(func);
    //     }
    // });

    this_thread::sleep_for(chrono::seconds(2));
    // getchar();
    pool.Stop();
    // getchar();
    cout<<"start join"<<endl;
    // thd1.join();
    // thd2.join();

}
int main(int argc, char const *argv[])
{
    testThdPool();
    return 0;
}
