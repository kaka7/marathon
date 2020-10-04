#include <thread>
#include <iostream>
#include <vector>

using namespace std;

// void FunTest();
// class Test //完整定义放在前面
// {
// public:
//    Test(){cout<<"constructor func\n";}
// };
// class Test;//只声明不定义
// int main()
// {
//     // Test test; //需要类的完整定义,
//     Test* ptest; //使用指针，可以只用class Test 不会调用构造函数
//     // 如果类中只有申明类而没有定义，则只能定义指针：Test *test；如果不定义类而仅仅声明类的话，当使用Test test时，
//     // 编译器只知道Test是个class，但留多大空间？怎么初始化？都不知道，因此，在实例化一个对象之前，一定要看到类实体的声明，
//     // 否则是无法构造一个真正的对象的。
// }

//线程池 std::async(允许复用) ,std::thread 开销包括直接开销(初始化开销),间接开销(内存的增加导致缓存抖动),调度开销


//#线程使用
void FunTest()
{
}

void func1(){
    cout<<"exe func!\n";
}
    void func(int x){
        cout<<"x:"<<x<<endl;
    }

class Test{
    public:
    Test(){cout<<"call 构造函数\n";};//main中定义class一定要写完整{}符号
    Test(const Test &){//如果在线程中传参,只能在拷贝构造函数中初始化列表TA(const TA& ta) :m_i(ta.m_i)
        cout<<"call拷贝构造函数\n";
    }
    ~Test(){cout<<"call 析构函数\n";};
    void operator()(){//1使用类来进行创建： 一定要重载()操作符，使得他变成一个可调用对象,然后就可以传给线程了;2构造时也会执行该操作,
        cout<<"callable obj\n";
        // void operator()(std::string& msg) 用的时候std::thread t1(Fctor(), std::ref(s));
    }
    void Set(int & v){
        var=v;
    }
    private:
    int var;
};

class Test;

int main(int argc, char const *argv[])
{
    /* code */
    // thread t(func1);
    // t.join();
    // Test* ptest= new Test();
    // cout<<"创建指针对象完毕\n";
    // delete ptest;//todo 用vargrand 查看栈内存泄露,不是在堆上???

    Test test;
    cout<< "obj创建完毕:";
    // thread c_t(Test);
    thread c_t(test);//对象实际被赋值到了线程中去了
    // thread ttest(std::ref(test));就只用调用一次构造和一次析构

    cout<< "线程启动完毕:\n";
    c_t.join();
    // c_t.detach();
    cout<< "线程执行完毕:\n"<<endl;//为啥会调用四次次析构,两次拷贝构造TODO operator导致的???


}
//     //#多线程串行

//     vector<thread> vthread;
//     for (auto i=0;i<10;++i){
//         // vthread.emplace_back(thread(func1));
//                 vthread.push_back(thread(func,i));//func不能传i的引用??? todo 线程只传栈地址?

//     }
//     for (auto iter=vthread.begin();iter!=vthread.end();++iter){
//         iter->join();
//     }
//     // for (auto i=0;i<10;++i){
//     //     vthread[i].join;
//     // }

//     // std::thread t2 = std::move(t1);
//     // std::cout << t2.get_id() << std::endl;//输出线程id

//     return 0;
// }

// //#共享数据问题

// #include <thread>
// #include <iostream>
// #include <mutex>
// mutex mt;

// int counter = 0;

// void add()
// {   mt.lock();
//     for (int i = 0; i < 1000000; i++)
//     {
//         counter = counter + 1;
//     }
//     mt.unlock();
// }

// void sub()
// {mt.lock();
//     for (int i = 0; i < 1000000; i++)
//     {
//         counter = counter - 1;
//     }
//     mt.unlock();
// }

// int main()
// {
//     std::thread t1(add);
//     std::thread t2(sub);

//     t1.join();
//     t2.join();

//     std::cout << "counter:\t" << counter << std::endl;
// }




// #include <queue>
// #include <list>
// #include <mutex>

// class Test
// {
// public:
//     list<int> CMDqueue;

//     void RecMSGProcess()
//     {
//         for (auto i = 0; i < 10; ++i)
//         {
//             mt.lock();
//             // std::lock_guard<std::mutex> sbguard(mt);

//             cout <<"thread:"<< std::this_thread::get_id()<< ":rec:" << i << endl;
//             CMDqueue.emplace_back(i);
//             mt.unlock();
//         }
//     }
//     void ExeMSGProcess()
//     {periods
//         for (auto i = 0; i < 10; ++i)
//         {
//             mt.lock();
//             // std::lock_guard<std::mutex> sbguard(mt);

//             cout << "run Exe for" << endl;
//             if (!CMDqueue.empty())
//             {
//                 cout <<"thread:"<< std::this_thread::get_id()<< ":Exe:" << CMDqueue.front() << endl;
//                 CMDqueue.pop_front();
//             }
//             mt.unlock();
//         }
//     }

// private:
//     mutex mt;
// };
// int main(int argc, char const *argv[])
// {
//     /* code */
//     Test test;
//     thread ttestrec(&Test::RecMSGProcess, &test); //一定要是对象的引用
//     thread ttestexe(&Test::ExeMSGProcess, &test);
//     //#两个线程是独立的,重要的事情说三遍
//     ttestrec.join();
//     ttestexe.join(); //for循环肯定要执行,但是队列可能为空,join并加锁时 会按照顺序执行完毕后再队列长度为0,都不加锁则长度值随机;如果只加其中还一个锁,可能另一个先执行,所以则长度也未知,但是不会出现段错误???
//     // ttestrec.detach();
//     // ttestexe.detach(); //输出count可能先于子线程执行,所以结果任意;detach并都加锁时(或部分加锁时),可能段错误;都不加锁时不会段错误,所以共享数据时不要用detach
//     cout << "queue size:" << test.CMDqueue.size() << endl;

//     return 0;
// }

// #include <chrono>
// #include <future>
// #include <iostream>
// #include <thread>

// double function(const double var) {
//     std::this_thread::sleep_for(std::chrono::milliseconds(1000));
//     return var;
// }
// // using namespace std;

//#生产者和消费者 - Condition variable 

// #include <atomic>
// #include <chrono>
// #include <condition_variable>
// #include <iostream>
// #include <queue>
// #include <random>
// #include <thread>
// #include <mutex>
// #include <memory>

// class BackEnd
// {
// public:
//     BackEnd() : thread_ptr_(new std::thread(&BackEnd::Process, this))
//     {
//         // thread_ptr_ = std::make_shared<std::thread>(&BackEnd::Process, this);
//     }

//     void AddData(const int data)
//     {
//         {
//             std::lock_guard<std::mutex> lg(data_queue_mutex_);
//             data_queue_.push(data);
//         }
//         data_queue_cond_var_.notify_one();//随机唤醒一个等待的线程 类似join,wait会等待这个触发
//     }

//     void Process()
//     {
//         thread_running_.store(true);//原子布尔型 不怕被改
//         while (thread_running_.load())
//         {
//             int data;
//             {
//                 // Wait for data.
//                 std::unique_lock<std::mutex> ul(data_queue_mutex_);
//                 data_queue_cond_var_.wait(ul, [this] { return !data_queue_.empty(); });//predict为false才触发
//                 data = data_queue_.front();
//                 data_queue_.pop();
//             } // Release lock.

//             // Process data.
//             std::cout << "[BackEnd]: Recive data: " << data << std::endl
//                       << std::endl;
//         }
//     }

// private:
//     std::atomic<bool> thread_running_;

//     std::mutex data_queue_mutex_;
//     std::queue<int> data_queue_;
//     std::condition_variable data_queue_cond_var_;

//     std::unique_ptr<std::thread> thread_ptr_;
// };

// int main(int argc, char **argv)
// {
//     // Start the back-end thread.
//     BackEnd back_end;

//     // This is the front-end.
//     std::default_random_engine generator;
//     std::uniform_int_distribution<int> distribution(0, 1000);
//     for (size_t i = 0; i < 10; ++i)
//     {
//         // Produce data.
//         int random_var = distribution(generator);

//         // Send data to the back-end.
//         back_end.AddData(random_var);

//         std::cout << "[FrontEnd]: Add var " << random_var << std::endl;
//         std::this_thread::sleep_for(std::chrono::milliseconds(500));
//     }

//     return 1;
// }

//#异步并行任务

// int main(int argc, char** agrv) {
//     std::cout<<"任务独立"<<std::endl;
//     // 我们可以使用async启动一个线程，使用future，在未来获取线程返回的结果
//     // Compute f1 + f2 + f3 + f4 using one thread.
//     std::chrono::steady_clock::time_point t1 = std::chrono::steady_clock::now();

//     double result = function(1.) + function(2.) + function(3.) + function(4.);

//     std::chrono::steady_clock::time_point t2 = std::chrono::steady_clock::now();
//     double time_cost = std::chrono::duration_cast<std::chrono::duration<double>>(t2 - t1).count() * 1000.;
//     std::cout << std::fixed << "Sigal thread result: " << result << " and time cost: " << time_cost << std::endl;

//     // Compute f1 + f2 + f3 + f4 using four threads.
//     t1 = std::chrono::steady_clock::now();

//     std::future<double> f1(std::async(std::launch::async, function, 1.));
//     auto f2 = std::async(std::launch::async, function, 2.);
//     auto f3 = std::async(std::launch::async, function, 3.);
//     result = function(4.) + f1.get() + f2.get() + f3.get();

//     t2 = std::chrono::steady_clock::now();
//     time_cost = std::chrono::duration_cast<std::chrono::duration<double>>(t2 - t1).count() * 1000.;
//     std::cout << std::fixed << "Multi-threads result: " << result << " and time cost: " << time_cost << std::endl;

//     return 1;
// }
// // g++ -std=c++11 src/test_threads.cc -lpthread


//#线程池 将线程放到vector中 消息放到queue中
// 在大多数系统中，将每个任务指定给某个线程时不切实际的，不过可以利用现有的并发性，进行并发执行。线程池就提供了这样的功能，提交到线程池中的任务并发执行，
// 提到的任务将会挂在任务队列上。队列中的每个任务都会被池中的工作线程获取，当一个任务执行完成后，到队列中获取下一个任务执行

#include <atomic>
#include <condition_variable>
#include <functional>
#include <iostream>
#include <mutex>
#include <queue>
#include <thread>
#include <vector>

class ThreadPool {
public:
    ThreadPool(const int thread_num) {
        threads_.reserve(thread_num);
        for (size_t i = 0; i < thread_num; ++i) {
            threads_.emplace_back(&ThreadPool::Thread, this);
        }
    }

    ~ThreadPool() {
        // Stop all threads in the pool.
        done_.store(true);
        thread_cond_var_.notify_all();
        for (size_t i = 0; i < threads_.size(); ++i) {
            threads_.at(i).join();//join完毕后就结束了
        } 

        std::cout << "[Threads stoped]\n";
    }

    void Submit(const std::function<void()>& work) {
        {
            // Add work to the queue.
            std::lock_guard<std::mutex> lg(mutex_);
            works_.push(work);
        }

        // Tell all threads to work. 
        thread_cond_var_.notify_all();
    }

private:
    void Thread() {
        done_.store(false);
        while (true) {
            // Wait for work.
            std::function<void()> work;
            {
                std::unique_lock<std::mutex> ul(mutex_);
                thread_cond_var_.wait(ul, [this] { return !works_.empty() || done_.load(); });
                if (done_.load()) {//析构函数调用
                    break;
                }

                work = works_.front();
                works_.pop();
            }           

            // Do work.git
            work();
        }
    }

    std::atomic_bool done_;//不用担心被数据安全问题
    std::mutex mutex_;
    std::condition_variable thread_cond_var_;
    std::queue<std::function<void()>> works_;
    std::vector<std::thread> threads_;
};

class Task {
public:
    
    void PrintText(const std::string& text) {
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
        
        {
            std::lock_guard<std::mutex> lg(mutex_);
            std::cout << "Thread " << std::this_thread::get_id() << " do task " << text << std::endl;
        }
    }

    std::mutex mutex_;
};

int main (int argc, char** argv) {
    ThreadPool thread_pool(2);

    Task task;
    for (size_t i = 0; i < 10; ++i) {
        thread_pool.Submit(std::bind(&Task::PrintText, &task, std::to_string(i)));
        std::cout << "Submit task: " << i << std::endl;
    }

    std::this_thread::sleep_for(std::chrono::seconds(5));
    return 1;
}
