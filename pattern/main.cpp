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
