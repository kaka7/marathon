
#include <vector>
#include <iostream>
using namespace std;
struct zoo
{
    string name;
    int age;
};

struct TreeNode
{
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode(int x) : val(x), left(NULL), right(NULL) {}
};
class Solution
{
public:
    TreeNode *reConstructBinaryTree(vector<int> pre, vector<int> vin)
    {
        if (pre.empty() || vin.empty())
            return NULL; //#指针为空时置NULL
        std::cout << "new rec" << std::endl;
        for (auto iter : vin)
        {
            cout << iter << endl;
        };

        int root = pre[0];
        // b_tree->val = root;
        TreeNode *b_tree = new TreeNode(pre[0]); //#此时

        if (pre.size() == 1)
        {
            return b_tree;
        }
        // pre.erase(pre.begin(), pre.begin() + 1);

        bool flag = true;
        vector<int> i_left, i_right, p_left, p_right;
        for (auto iter : vin)
        {
            if (iter == root)
                flag = false;
            else //#太重要了,不然就重复
            {
                if (flag)
                    i_left.push_back(iter);
                else
                    i_right.push_back(iter);
            }
        }
        int left_len = i_left.size();
        for (int i = 0; i < left_len; i++)
            p_left.push_back(pre[i + 1]);
        for (int i = 0; i < pre.size() - left_len - 1; i++)
            p_right.push_back(pre[i + left_len + 1]);

        // pre.clear();
        // vin.clear();
        if (!p_left.empty() || !i_left.empty())
            b_tree->left = reConstructBinaryTree(p_left, i_left);
        if (!p_right.empty() || !i_right.empty())
            b_tree->right = reConstructBinaryTree(p_right, i_right);
        return b_tree;
    }
};
void preOrder(TreeNode *tree)
{
    if (tree != NULL)//#不能是while
    {
        std::cout << tree->val << endl;
        preOrder(tree->left);
        preOrder(tree->right);
    }
}
int main()
{

    vector<int> pre{1, 2, 4, 7, 3, 5, 6, 8};
    vector<int> vin{4, 7, 2, 1, 5, 3, 8, 6};
    Solution *s = new Solution();
    TreeNode *newtree = s->reConstructBinaryTree(pre, vin);
    delete s;
    std::cout << "result:" << endl;
    preOrder(newtree);

    return 0;
}

//#另外的思路 	BinaryTree *Root = GetBinaryTree( PreOrder, 0, 12, InOrder, 0, 12);
//#结构体指针初始化要赋值:TreeNode* b_tree=new TreeNode(pre[0]);//#此时如果是TreeNode *f就是野指针没有申请空间,即没有创建对象,并且函数返回也是野的,
//#因为结构体指针变量是没有构造函数的,所以要赋值,没有赋值,就不会空间,而class成员变量都有构造函数
//#结构体中没有指针时可以直接初始化,struct_name s; 需要用指针时&s
//#函数中的临时变量是返回后就被清除了
