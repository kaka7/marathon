#encoding=utf-8
"""
-------------------------------------------------
   File Name：     DP
   Description :
   Author :       naruto
   date：          8/13/19
-------------------------------------------------
   Change Activity:
                   8/13/19:
-------------------------------------------------
"""
__author__ = 'naruto'

import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import sys

import numpy as np
m,n=2,3
grid=np.zeros((m+1,n+1))
# m,n=grid.shape
grid[0,:]=1
grid[:,0]=1
for i in range(1,m+1):
    for j in range(1,n+1):
        grid[i][j]=grid[i][j-1]+grid[i-1][j]
print(grid[m][n])

"""给定一个矩阵m，从左上角开始每次只能向下或者向左走，最后到达右下角的位置，路径上的数字累加起来就是路径和，
返回所有路径中最小路径和。如果给定矩阵如下，则路径1,3,1,1,6,1是所有路径中路径和最小的，所以返回13.。
1 3 5 9

8 1 3 4

5 1 6 1

8 8 4 0
--------------------- 
"""
def matrix_path_least(a,m,n):
    if m<1 or n<1:
        print()
        return 0#因为要相加，所以即便是空的也要返回０，否则会报错
    if a[:m,:n].size==1:
        print(a[:m,:n])
        return a[:m,:n]
    if a[:m,:n].size==2:
        print(a[:m,:n].sum())
        return a[:m,:n].sum()
    if a[:m,:n].size>2:
        print(a[m-1,n-1]+min(matrix_path_least(a,m-1,n),matrix_path_least(a,m,n-1)))
        return a[m-1,n-1]+min(matrix_path_least(a,m-1,n),matrix_path_least(a,m,n-1))
a=np.array([[1,3,5,9],[8,1,3,4],[5,1,6,1],[8,8,4,0]])
print(matrix_path_least(a,4,4))#error

# dp[m][n]保存用于递推

#走台阶
#绵羊出生问题

#找零钱:最少钱币数，可重复
def charge(num):
    print("charge")
    charges=[5,3,2]#由于最少，所以优先用大的
    charges_num=np.zeros((num+1,len(charges)+1))#每行中只有一个非０,代表数量而非具体每个币值的数量
    for x in range(1,num+1):
        for idx,y in enumerate(charges):
            if x ==y:
                charges_num[x,idx+1]=1
                break#由于之前已经保存了小的找零数，所以小的不用接着算了
            elif x>y:
                charges_num[x, idx+1]=charges_num[x-y].sum()+1
                break#由于之前已经保存了小的找零数，所以小的不用接着算了
            else:#没有可以兑换的纸币所以都为０
                pass                # charges_num[x, idx+1]=0
    print(charges_num[num])
charge(20)



