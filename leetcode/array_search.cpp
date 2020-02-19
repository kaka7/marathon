#include <iostream>
#include <vector>
using namespace std;

// class Solution
// {
// public:
//     bool Find(int target, vector<vector<int>> array)
//     {
//         int rows = array.size();
//         int cols = array[0].size();
//         std::cout << rows << "  " << cols << endl;
//         int i = 0, j = cols - 1;
//         // for (int i=0;i<rows-1;i++)
//         // {
//         //     for(int j=cols-1;j>0;j--)
//         while (i < rows - 1 || j > 0)
//         {
//             cout << "cur:" << array[i][j] << endl;
//             if (array[i][j] > target)
//             {
//                 j--;
//                 cout << "bigger ,j--" << endl;
//             }
//             else if (array[i][j] < target)
//             {
//                 i++;
//                 cout << "less i++" << endl;
//             }
//             else
//             {
//                 cout << "searched" << endl;
//             return true;
//             }
//         }
//         // }
//         return false;
//     }
// };

class Solution {
public:
    bool Find(int target, vector<vector<int> > array) {
        int rows = array.size();
        int cols = array[0].size();
        std::cout << rows << "  " << cols << endl;
        int i = 0, j = cols - 1;
        // for (int i=0;i<rows-1;i++)
        // {
        //     for(int j=cols-1;j>0;j--)
        // while (i < rows - 1 && j > 0 )
                while (i < rows &&  j >= 0 )

        {
            cout << "cur:" << array[i][j] << endl;
            if (array[i][j] > target)
            {
                j--;
                cout << "bigger ,j--" << endl;
            }
            else if (array[i][j] < target)
            {
                i++;
                cout << "less i++" << endl;
            }
            else
            {
                cout << "searched" << endl;
                return true;
            }
        }
        // }
        return false;
        
    }
};

int main()
{
    vector<int> ar = {1, 2, 8, 9};
    vector<vector<int>> arr;
    arr.push_back(ar);
    // ar.clear;
    ar = {4, 7, 10, 13};
    arr.push_back(ar);
    Solution *s = new Solution();
    std::cout << s->Find(7, arr) << endl;
}

// g++ -std=c++11  -o demo array_search.cpp && ./demo 