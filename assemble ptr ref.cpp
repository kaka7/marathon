#include <iostream>
#include <stdio.h>
#include<memory>

using namespace std;

class Base
{
public:
    Base()
    {
        nBase = 1;
        printf("CBase");
    }
    ~Base()
    {
        printf("~CBase");
    }
    virtual void f()
    {
        printf("Base:f()");
    }
    virtual void g()
    {
        printf("Base:g()");
    }

private:
    int nBase;
};

class Derive : public Base
{
public:
    Derive()
    {
        nDerive = 2;
        printf("Derive");
    }
    ~Derive()
    {
        printf("~Derive");
    }
    virtual void g()
    {
        printf("Dervie:g()");
    }
    virtual void h()
    {
        printf("Dervie:h()");
    }

private:
    int nDerive;
};
int main()
{   
    // std::unique_ptr<int>
    Derive d;
    Base *b = &d;
    b->g();
    return 0;
}