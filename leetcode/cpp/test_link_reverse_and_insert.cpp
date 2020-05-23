//
// Created by naruto on 9/8/19.
//
#include <iostream>
#include <assert.h>
using namespace std;

//typedef struct Node
//    {
//    int val;
//    Node * next;
//
//    } node;

struct node
    {
    int val;
    node * next;
    };

void print_link(node *lnode);
void linkinsert(node * head,int val,int idx=-1);
node * reverse_link(node * head);


int main(void)
    {
    int arr[]={1,2,3,4,5};
    int arr_len=sizeof(arr)/sizeof(int);
    node lnode[arr_len];//会产生５个类似数组
    for (int i=0;i<arr_len;i++)
        {
        lnode[i].val=arr[i];
        if (i==arr_len-1)
            {
            lnode[i].next=NULL;
            }
        else
            {
            lnode[i].next=&lnode[i+1];    //node* first = new node(1);     first->next = second;
            }

        }
    cout<<"init linklist done!!!"<<endl;

    print_link(lnode);//因为lnode类似是数组，数组名可以直接当地址


   linkinsert(lnode,7,1);
//    print_link(lnode);//为啥变了todo ???
    node * tmp=reverse_link(lnode);
    }

void print_link(node *lnode)
    {
    cout<<"打印链表"<<endl;
    node *pr = lnode;// 非 &lnode
    while (pr)//不能是pr->next　这样会导致少一个数
        {
        cout << pr->val << endl; //只能->
        pr = pr->next;
        }
    }

void linkinsert(node * head,int val,int idx)
    {
    assert(idx>-2);
    node * head_bak=head;

    if (idx==-1)
        {
        node * tmp=head;
        while(tmp->next)//如果tmp为null那ｖａｌ就没有值
            {
            tmp=tmp->next;
            }

        node  n;//不能用指针　对于单个节点不应该是指针
        n.val=val;
        n.next=NULL;
        tmp->next=&n;//导致循环？？？todo error
        }
    else
        {
        int count=0;
        node * tmp=head;
        while(tmp->next)
            {
            count++;
            if (count==idx)
                {
                node n;
                n.val=val;
                n.next=tmp->next;
                tmp->next=&n;
                break;
                }
            else
                {
                tmp=tmp->next;

                }
            }
        }
//    return head_bak;
    }


node * reverse_link(node * head)
    {
    node * head_bak=head;
    node *p1=NULL;
    node *p2=NULL;
    while(head)
        {
        p1=head;
        head=head->next;//一定要放到这
        p1->next=p2;//截断并且和以前的反向拼接
        p2=p1;
        }

    cout<<"after reverse:"<<endl;
    while(p2)
        {
        cout<<p2->val<<endl;
        p2=p2->next;
        }

    return p2;
    }

