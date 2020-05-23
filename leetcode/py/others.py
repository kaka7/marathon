#encoding=utf-8
"""
-------------------------------------------------
   File Name：     others
   Description :
   Author :       naruto
   date：          7/16/19
-------------------------------------------------
   Change Activity:
                   7/16/19:
-------------------------------------------------
"""
__author__ = 'naruto'

import os

import numpy as np
def f_x2(x):
    return x*x-2 #逼近法,根是根号2,目的是找到f=0对应的点就是结果,只有通过迭代
def get_root_2(n,f):
    diff=1
    a = 0.0
    b = 2.0
    while diff>n:
        if f(a)*f((a+b)/2.0)<0:
            b=(a+b)/2.0
        else:a=(a+b)/2.0
        # media=f((a+b)/2)-2
        # if media>n:
        #     b=media
        # else:a=media
        diff=b-a
    print((a+b)/2)


    # sum=0
    # for i in range(1,n+1):
    #     sum+=1.0/n *(i*1.0/n - 0.5/n)
    # print(sum)
get_root_2(0.000000001,f_x2)



#0723
import numpy as np
m=np.random.random((4,4))
print(m)
left = 0
up = 0
down, right = m.shape
def print_matrix(m,up, left,down, right):
    """

    :param m:
    :param up: 起点索引
    :param left:
    :param down: m.shape
    :param right:
    :return:
    """

    l=left
    u=up
    while left<right :
        print(m[up][left])
        left+=1
    left -= 1
    up += 1
    while up<down:
        print(m[up][left])
        up+=1
    up -= 1#避免越界
    left -= 1#避免重复
    while l<=left:#等号重要
        # left-=1
        print(m[up][left])
        left-=1
    up -= 1
    left += 1
    while u<up:
        print(m[up][left])
        up-=1
    up, left=up+1,left+1
    down, right=down-1, right-1
    # down, right=down, right
    tmp=m[up:down][left:right]
    # np.em
    if tmp.size:
        print_matrix(m,up, left,down, right)
    else:
        return
print_matrix(m,up, left,down, right)

def create_matrix(a):
    len_a=len(a)
    x=[]
    x.append(1)
    for i in range(1,len_a):
        x.append(a[i-1]*x[i-1])
    y=[]
    y.insert(0,1)
    for i in range(len_a,1,-1):
        y.insert(0,y[0]*a[i-1])
    r=[]
    for i in range(len_a):
        r.append(x[i]*y[i])
    print(r)
a=[1,2,3,4,5]
create_matrix(a)


def loop_print(m,n):
    a=[i for i in range(m)]
    def helper(x,n):
        if not len(x) or n<=0:
            return
        if len(x)==1:
            print(x.pop(n - 1))
            return
        if len(x)>n:
            print(x.pop(n-1))
            if len(x[n-1:])<n:
                x = helper(x[n - 1:].extend(x[:n - 1]), n)

            else:# len(x[n-1:])==n:
                x=x[:n-1].extend(helper(x[n - 1:],n))



            # if len(x[n-1:])>n and len(x[n-1:])<2*n:
            #     x=helper(x[n-1:].extend(x[:n-1]),n)
            # elif len(x[n-1:])==n:
            #     x=helper(x)

            # else:
            #     # print(x.pop(n - 1))
            #     x=helper(x,n-len(x[n-1:]))
            #     # x = helper(x, n)
        elif len(x)==n:
            print(x.pop(n - 1))
            # x=helper(x,n)
        else:
            x=helper(x,n-len(x))
        return x
    while len(a):
        a=helper(a,n)
# loop_print(10,5)

def loop_print2(m,n):
    def helper(x,n):
        if not len(x) or n<=0:
            return
        if len(x)==1:
            print(x.pop(n - 1))
            return
        if n<=len(x):
            print(x.pop(n - 1))
            return x

        # return x

    a=[i for i in range(m)]
    count=0
    step=0
    len_a=len(a)
    b=a.copy()

    while len(a):
        for j in a:
            count+=1
            step+=1
            if count==n:
                print(j)
                # b.pop(i)
                del b[b.index(j)]
                len_a-=1
                step-=1
                count=0
            if count<n and count>0 and step==len_a and len_a==n:
                tmp=b[-count:]+b[:-count]
                a =tmp.copy()
                b=tmp.copy()
                count = 0
                step = 0
            if count==0 and step==len_a:
                a=b.copy()
                # count = 0
                step = 0
            if len(a)<n:
                if step==len_a and count==len_a:
                    a=helper(a, n - len(a))
def loop_print3(m,n):
    a=[x for x in range(m)]
    def helper(a_list,p):
        if len(a_list)==0:
            return
        if len(a_list)>=p:
            print(a_list.pop(p-1))# pop (index)
            return a_list
        else:
            return helper(a_list,p-len(a_list))

    while len(a):
        if len(a)>=n:
            print(a.pop(n-1))
            a=a[n-1:]+a[:n-1]
        else:
            a=helper(a,n-len(a))

loop_print3(10,5)



# max(a[l:r])<min(b[l:r])

def max_min(a,b):
    assert len(a)==len(b)
    l_len=len(a)
    assert l_len>0
    count=0
    for i in range(l_len+1):
        for j in range(i+1,l_len+1):
            if max(a[i:j])<min(b[i:j]): #沒有中間變量　但是调用系统ｍａｘ函数，不好
                count+=1
    print("max less min :",count)

def max_min2(a,b):
    assert len(a)==len(b)
    l_len=len(a)
    assert l_len>0
    count=0
    # if a[0]<q_b[-1]: count+=1
    for i in range(l_len):
        q_a = [i]#保存索引queue　升序　但是还是用了两层循环　且有中间变量
        q_b = [i]#降序
        if a[i]<b[i]:
            count+=1
        for j in range(i+1,l_len):
            if a[q_a[-1]]<a[j]:
                q_a.append(j)
            if b[q_b[-1]]>b[j]:
                q_b.append(j)
            if a[q_a[-1]]<b[q_b[-1]]:
                count+=1
    print("max less min :",count)

def max_min3(a,b):
    """
    能否用队列？？？ 就要用中间变量
    :param a:
    :param b:
    :return: idx 最后和len相等，
    """
    assert len(a)==len(b)
    l_len=len(a)
    # assert l_len>0  再次体现递归要有结束条件而不能用assert
    if l_len==0:
        return 0
    idx=0#记录起始位置 避免额外空间　传递给递归函数
    q_a = [0]#保存索引queue　升序　但是还是用了两层循环　且有中间变量　用于代替重新计算的max min 　或者直接保存单个的最值
    q_b = [0]#降序
    count = 0
    if a[0]<b[0]:
        count+=1
    for j in range(1,l_len):
        if a[q_a[-1]]<a[j]:
            q_a.append(j)
        if b[q_b[-1]]>b[j]:
            q_b.append(j)
        if a[q_a[-1]]<b[q_b[-1]]:#
        # if max(a[idx:j+1]) < min(b[idx:j+1]):
            count+=1
        # ??？＝有影响
        # else:#此时被截断　因为新加的元素不会导致当前max_a减小，min_b变大　依然满足max_a<min_b,所以被截断
        #     count+=max_min3(a[idx:j],b[idx:j])#递归函数要获得的是单个count则直接+传递,其他占用空间大的则直接覆盖（返回地址，c++中引用），
        #     idx=j#跟新起始idx
    # if　idx < l_len:  # 为啥不能用while??? max_min3 已传入idx信息　用队列是否更好
    if idx<l_len:
        idx+=1
        count += max_min3(a[idx:], b[idx:])#变相循环 不好
            # while len(q_a)>0 and len(q_b)>0 and idx <=j:
    return count

def max_min4(a,b):
    """
    能否用队列？？？ 就要用中间变量
    :param a:
    :param b:
    :return: idx 最后和len相等，
    """
    assert len(a)==len(b)
    l_len=len(a)
    # assert l_len>0  再次体现递归要有结束条件而不能用assert
    if l_len==0:
        return 0
    idx=0#记录起始位置 避免额外空间　传递给递归函数
    q_a = [0]#保存索引queue　升序　但是还是用了两层循环　且有中间变量　用于代替重新计算的max min 　或者直接保存单个的最值
    q_b = [0]#降序
    count = 0
    if a[0]<b[0]:
        count+=1
    for j in range(1,l_len):
        if a[q_a[-1]]<a[j]:
            q_a.append(j)
        if b[q_b[-1]]>b[j]:
            q_b.append(j)
        # if a[q_a[-1]]<b[q_b[-1]]:#
        if max(a[idx:j+1]) < min(b[idx:j+1]):
            count+=1
        # ??？＝有影响
        else:#此时被截断　因为新加的元素不会导致当前max_a减小，min_b变大　依然满足max_a<min_b,所以被截断
            if len(q_a)>1:
                count+=max_min4(a[idx:j],b[idx:j])#递归函数要获得的是单个count则直接+传递,其他占用空间大的则直接覆盖（返回地址，c++中引用），
                idx=j#跟新起始idx

     # 为啥不能用while??? max_min3 已传入idx信息　用队列是否更好

    if idx<l_len:
        idx+=1
        count += max_min4(a[idx:], b[idx:])#变相循环 不好
            # while len(q_a)>0 and len(q_b)>0 and idx <=j:

    return count



a=[0,1,2,3]
b=[4,5,6,7]
import numpy as np
from random import  shuffle
a=[x for x in range(10)]
b=[x for x in range(10)]
shuffle(a)
shuffle(b)
#
# a=[1, 0, 8, 6, 7, 2, 3, 4, 5, 9]
# b=[5, 1, 7, 3, 2, 8, 6, 4, 9, 0]
a=[4, 2, 3, 0, 1]
b=[4, 2, 0, 1, 3]
# a=[3,2,1]
# b=[3,3,3]
print(a)
print(b)
max_min(a,b)
max_min2(a,b)
print(max_min3(a,b))
print(max_min4(a,b))






