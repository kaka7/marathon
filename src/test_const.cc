#include <iostream>
using namespace std;
int main(int argc, char const *argv[])
{
    int i =0;
    int i1=2;
    int * const p1=&i;
    // p1=&i1;//error:顶层const,不能改变指针本身

    const int c1=42;
    const int c2 =43;
    int c3=44;
    const int *p2=&c1;
    // *p2=43;//error:底层const,能改变指针,但不能改变指针的值
    p2=&c2;
    p2=&c3;
    const int & p3=c1;//底层const,拷贝构造函数
    return 0;
}
