__author__ = 'hadoop'
#coding :utf-8
def MIN(a,b):
    if a<=b:return a
'''
def bag(num,c,v,w,d):
    if num ==0:
        d[num]==0
        bag(num+1,c,v,w,d)
    else:
        Min=999
        tag=False
        for i in range(len(w)):
            if num>=w[i]:
                Min=min(d[num-w[i]]+1,Min)
                tag==True
        if tag==False:Min==0
        d[num]=Min
        if num==c:return d
        else:bag(num+1,c,v,w,d)

if __name__=='__main__':
    n=5
    c=10
    dp=[0 for i in range(11)]
    w=[1,2,3,4,5]
    v=[6,3,5,4,6]
    res=bag(0,10,v,w,dp)
'''
'''
def bag(n,c,w,v):
    res=[[-1 for j in range(c+1)] for i in range(n+1)]
    for j in range(c+1):
        res[0][j]=0
    for i in range(1,n+1):
        for j in range(1,c+1):
            res[i][j]=res[i-1][j]
            if j>=w[i-1] and res[i][j]<res[i-1][j-w[i-1]]+v[i-1]:
                res[i][j]=res[i-1][j-w[i-1]]+v[i-1]
    return res

def show(n,c,w,res):
    print('最大价值为:',res[n][c])
    x=[False for i in range(n)]
    j=c
    for i in range(1,n+1):
        if res[i][j]>res[i-1][j]:
            x[i-1]=True
            j-=w[i-1]
    print('选择的物品为:')
    for i in range(n):
        if x[i]:
            print('第',i,'个,')
    print('')


if __name__=='__main__':
    n=5
    c=10
    w=[2,2,6,5,4]
    v=[6,3,5,4,6]
    res=bag(n,c,w,v)
    show(n,c,w,res)
'''
def fibfun(a,b,alist):
    if a==1:
        alist[a]==1
        fibfun(a+1,b,alist)
    if a==2:
        alist[a]==2
        fibfun(a+1,b,alist)
    if a>2:
        alist[a]=alist[a-1]+alist[a-2]
    if a==b:return alist
    else:fibfun(a+1,b,alist)

if __name__=="__main__":
    dp=[0 for i in range(11)]
    print fibfun(1,6,dp)
    import profile
    profile.run(fibfun())