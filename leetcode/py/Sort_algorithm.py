__author__ = 'hadoop'
#coding :utf-8
def QuickSort(alist,start,end):
    loc = HelpQuickSort(alist)
    QuickSort(alist,start,loc)
    QuickSort(alist,loc+1,end)
def HelpQuickSort(alist):
    value = alist[0]
    start=1
    end=len(alist)-1
    left = start
    right = end;flag=1
    while flag:
        while left<=right and alist[left]<=value:left = left+1
        while left<=right and alist[right]>=value:right = right-1
        if right>left:
            alist[left],alist[right] = alist[right],alist[left]
        else:flag=0
    alist[0],alist[right] = alist[right],alist[0]
    return right

if __name__ == "__main__":
    alist = [7,3,15,84,59,12,46,73]
    QuickSort(alist,0,len(alist)-1)


	
	# __author__ = 'hadoop'
#coding :utf-8
def QuickSort(alist,start,end):
   if start < end:
        loc = HelpQuickSort(alist,start,end)
        # loc2= loc
        QuickSort(alist,start,loc-1)
        QuickSort(alist,loc+1,end)

def HelpQuickSort(alist,first,end):

    value = alist[first]
    start=first+1
    # end=len(alist)-1
    left = start
    right = end;flag=1
    while flag:
        while left<right and alist[left]<value:left = left+1
        while left<right and alist[right]>value:right = right-1
        if right>left:
            alist[left],alist[right] = alist[right],alist[left]
        else:flag=0
    alist[first],alist[right] = alist[right],alist[first]
    return right
if __name__ == "__main__":
    alist = [25,3,15,84,59,12,46,73]
    QuickSort(alist,0,len(alist)-1)
    print (alist)
	
	
	
	
__author__ = 'hadoop'
def BubbleSort(alist,start,end):
    L=end-start
    while L>=0:
        for i in range(L):
            if alist[i]>alist[i+1]:
                alist[i],alist[i+1]=alist[i+1],alist[i]
        L=L-1
alist=[3,6,4,1,9,10,2,8]
BubbleSort(alist,0,len(alist)-1)
print (alist)

#coding :utf-8
# a=[0]*10
# a[0]=1
# a[1]=2
# for i in xrange(2,10,1):
#     a[i]=a[i-1]+a[i-2]
# print a

# def f(n):
#     while n>0:
#         if n==1:return 1
#         if n==2:return 2
#         return f(n-1)+f(n-2)
# f(30)

#encoding=utf-8
def merge(a, b):
    print ("current merge a:{},b:{}".format(a,b))
    c = []
    h = j = 0
    while j < len(a) and h < len(b):
        if a[j] < b[h]:
            c.append(a[j])
            j += 1
        else:
            c.append(b[h])
            h += 1

    if j == len(a):
        for i in b[h:]:
            c.append(i)# append 是因为已经排好序了，和quick sort 不同是引入第三个变量中转，
    else:
        for i in a[j:]:
            c.append(i)
    print (" merge result:{}".format(c))

    return c


def merge_sort(lists):
    print("current list:",lists)
    if len(lists) <= 1:
        return lists
    middle = len(lists)/2
    left = merge_sort(lists[:middle])
    right = merge_sort(lists[middle:])
    return merge(left, right)

def quick_sort(a):
    if len(a)<2:#!!!!!!!
        return a
    mid=a[0]
    left=[x for x in a[1:] if x<=mid]
    right=[x for x in a[1:] if x>mid]
    return quick_sort(left)+[mid]+quick_sort(right)


a=[2,1,4,3,5,6]
print(quick_sort(a))


if __name__ == '__main__':
    a = [4, 7, 8, 3, 5, 9]
    print (merge_sort(a))