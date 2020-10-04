#include <iostream>
using namespace std;
//https://avdancedu.com/9683d88/

// template <typename T>
// class AutoPtr
// {
// public:
//     explicit AutoPtr(T *ptr = nullptr):owner_(true)//ptr_(ptr),
//     {
//         if (ptr)
//         {
//             cout << "new ptr" << endl;
//             ptr_ = ptr;
//         }
//     }
//     AutoPtr(AutoPtr<T> &auto_ptr):ptr_(auto_ptr.ptr_),owner_(false){}
//     ~AutoPtr()
//     {
//         if (owner_&& ptr_)//owner_=true 并且ptr不等于nullptr才能delete
//         {
//             cout << "rel delete ptr" << endl;
//             delete ptr_;
//             // return 0;
//         }
//         else{
//                         cout << "delete ptr" << endl;

//         }
//     }
//     T *operator->()//智能指针的运算符
//     {
//         return this->ptr_; //this class实例化后的对象指针
//     }
//     T &operator*()//智能指针的运算符
//     {
//         return *(this->ptr_);
//     }
//     //拷贝构造函数
//     AutoPtr &operator=(AutoPtr<T> &auto_ptr)//多个指针指向同一个对象
//     {
//         if (this != &auto_ptr)
//         {
//             if (ptr_)
//                 delete ptr_;
//             this->ptr_ = auto_ptr->ptr_;
//             owner_ = false;
//         }
//         return *this;
//     }

// private:
//     T *ptr_;
//     bool owner_;
// };

// 后创建的智能指针更应该是owner
template <typename T>
class AutoPtr
{
public:
    explicit AutoPtr(T *ptr = nullptr) : owner_(true) //ptr_(ptr),
    {
        if (ptr)
        {
            cout << "new ptr" << endl;
            ptr_ = ptr;
        }
    }
    // AutoPtr(AutoPtr<T> &auto_ptr) : ptr_(auto_ptr.ptr_), owner_(false) {}
    AutoPtr(AutoPtr<T> &auto_ptr) : ptr_(auto_ptr.ptr_), owner_(true) { auto_ptr.owner_ = false; }

    ~AutoPtr()
    {
        if (owner_ && ptr_) //owner_=true 并且ptr不等于nullptr才能delete
        {
            cout << "rel delete ptr" << endl;
            delete ptr_;
            // return 0;
        }
        else
        {
            cout << "delete ptr" << endl;
        }
    }
    T *operator->() //智能指针的运算符
    {
        return this->ptr_; //this class实例化后的对象指针
    }
    T &operator*() //智能指针的运算符
    {
        return *(this->ptr_);
    }
    //拷贝构造函数
    AutoPtr &operator=(AutoPtr<T> &auto_ptr) //多个指针指向同一个对象
    {
        if (this != &auto_ptr)
        {
            if (ptr_)
                delete ptr_;
            this->ptr_ = auto_ptr->ptr_;
            // owner_ = false;
            owner_ = true;
            auto_ptr->owner_ = false;
        }
        return *this;
    }
    T *get()
    {
        if(owner_&& this->ptr_!=nullptr){
        return this->ptr_;}
        else return nullptr;

        // return this->ptr_;
    }

private:
    T *ptr_;
    bool owner_;
};

class Myclass
{
public:
    Myclass()
    {
        cout << "new myclass" << endl;
    }
    ~Myclass()
    {
        cout << "delete myclass" << endl;
    }
    void hello()
    {
        cout << "hello" << endl;
    }
};

// 堆空间分配+析构函数自动释放解决栈内存溢出
// delete ptr      rel delete ptr
// rel delete ptr  delete myclass
// delete myclass  delete ptr
//析构顺序为newmy(AutoPtr在外部,所以先于newmy释放),my

// 既然auto_ptr的所有问题都是因为传递性引起的，所以阻止其传递性就可以解决这个问题了。
// 因此scoped_ptr的实现也特别简单，它将其拷贝构造函数及赋值操作符全部隐藏起来，这样就不会有auto_ptr的问题了。


template<typename T>
class ScopedPtr {
    public:
        ScopedPtr(T * ptr = nullptr): _ptr(ptr){
        }

        T* operator->(){
            return this->_ptr;
        }

        T& operator*(){
            return *(this->_ptr);
        }

        T* get(){
            return this->_ptr;
        }

        ~ScopedPtr(){
            if(_ptr != nullptr){
                delete _ptr;
            }
        }
    protected:
        ScopedPtr(ScopedPtr<T> & scopedptr){}                     //ScopedPtr<int> myPtr(new int(100)); 
        ScopedPtr<T> & operator=(ScopedPtr<T> & scopedptr){}      //ScopedPtr<int> newPtr = myPtr; 
        //error: calling a protected constructor of class 'ScopedPtr<int>'  ScopedPtr<int> newPtr = myPtr;  

    private:
        T *_ptr;
};



// unique_ptr可以对右值进行转移，说明白了就是提供了一种特殊方法可以将unique_ptr赋值给另一个unique_ptr，被转移后的unique_ptr也就不能再处理之前管理的指针了。
// 我们还是来看一个具体的例子你就清楚了，只要给我们之前的ScopedPtr加上一个移动构造函数(传入&&)和移动赋值运算符就实现unique_ptrr的转移功能了。
/*C++11标准中的unique_ptr的实现，这样一分析下来也是蛮简单的对吧
class ScopedPtr{
    ...
    ScopedPtr(ScopedPtr<T>&& scopedptr) noexcept : _ptr(scopedptr._ptr){
        std::cout << "move construct..." << std::endl;
        scopedptr._ptr =  nullptr;
    }

    ScopedPtr& operator=(ScopedPtr<T> && scopedptr) noexcept {
        std::cout << "move assignment..." << std::endl;
        if(this != &scopedptr){
            _ptr = scopedptr._ptr;
           scopedptr._ptr = nullptr;
        }
        return *this;
    }
};

int main(int argc, char * argv[]){
    ScopedPtr<int> myPtr(new int(100));
    //ScopedPtr<int> newPtr = myPtr;            //拷贝构造函数已经不能用了
    ScopedPtr<int> newPtr = std::move(myPtr);   //可以使用移动拷贝构造函数进行转移
}
*/

/* shared_ptr
基本原理是当有多个智能指针指对同一块堆空间进行管理时，每增加一个智能指针引用计数就增1，每减少一个智能指针引用计数就减少。当引用计数减为0时，就将管理的堆空间释放掉。

我们还是看一个具体例子吧，其实现是在unique_ptr的基础之上实现的，代码如下：

class ScopedPtr {

    public:
        ...
        ScopedPtr(T *ptr = nullptr): _ptr(ptr), _ref_count(new int(1)){
        }

        ScopedPtr(ScopedPtr<T> & scopedptr): _ptr(scopedptr._ptr), _ref_count(scopedptr._ref_count){
            ++（*_ref_count);
        }

        ScopedPtr & operator=(ScopedPtr<T> & scopedptr){
            if(this != &scopedptr){
                _release();
                _ptr(scopedptr._ptr);
                _ref_conut(scopedptr._ptr);
                ++(*_ref_count);
            }

            return *this;
        }

        ~ScopedPtr(){
            _release();
        }

        int* getCount(){
            return *_ref_count; 
        }
    protected:
        void _release() {
            std::cout << "deconstruct...: count=" << ((*_ref_count) -1)  << std::endl;
            if(--(*_ref_count) == 0){
                delete _ptr;
                delete _ref_count;
            }
        }

    private:
        ...
        int *_ref_count;   //引用计数
};

int main(int argc, char *argv[]){
    ScopedPtr<int> myPtr(new int(100));
    ScopedPtr<int> pT2 = myPtr;
}
*/


/*
weak_ptr
weak_ptr就是专门为了解决这个问题而出现的。实际上weak_ptr不能单独称为一个智能指针，它必须与shared_ptr一起使用，起到辅助share_ptr的作用。我们来看看它是如何解决上述问题的吧。
首先引入weak_ptr后，weak_ptr也要有自己的引用计数，因此我们需要修改之前的ScopedPtr，将它的计数成员变成一个类型，包括它自己的计数和weak_ptr的计数，
*/
int main(int argc, char const *argv[])
{
    //1智能指针原理:自动释放内存
    AutoPtr<Myclass> my(new Myclass());
    my->hello();
    (*my).hello();
    AutoPtr<Myclass> newmy = my;

//2 共享所有权:通过owner
    AutoPtr<int> oldPtr(new int(100));
    {
        AutoPtr<int> newPtr(oldPtr);
    }
    //2.1共享所有权失败
    //newPtr处理中括号后生命周期结束，堆空间也被回收了 这里出现了野指针
    // *(oldPtr.get()) = -100;//Segmentation fault,所以get时通过owner_=true判断是否返回空还是有效地址
    // std::cout << "the value is " << *(oldPtr.get()) << std::endl;
    // 3不共享所有权,不要owner 直接ptr_=autoptr.ptr_;autoptr.ptr=nullptr

    return 0;
}
