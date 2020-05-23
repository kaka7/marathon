
// 1 ??????
#include<iostream>
#include<vector>
using namespace std;
struct ListNode {
        int val;
       struct ListNode *next;
       ListNode(int x) :
              val(x), next(NULL) {
        }
  };
class Solution {
public:
    vector<int> ArrayList;
    vector<int> printListFromTailToHead(ListNode* head) {
       // if(head==NULL)
         //   return head;
        ListNode* tail=nullptr;
        ListNode* temp=nullptr;
        while(head)
        {
            temp=head;
            head=head->next;
            temp->next=tail;
            tail=temp;
        }
        while(tail)
        {
            ArrayList.push_back(tail->val);//非tail.val
            tail=tail->next;
        }
        return ArrayList;
        
    }
};

//2 ??stack

// #include <iostream>
// #include <stack>
// #include <vector>
// using namespace std;
// struct LinkNode{
// public :
//     int val;
// struct LinkNode* next;
// };

// class Solution{
// public:
//     vector <int> printListFromTailToHead(struct LinkNode* head) //??stack ?????
//         {
//     LinkNode* node = head;
//     stack<int> st;
//     int count =0;
//     while(node !=NULL)
//     {
//         cout<<node->val<<" in stack"<<endl;
//         st.push(node->val);
//         count++;
//         node=node->next;
//     }
//     vector <int> res(count);
//     cout<<"count="<<count<<endl;
//     for (int i=0;i<count && st.empty()!=true;i++)
//     {
//         cout<<st.top()<<" in vector "<<endl;
//         res[i]= st.top();
//         st.pop();


//     }
//                 return res;
//         }
// };

// int main(){
//     LinkNode list[4];
//     list[0].val=1;
//     list[0].next=&list[1];
//     list[1].val=2;
//     list[1].next=&list[2];
//     list[2].val=3;
//     list[2].next=&list[3];
//     list[3].val=4;
//     list[3].next=NULL;
//     Solution solu;
//     vector <int> res=solu.printListFromTailToHead((list));
//     cout<<res.size()<<endl;
//     for (int i=0;i<res.size();i++)
//     {
//         cout<<res[i]<<endl;

//     }
// }