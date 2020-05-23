#encoding=utf-8
"""
-------------------------------------------------
   File Name：     190731_array
   Description :
   Author :       naruto
   date：          7/31/19
-------------------------------------------------
   Change Activity:
                   7/31/19:
-------------------------------------------------
"""
__author__ = 'naruto'

import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import sys

def get_random_repeat_num(a,n):
    assert len(a)==n
    assert max(a)<=n
    assert min(a)>=0
    for i in range(len(a)):
        while i!=a[i]:
        #
        # else:
        #     pass
            if a[i]==a[a[i]]:
                print (a[i])
                return
            else:
                tmp=a[i]
                a[i]=a[tmp]
                a[tmp]=tmp
                # a[i],a[a[i]]=a[a[i]],a[i]＃坑!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! todo

            # else:
            #     a[i],a[a[i]]=a[a[i]],a[i]
    print(False)

a=[2,3,2,1]
a=[2,3,1,0,2,4,3]
get_random_repeat_num(a,7)




def get_series_sum(n):
    result=[]
    r=[]
    sum=0
    small = 1
    big = 1 + 1
    r.append(small)
    r.append(big)
    sum = sum + small + big
    # for x in range(1,int(n/2)):
    #     small = x
    #     big = x + 1
    x=1
    while x<=int(n/2):
        while sum <n:
            big+=1
            sum+=big
            r.append(big)
        if sum==n:
            result.append(r)
            print(r)
            # sum -= r.pop(0)
        else:
            pass
            # sum-=r.pop(0)
        sum -= r.pop(0)

        x+=1
    # print(result)

get_series_sum(15)


def get_2_repeat(a):
    def helper(p,i):
        tmp=p>>(i-1)#!!!!!!!!!!!!! r=1 count=1 无需移位
        if tmp%2==1:#!!!!!!!!!!!!!
            return True
        else:
            return False

    r=a[0]
    for x in a[1:]:
        r=x^r

    count=0
    r1=r
    while r1>0:
        count+=1
        if r1&1==1:
            break
        else:
            r1=r1>>1

    t_list=[]
    for x in a:
        if helper(x,count):
            t_list.append(x)

    r2=t_list[0]
    for x in t_list[1:]:
        r2=r2^x
    r3=r^r2
    print(r3)
    print(r3^r)
a=[3,4,3,5]
get_2_repeat(a)#

def series_max_sum(a):
    sum=a[0]
    total=a[0]
    for i in a[1:]:
        if total>0:
            total+=i
        else:
            total=i#!!!!!!!!!!!!!!!!
        if sum<total:
            sum=total
    print(sum)
a=[6,-3,-2,7,-15,1,2]
series_max_sum(a)


def ji_ou_change(a):#todo error
    steps=int(len(a)/2)
    count=steps
    while steps>0:
        if steps % 2 == 0:

            for x in range(count-steps,count):
                    tmp=a[2*x+1]
                    a[2 * x + 1]=a[2*x]
                    a[2*x]=tmp
        else:
            for x in range(count-steps,count):

                tmp = a[2 * x - 1]
                a[2 * x - 1] = a[2 * x]
                a[2 * x] = tmp
            # a[2*x+1],a[2*x]=a[2*x],a[2*x+1]

        steps-=1
    print(a)
    # for i in range(int(len(a)/2):
a=[x for x in range(8)]
ji_ou_change(a)
















