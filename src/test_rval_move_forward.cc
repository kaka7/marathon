#include <iostream>


using  namespace std;

// 返回类型后置:auto和decltype(编译时,仅希望得到类型而auto是得到类型的结果,->通过返回值推导的结果)
template<class Function,class... Args>
inline auto FuncWrapper(Function && f,Args && ... args)-> decltype(f(std::forward<Args>(args)...))
{
    return f(std::forward<Args>(args)...);
}
template<typename T>
void PrintT(T& t)
{
    cout<<"lvalue\n";
}

template<typename T>
void PrintT(T && t)
{
    cout<<"rval\n";
}
template<typename T>
void TestForward(T && v)
{
    PrintT(v);
    PrintT(std::forward<T>(v));
    PrintT(std::move(v));
}

int main(int argc, char const *argv[])
{
    TestForward(2);
    int x =3;
    TestForward(x);
    TestForward(std::forward<int>(x));
    return 0;
}


