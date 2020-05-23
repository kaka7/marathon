//#单例模式
/* 意图是保证一个类仅有一个实例，并提供一个访问它的全局访问点，该实例被所有程序模块共享。整个系统生命周期里，保证一个类只能产生一个实例，确保该类的唯一性。
定义一个单例类：
    私有化它的构造函数，以防止外界创建单例类的对象；
    使用类的私有静态指针变量指向类的唯一实例；private:	static Singleton* instance;
    使用一个公有的静态方法获取该实例。*/
// 什么是线程安全？
// 在拥有共享数据(单例对象)的多条线程并行执行的程序中，线程安全的代码会通过同步机制保证各个线程都可以正常且正确的执行，不会出现数据污染等意外情况。
//#也就是多个thread去写共享数据,也就是new单例(多个单例对象地址),导致不安全,所以加锁是在new时(所以饿汉式是安全的),简而言之多个线程可以写,但是同一时刻只能一个线程写
/*
//#懒汉版（Lazy Singleton）

教学版，即懒汉版（Lazy Singleton）：单例实例在第一次被使用时才进行初始化，这叫做延迟初始化。

// version 1.01
class Singleton
{
private:
	static Singleton* instance;
private:
	Singleton() {};
	~Singleton() {};
	Singleton(const Singleton&);
	Singleton& operator=(const Singleton&);
public:
	static Singleton* getInstance() 
        {
		if(instance == NULL) 
			instance = new Singleton();
		return instance;
	}
};

// init static member
Singleton* Singleton::instance = NULL;

问题1：Lazy Singleton存在内存泄露的问题，有两种解决方法：

使用智能指针使用静态的嵌套类对象


//#饿汉版（Eager Singleton）：指单例实例在程序运行时被立即执行初始化

// version 1.3
class Singleton
{
private:
	static Singleton instance;
private:
	Singleton();
	~Singleton();
	Singleton(const Singleton&);
	Singleton& operator=(const Singleton&);
public:
	static Singleton& getInstance() {
		return instance;
	}
}

// initialize defaultly
Singleton Singleton::instance;

由于在main函数之前初始化，所以没有线程安全的问题。但是潜在问题在于no-local static对象（函数外的static对象）
在不同编译单元中的初始化顺序是未定义的。也即，static Singleton instance;和static Singleton& getInstance()二者的初始化顺序不确定，
如果在初始化完成之前调用 getInstance() 方法会返回一个未定义的实例。

总结：
懒汉式是私有化类的静态指针对象
恶汉式是私有化类的静态对象,然后Singleton Singleton::instance;

    Eager Singleton 虽然是线程安全的，但存在潜在问题；
    Lazy Singleton通常需要加锁来保证线程安全，但局部静态变量版本在C++11后是线程安全的；局部静态变量版本（Meyers Singleton）最优雅。

    */

// #include <iostream>
// #include <mutex>
// #include <thread>

// using namespace std;
// mutex mu;//线程互斥对象
// class Singleton_Hungry
// {
// private:
// 	Singleton_Hungry()
// 	{
// 		cout << "我是饿汉式，在程序加载时，我就已经存在了。" << endl;
// 	}
// 	static Singleton_Hungry* singleton;
// public:
// 	static Singleton_Hungry* getInstace()
// 	{
// 		return singleton;
// 	}

// };
// //静态属性类外初始化
// Singleton_Hungry* Singleton_Hungry::singleton = new Singleton_Hungry;

// class Singleton_Lazy
// {
// private:
// 	Singleton_Lazy()
// 	{
// 		cout << "我是懒汉式,在别人需要我的时候，我才现身。"  << "我的实例内存地址是:" << this<< endl;
//         // std::cout << "我的实例内存地址是:" << this << std::endl;
// 	}
// 	static Singleton_Lazy* singleton;
// public:
// 	static Singleton_Lazy* getInstance()
// 	{

// 		if (NULL == singleton)
// 		{

// 			// mu.lock();//关闭锁
//             // std::lock_guard<std::mutex> lg(mu);
// 			if (NULL == singleton)
// 			{
// 				singleton = new Singleton_Lazy;
// 			}
// 			// mu.unlock();//打开锁
// 		}
// 		return singleton;
// 	}
// };
// Singleton_Lazy* Singleton_Lazy::singleton = NULL;
// void thread01()
// {
// 	for (int i = 0; i < 5; i++)
// 	{
// 		cout << "thread01 working...." << endl;
// 		Singleton_Lazy *lazy1 = Singleton_Lazy::getInstance();
// 		cout << "thread01创建单例lazy1地址:" << lazy1 << endl;
// 	}
// }
// void thread02()
// {
// 	for (int i = 0; i < 5; i++)
// 	{
// 		cout << "thread02 working...." << endl;
// 		Singleton_Lazy *lazy2 = Singleton_Lazy::getInstance();
// 		cout << "thread02创建单例lazy2地址:" << lazy2 << endl;
// 	}
// }

// int main(int argc, char *argv[])
// {
// 	thread thread1(thread01);
// 	thread thread2(thread01);
// 	thread1.detach();
// 	thread2.detach();
// 	for (int i = 0; i < 5; i++)
// 	{
// 		cout << "Main thread working..." << endl;
// 		Singleton_Lazy *main = Singleton_Lazy::getInstance();
// 		cout << "Main 创建单例lazy地址:" << main << endl;
// 	}
// 	return 0;
// }

//这里意思是主线程和两个子线程同时run,
#include <iostream>
using namespace std;
class Singleton
{
private:
	// static Singleton *local_instance;
	Singleton(int a)
	{
		cout << "构造1" << endl;
	};
	Singleton()
	{
		cout << "构造2" << endl;
	};
	~Singleton()
	{
		cout << "析构" << endl;
	}

public:
	static Singleton *getInstance()
	{
		int x = 0;
		// static Singleton locla_s;
		// return &locla_s;
		return getInstance(x);
	}
	static Singleton *getInstance(int a)
	{
		if (a != 0)
		{
			// 	return getInstance();
			// }
			static Singleton locla_s(a);
			return &locla_s;
		}
		static Singleton locla_s;
		return &locla_s;

	}
};

class Singleton1
{
private:
static int b;
	// static Singleton1 *local_instance;
	Singleton1(int a)
	{
		cout << "构造1" << endl;
	};
	Singleton1()
	{
		cout << "构造2" << endl;
		cout<< b <<endl;
	};
	~Singleton1()
	{
		cout << "析构" << endl;
	}

public:
	// static Singleton1 *getInstance()
	// {
	// 	int x = 0;
	// 	// static Singleton1 locla_s;
	// 	// return &locla_s;
	// 	return getInstance(x);
	// }
	static Singleton1 *getInstance(int a)
	{
		// if (a != 0)
		// {
		// 	// 	return getInstance();
		// 	// }
		// 	static Singleton1 locla_s(a);
		// 	return &locla_s;
		// }
		static Singleton1 locla_s;
		return &locla_s;

	}
};

void foo(){
			Singleton1 *s3 = Singleton1::getInstance(2);
		std::cout << "单例模式访问第二次后" << s3 << std::endl;
}
int Singleton1::b =0;

enum class Type{ A,B};
	int main()
	{
		// cout << "单例模式访问第一次前" << endl;
		Singleton1 *s = Singleton1::getInstance(2);
		std::cout << "单例模式访问第一次后" << s << std::endl;
		// cout << "单例模式访问第二次前" << endl;
		Singleton1 *s2 = Singleton1::getInstance(2);
		std::cout << "单例模式访问第二次后" << s2 << std::endl;
		foo();
		auto x=Type::A;
		std::cout<< x <<std::endl;
		return 0;
	}
