#pragma once

#include "MessageFactory.hpp"
#include "Message.hpp"

class Message1 : public Message
{
public:

	Message1()
	{
		std::cout << "message1" << std::endl;
	}

	Message1(int a)
	{
		std::cout << "message1" << std::endl;
	}

	~Message1()
	{
	}

	void foo() override
	{
		std::cout << "message1" << std::endl;
	}
};
//5 派生类中调用宏实现自动注册
//REGISTER_MESSAGE(Message1, "message1", 2);
REGISTER_MESSAGE(Message1, "message1");
