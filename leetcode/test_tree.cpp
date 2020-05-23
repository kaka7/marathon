#include <stdio.h>
#include <stdlib.h>
#include <memory.h>

typedef struct Node{
    int data;
    struct Node * LChild;
    struct Node * RChild;
    }BitNode,*BiTree;

void CreateTree(BiTree *bt,int a[],int len,int index)
    {
    //从数组a中创建二叉树，len为数组a的长度-1。index初始值为0。
    if(index>len) return;
    (*bt)=(BiTree)malloc(sizeof(BitNode));
    (*bt)->data=a[index];
    CreateTree(&((*bt)->LChild),a,len,2*index+1);
    CreateTree(&((*bt)->RChild),a,len,2*index+2);
    }

int main()
    {
    int arr[]={3,1,4,1,5,9,2,6,5,3,5,8,9,7,9};
    BiTree root;
    CreateTree(&root,arr,sizeof(arr)/sizeof(int),0);
    }