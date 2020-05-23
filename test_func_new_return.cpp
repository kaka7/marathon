#include<iostream>
using namespace std;

const char * const helpFun()
{
    char * p =new char[3];
    p[0]='a';
    p[1]='b';
    p[2]='\0';
    return p;
}

int main()
{
    const char * p = helpFun();
    p++;
    cout<<p<<endl;
    delete p;
    return 0;
}
