#encoding=utf-8
"""
-------------------------------------------------
   File Name：     5_algs
   Description :
   Author :       naruto
   date：          7/20/19
-------------------------------------------------
   Change Activity:
                   7/20/19:
-------------------------------------------------
"""
__author__ = 'naruto'

seq = [3, 4, 1, 6, 3, 7, 9, 13, 93, 0, 100, 1, 2, 2, 3, 3, 2]
def partion(a_list):
    split=a_list[0]
    less=[x for x in a_list[1:] if x<=split]#[1:] 很重要
    bigger=[x for x in a_list[1:] if x>split]
    return less,split,bigger
def find_kth_min(a_list,k):
    less,split,bigger=partion(a_list)
    l=len(less)
    if l==k:
        return split
    elif l<k:
        return find_kth_min(bigger,k-l-1)
    else:
        return find_kth_min(less,k)
print(find_kth_min(seq,3))#分治，分解成相同子问题（可能需要合并），子问题的解非独立　用于并行
# https://www.cnblogs.com/hhh5460/p/6851013.html
# 题目1. 给定一个顺序表，编写一个求出其最大值的分治算法。
# 题目2. 给定一个顺序表，判断某个元素是否在其中。
# 题目4. 快速排序？无交叉？？？复杂度
# 题目5. 合并排序（二分排序）
# 题目6. 汉诺塔
# 问题8. 给定平面上n个点，找其中的一对点，使得在n个点的所有点对中，该点对的距离最小。（最近点对问题）？？？
# 问题8. 从数组 seq 中找出和为 s 的数值组合，有多少种可能？？？

#DP
def find(seq, s):
    n = len(seq)
    if n == 1:#也可和下一个if合并
        return [0, 1][seq[0] == s]#相等则为ｔｒｕｅ＝＝１，返回１即有一种

    if seq[0] == s:
        return 1 + find(seq[1:], s)#第一个就匹配到了则说明有一种了，就可以找余下的
    # else:
        # return find(seq[1:], s - seq[0]) \
        #        + find(seq[1:], s)
    elif seq[0]<s:
        return find(seq[1:], s - seq[0])+\
               find(seq[1:], s)#seq[-1]==s
    else:
        return find(seq[1:], s)




# 测试
seq = [1, 2, 3, 4, 5, 6, 7, 8, 9]
s = 7  # 和
print(find(seq, s))  # 15




#回溯算法　试探
# 回溯法.这题超级绕人
# 详细参考：https://darktiantian.github.io/%E7%9F%A9%E9%98%B5%E4%B8%AD%E5%8D%95%E8%AF%8D%E7%9A%84%E8%B7%AF%E5%BE%84%EF%BC%8C%E5%BE%88%E5%A4%9A%E4%BA%BA%E9%83%BD%E9%94%99%E4%BA%86/
# 参考链接里有一个很巧妙地测试用例。
# https://blog.csdn.net/dududududou/article/details/93111593
class Solution:
    def exist(self, board, word):
        l1 = len(board)  # 行数
        l2 = len(board[0])  # 列数

        def spread(i, j, w):  # 函数功能：判断当前位置之后的字母是否都能找到
            if not w:  # 当字符串是空时候，返回True。”因为如果能找到，最后肯定是空“
                return True
            initial, board[i][j] = board[i][j], '*'  # 将用过的字母用*抹去，并用临时变量存储他
            flag = False  # 标志位，置为false
            # print('({}, {}) {}, {}'.format(i, j, w, board))
            for x, y in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)):  # 循环查找上下左右四个位置
                if 0 <= x < l1 and 0 <= y < l2 and board[x][y] == w[0]:  # 如果当前查找的是合法且匹配的
                    if spread(x, y, w[1:]):  # 递归调用
                        flag = True  # 递归结束之后，标志位置为true，表示ok
                        break  # 结束for循环
            board[i][j] = initial  # for循环结束后，一步一步的还原二位列表中的*
            # print('flag{}, recover ({}, {}), after {}'.format(flag, i, j, board))
            return flag

        for i in range(l1):  # 遍历每个元素，找符合条件的第一个字母
            for j in range(l2):
                if board[i][j] == word[0] and spread(i, j, word[1:]):
                    return True
        return False
# 回溯在那呢？
# 答：17行 if spread(x,y,w[1:]):   # 递归调用
# 如果spread返回的是False,就执行20行：board[i][j] = initial   即为回溯。
# 比如说，for循环在判断’下‘位置时候，执行17行的spread,这个spread返回的是False
# （即下一步的上下左右都执行完了，然后返回22行的false），
# 接着就把上一步的*置换回去；
# 注意，此时刚刚的for循环还没执行完呢！接着执行’左‘位置，执行17行的spread。。。。（最绕人的就是在这）


#todo
import numpy as np
def moving_count(rows,cols,n,a):

    for i in range(rows):
        for j in range(cols):
            if i<0 or j<0 or i>=rows or j>=cols or a[i][j]==1 or help_sum(i)+help_sum(j)>n:
                return 0
            a[i][j]=1
            x1=moving_count(i-1,j,n,a)
            x2=moving_count(i+1,j,n,a)
            x3=moving_count(i,j-1,n,a)
            x4=moving_count(i,j+1,n,a)+1
            print(x1,x2,x3,x4)
            return x1+x2+x3+x4

def help_sum(x):

    SUM=0
    while x:
        SUM+=x%10
        x=x//10
    return SUM
a=np.zeros((4,4))

print(moving_count(4,4,9,a))


