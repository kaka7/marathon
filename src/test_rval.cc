#include <iostream>
using namespace std;

// 右值引用的两大用途：

//     移动语意 a=func();返回的结果通过"="操作符,首先清空a的内存,然后申请a的空间,赋值给a,最后销毁func()的中间结果
//     完美转发

/*
移动语意

移动语意(std::move)，可以将左值转化为右值引用

int a = 1; // 左值
int &b = a; // 左值引用

// 移动语意: 转换左值为右值引用
int &&c = std::move(a); 

void printInt(int& i) {
  cout << "lval ref: " << i << endl; 
}
void printInt(int&& i) {
  cout << "rval ref: " << i << endl; 
} 

int main() {
  int i = 1;
  
  // 调用 printInt(int&), i是左值
  printInt(i);
  
  // 调用 printInt(int&&), 6是右值
  printInt(6);
  
  // 调用 printInt(int&&)，移动语意
  printInt(std::move(i));   
}

由于编译器调用时无法区分

    printInt(int) 与 printInt(int&)printInt(int) 与 printInt(int&&)

如果再定义 printInt(int) 函数，会报错
*/

// 为啥要用移动语义?
class myVector
{
    int size;
    double *array;

public:
    // 拷贝构造函数
    myVector(const myVector &rhs)
    {
        std::cout << "Copy Construct\n";
        size = rhs.size;
        array = new double[size];
        for (int i = 0; i < size; i++)
        {
            array[i] = rhs.array[i];
        }
    }
    ~myVector(){cout<<"调用析构\n";}

    myVector(int n)
    { cout<<"调用默认构造函数\n";
        size = n;
        array = new double[n];
    }
    // 移动构造函数
    myVector(myVector &&rhs)
    {
        std::cout << "Move Constructor\n";
        size = rhs.size;
        array = rhs.array;
        rhs.size = 0;
        rhs.array = nullptr;
    }
// 有这个函数时
//     调用默认构造函数
// Move Constructor
// 调用析构
// Move Constructor
// 调用析构
// 调用析构
};
void foo(myVector&& v)
{
    /* Do something */
    //   cout<<"size:"<<v.size
    cout << "call foo\n";
}
// void foo(myVector &v)
// {
//     /* Do something */
//     //   cout<<"size:"<<v.size
//     cout << "call foo\n";
// }

// 假设有一个函数，返回值是一个 MyVector
myVector createMyVector()
{
    // myVector vec(2);
    return myVector(2);
};

int main()
{
    // Case 1:
    // myVector reusable = createMyVector(); //改成void foo(myVector& v)
//     调用默认构造函数
// Copy Construct
// 调用析构
// Copy Construct
// 调用析构
// 调用析构

// 调用两次的原因:一次是在函数中myVector(2),另一次是在main中赋值

    // // 这里会调用 myVector 的复制构造函数
    // // 如果我们不希望 foo 随意修改 reusable
    // // 这样做是 ok 的
    // foo(reusable);
    /* Do something with reusable */

    // Case 2:
    // createMyVector 会返回一个临时的右值
    // 传参过程中会调用拷贝构造函数
    // 多余地被复制一次
    // 虽然大部分情况下会被编译器优化掉
    foo(createMyVector());//使用 void foo(myVector&& v) 少一次调用构造函数
}
// g++ -std=c++11 src/test_rval.cc -fno-elide-constructors  -lpthread && time ./a.out 
//为啥要用完美转发

// void foo(myVector &v)
// {
//     /* Do something */
//     //   cout<<"size:"<<v.size
//     cout << "call foo\n";
// }
// template<typename T>
// void relay(T&& arg) {
//     foo(std::forward<T>(arg));
// }
// void foo(myVector& v) {}

// // 参数转发
// template<typename T>
// void relay(T arg) {
//     foo(arg);
// }

// int main() {
//   myVector reusable= reateMyVector();
  
//   // 拷贝构造函数
//   relay(reusable); 

//   // 移动构造函数
//   relay(createMyVector()); 
// }


