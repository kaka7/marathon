#include <stack>
using namespace std;

#include<stack>
using namespace std;
#include<stack>
using namespace std;
class Solution
{
public:
    void push(int node) {
        //这有点麻烦了,直接用两个stack分别记录内容和地址
        while(! stack2.empty())
        {
            stack1.push(stack2.top());//pop是移除,不代表返回,所以要用top ,
            stack2.pop();
        }
        stack1.push(node);

    }

    int pop() {
        int tem;
        while(! stack1.empty())
        {
            stack2.push(stack1.top());
            stack1.pop();
        }
        if(! stack2.empty())
        {
            tem= stack2.top();
            stack2.pop();
        }
        return tem;

    }

private:
    stack<int> stack1;
    stack<int> stack2;
};

int main()
{
    Solution *s = new Solution();
    s->push(3);
}