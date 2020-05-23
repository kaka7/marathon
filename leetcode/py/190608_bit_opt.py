#encoding=utf-8
"""
-------------------------------------------------
   File Name：     190608_bit_opt
   Description :
   Author :       naruto
   date：          6/8/19
-------------------------------------------------
   Change Activity:
                   6/8/19:
-------------------------------------------------
"""
__author__ = 'naruto'

import os
if __name__=="__main__":
    #××××××××××××××××××××××××××××××××××××××××××××××××××判断二进制位数
    # n=7
    # count=0
    #
    # while(n>0):
    #     n=n&(n-1)# bit and
    #     count+=1
    # print(count)
    #
    # count=0
    # n=6
    # while(n>0):
    #     # if n&1==1:
    #     if n%2==1:
    #
    #         count+=1
    #     n=n>>1
    #
    # print(count)


    #*****************************************************判断奇数和偶数
    def judge_o(n):
        if n&1==1:
            print(True)
        else :
            print(False)

    for i in map(judge_o,[x for x in range(5)]):
        print (i)

    # for i in map(lambda x: x ** 2, [1, 2, 3, 4, 5]):
    #     print (i)

    #****************************************************交换两个数
    # #异或的交换率和结合率
    # #n^n=0 n^0=n
    # x=x^y
    # y=x^y
    # x=x^y

    #****************************************************m的n次幂
    def pow_m_n(m,n):
        product=1
        tmp=m
        while n>0:
            if n&1==1:
                product=product*tmp
            else:
                pass
            tmp=tmp*tmp
            n=n>>1
        print(product)
    pow(2,13)

    #****************************************************找出不重复的数
    # tmp=a[0]
    # for
    #     tmp=tmp^a[i]

    #****************************************************不大于n的最大2幂指数　１０２３－＞５１２
    def get_max_2(n):
        pro=1
        while n>>1:
            pro=pro*2
            n=n>>1
        print(pro)
    get_max_2(1023)

    #***************************************************是否是２的幂指数
    def judge_2(n):
        count=0
        while n>0:
            count+=1
            n=n&(n-1)
            if count>1:
                return False
        return True
    print(judge_2(6))

    # 法２：  利用只有一个１的特点
    # return n&(n-1)

    #***************************************************n,m中移动的位数　异或后算１的位数






    #链表双指针　
    # 判断有环
    # 中间数
    # 倒数第k个数
    # 两数之和





