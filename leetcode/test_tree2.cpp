//
// Created by naruto on 11/25/19.
//
// BinaryTree.cpp : 定义控制台应用程序的入口点。
//C++实现链式二叉树，在二叉树中找出和为某一值的所有路径
//#include "stdafx.h"
#include<iostream>
#include<string>
#include <stack>
using namespace std;
static int sum(0);
static int count(0);

template<class T>
struct BiNode
    {
    T data;
    struct BiNode<T> *rchild,*lchild;
    };

template<class T>
class BiTree
    {
public:
    BiTree(){
        cout<<"请输入根节点:"<<endl;
        Create(root);
        if (NULL != root)
            {
            cout<<"root="<<root->data<<endl;
            }
        else
            {
            cout << "The BinaryTree is empty." << endl;
            }
        }
    ~BiTree()
    {Release(root);}
    int Depth(){return Depth(root);}

    int FindPath(T i)
        {
        stack<BiNode<T>*> sta;
        return FindPath(i, root, sta);
        };
private:
    BiNode<T> *root;
    void Create(BiNode<T>* &bt);
    void Release(BiNode<T> *bt);
    int Depth(BiNode<T>* bt);
    int FindPath(T i, BiNode<T>* bt, stack<BiNode<T>*> &sta);
    };
//析构函数
template <class T>
void BiTree<T>::Release(BiNode<T> *bt)
    {

    if(bt==NULL)
        {
        Release(bt->lchild );
        Release(bt->rchild );
        delete bt;
        }
    }
//建立二叉树
template <class T>
void BiTree<T>::Create(BiNode<T>* &bt)
    {
    T ch;
    cin>>ch;
    if(ch== 0)bt=NULL;
    else
        {
        bt=new BiNode<T>;
        bt->data =ch;
        cout<<"调用左孩子"<<endl;
        Create(bt->lchild );
        cout<<"调用右孩子"<<endl;
        Create(bt->rchild );
        }
    }
//求树的深度
template <class T>
int BiTree<T>::Depth(BiNode<T>* bt)
    {
    if (NULL == bt)
        {
        return 0;
        }
    int d1 = Depth(bt->lchild);
    int d2 = Depth(bt->rchild);
    return (d1 > d2 ? d1 : d2)+ 1;
    }
template <class T>
int BiTree<T>::FindPath(T i, BiNode<T>* bt, stack<BiNode<T>*> &sta)
    {
    if (NULL != bt)
        {
        sta.push(bt);
        }
    sum += bt->data;
    if (sum == i && bt->lchild == NULL && bt->rchild == NULL)
        {
        stack<BiNode<T>*> sta2(sta);
        BiNode<T>* p;
        cout << "One of the path is: " ;
        while (!sta2.empty())
            {
            p = sta2.top();
            cout << p->data << " ";
            sta2.pop();
            }
        cout << endl;
        count ++;
        }
    if (NULL != bt->lchild)
        {
        FindPath(i, bt->lchild, sta);
        }
    if (NULL != bt->rchild)
        {
        FindPath(i,bt->rchild, sta);
        }
    sum -= bt->data;
    sta.pop();
    return count;
    }
int main()
    {
    BiTree<int> a;
    cout << "There are " << a.FindPath(9) << " path all." << endl;
    return 0;
    }

