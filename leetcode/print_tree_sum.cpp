//
// Created by naruto on 11/25/19.
//
#include <iostream>
#include <vector>
#include <string>
#include <stdio.h>
#include <string.h>
using namespace std;

struct Node{
    int   Data;
    Node *pLeft;
    Node *pRight;
    };

Node* buildTree(int *piValue, int iStart, int iLength)
    {
    if (iStart>=iLength){
        return NULL;
        }

    Node *pRoot = new Node;
    pRoot->Data  = piValue[iStart];
    pRoot->pLeft  = buildTree(piValue, iStart*2+1, iLength);
    pRoot->pRight = buildTree(piValue, iStart*2+2, iLength);

    return pRoot;
    }

Node* buildCompleteTree(int *piValue, int iLength)
    {
    if (piValue==NULL || iLength<=0){
        return NULL;
        }

    return buildTree(piValue, 0, iLength);
    }

void preOrderRecursive(Node *pRoot)
    {
    if (pRoot){
        cout<<pRoot->Data<<" ";
        preOrderRecursive(pRoot->pLeft);
        preOrderRecursive(pRoot->pRight);
        }
    }

class Solution {
public:
    vector<vector<int> > FindPath(Node* root,int expectNumber)
        {
        if(root)
            {
            dfsFind(root, expectNumber);
//        cout<<allRes<<endl;
            vector<vector<int > >::iterator iter;
            if (allRes.size())
                {
                cout<<"找到路径和如下:"<<endl;
                for (iter = allRes.begin(); iter != allRes.end(); ++iter)
                    {
                    for (int i = 0; i < (*iter).size(); ++i)
                        {
                        cout << (*iter)[i];
                        if (i < (*iter).size() - 1)
                            cout << ",";
                        }
                    cout << endl;
                    }

                }
            else
                cout<<"error"<<endl;
            }


      return allRes;
        }
//    return allRes;

    void dfsFind(Node * node , int target)
        {
        tmp.push_back(node->Data);

        if(!node->pLeft && !node->pRight)
            {
            if(target - node->Data == 0)
                allRes.push_back(tmp);
            }
        else
            {
            if(node->pLeft) dfsFind(node->pLeft, target - node->Data);
            if(node->pRight) dfsFind(node->pRight, target - node->Data);
            }

        if(!tmp.empty())
            tmp.pop_back();
        }
private:
    vector<vector<int> >allRes;
    vector<int> tmp;
    };


int main()
    {
    cout<<"请在英文模式下分别输入路径和以及树的节点值(以逗号分隔)"<<endl;
//    int data[9] = {10,5,12,4,7};
    int target;
    cin>>target;
    string s;

    while(cin>>s)
        {
        vector<int> nums;
        char *str = (char *) s.c_str();
        const char *split = ",";
        char *p = strtok(str, split);
        int a;

        while (p != NULL)
            {
            sscanf(p, "%d", &a);//char ---> int
            nums.push_back(a);
            p = strtok(NULL, split);
            }

//        for (int i = 0; i < nums.size(); i++)
//            {
//            printf("%d\n", nums[i]);
//            }


        int n = nums.size();
        int arr[n];

        for (int i = 0; i < n; i++)
            {//
            arr[i] = nums[i];//
            }
//        cout << sizeof(arr) / sizeof(arr[0]) << endl;

        Node *pRoot = buildCompleteTree(arr, sizeof(arr) / sizeof(arr[0]));
       cout << "Pre-Order traverse:" << endl;
       preOrderRecursive(pRoot);
        Solution S;
        S.FindPath(pRoot, target);





        }
    }
