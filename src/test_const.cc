#include <iostream>
using namespace std;
int main(int argc, char const *argv[])
{
    int a=3,aa=4;
    const int aaa=0;//值不能变
    const int *c=&a;//常量指针
    // *c=3;错误,不能通过c来改变对应的值
    c=&aa;//可以改变指针的地址

    int * const d=&a;//指针常量
    *d=4;//通过指针改变值
    // d=&aa; 错误,不能改变指针的地址

    const int * const ccc=&a;//指针和值都不能变

    // 区别,看const在*的位置来定
    return 0;
}
