#pragma once
#include<list>
#include<thread>
#include<functional>
#include<memory>
#include <atomic>
#include "SyncQueue.hpp"

const int MaxTaskCount = 100;
class ThreadPool
{
public:
    using Task = std::function<void()>;
    ThreadPool(int numThreads = std::thread::hardware_concurrency()) : m_task_queue(MaxTaskCount)
    {   cout<<"线程池构造函数:硬件线程数:"<<numThreads;
        Start(numThreads);//#todo
    }

    ~ThreadPool(void)
    {
        //如果没有停止时则主动停止线程池
        Stop();
    }

    void Stop()
    {
        std::call_once(m_flag, [this]{StopThreadGroup(); }); //保证多线程情况下只调用一次StopThreadGroup
    }

    void AddTask(Task&&task)
    {
        m_task_queue.Put(std::forward<Task>(task));
    }

    void AddTask(const Task& task)
    {
        m_task_queue.Put(task);
    }
    void Start(int numThreads)
    {
        m_running = true;
        //创建线程组
        for (int i = 0; i <numThreads; ++i)
        {   
            cout<<"before start,m_threadgroup lens:"<<m_threadgroup.size()<<endl;
            m_threadgroup.push_back(std::make_shared<std::thread>(&ThreadPool::RunInThread, this));
            cout<<"after start,m_threadgroup lens:"<<m_threadgroup.size()<<endl;

        }
    } 

private:   

    void RunInThread()
    {   cout<<"start run in thread\n";
        while (m_running)
        {
            //取任务分别执行
            std::list<Task> list;
            m_task_queue.Take(list);//放到list中

            for (auto& task : list)
            {
                if (!m_running)
                    return;

                task();
            }
        }
    }

    void StopThreadGroup()
    {
        m_task_queue.Stop(); //让同步队列中的线程停止
        m_running = false; //置为false，让内部线程跳出循环并退出

        for (auto thread : m_threadgroup) //等待线程结束
        {
            if (thread)
                thread->join();
        }
        m_threadgroup.clear();
    }

    std::list<std::shared_ptr<std::thread>> m_threadgroup; //处理任务的线程组
    SyncQueue<Task> m_task_queue; //同步队列     
    atomic_bool m_running; //是否停止的标志
    std::once_flag m_flag;
};