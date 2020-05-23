#encoding=utf-8
"""
-------------------------------------------------
   File Name：     190610_window_max
   Description :
   Author :       naruto
   date：          6/10/19
-------------------------------------------------
   Change Activity:
                   6/10/19:
-------------------------------------------------
"""
__author__ = 'naruto'

a=[4,3,5,4,3,3,6,7]
k=3
#维护双端队列，首尾的处理是关键

def getWindowMax(arr, k):#因为ｗｉｎｄｏｗ是代表索引　所以要有个index
    if len(arr)==0 or k<=0:
        return
    queue=[]
    res=[]
    for i,j in enumerate(a):
        while len(queue)!=0 and arr[queue[-1]]<j:
            queue.pop()#如果j比当前ｗｉｎｄｏｗ　任意一个(最后)大(小的没机会出头)，则pop ，最左端的肯定是最大的
        queue.append(i)#i 肯定会被加入ｑｕｅｕｅ　无论和ｑｕｅｕｅ【－１】大小关系
        if i-queue[0]==k:#索引过期,这里
            queue.pop(0)
        if i + 1 >=k:#保证前几个不会输出，最左端的肯定是最大的
            res.append(arr[queue[0]])
    print(res)



if __name__=="__main__":
    getWindowMax(a,k)
