#include "Message1.hpp"
#include "Message.hpp"

int main()
{
	Message* p = factory::produce("message1");
	p->foo();   //Message1
	delete p;
	
	auto p2 = factory::produce_unique("message1");
	p2->foo();
}

//参考 https://www.cnblogs.com/qicosmos/p/5090159.html
/*
实现动机:工厂方法是最简单地创建派生类对象的方法，也是很常用的，工厂方法内部使用switch-case根据不同的key去创建不同的派生类对象，
缺点:违反开闭原则:增加一个新class,就要增加switch语句
解决方案:自动注册的对象工厂
实现思路如下：
    1提供一个单例工厂对象。
    2工厂注册对象（保存创建对象的key和构造器）。
    3利用辅助类，在辅助类对象的构造过程中实现目标对象地注册。
    4利用一个宏来生成辅助对象。
    5在派生类文件中调用这个宏实现自动注册。

	需要注意:
	对象工厂并不直接保存对象，而是对象的构造器(通过宏来调用)，因为对象工厂不是对象池，是对象的生产者，允许不断地创建实例，这样做还实现了延迟创建。
	另外一个要注意的地方是借助宏来实现自动注册，本质上是通过宏来定义了很多全局的静态变量，而这些静态变量仅仅是为了实现自动注册，并没有实际的意义。

如果都是hpp的消息是没问题的，如果是h和cpp分开的那种，多个cpp包含含静态变量的头文件会引起的链接问题，这就把静态变量干掉，可以参考MessageFactory1.hpp or https://blog.csdn.net/mzlogin/article/details/13087479
工厂方法的伪代码。
Message* create(int type)
{
    switch (type) 
    {
    case MSG_PGSTATS:
        m = new MPGStats;
        break;
    case MSG_PGSTATSACK:
        m = new MPGStatsAck;
        break;
    case CEPH_MSG_STATFS:
        m = new MStatfs;
        break;
    case CEPH_MSG_STATFS_REPLY:
        m = new MStatfsReply;
        break;
    case MSG_GETPOOLSTATS:
        m = new MGetPoolStats;
        break;
    default:
        break;
    }
}
*/

