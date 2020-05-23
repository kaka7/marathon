
class Solution(object):
    def __init__(self):
        pass
    def find_exit_one_two(self,arr):
        res1=res2=0
        temp=0
        for x in arr:
            temp=temp^x
        print(temp)
        index=0
        for i in range(0,32):
            if (temp>>i)&1==1:#//&1
                index=i
                break

        for x in arr:
            if (x>>index)&1==1:
                res1=res1^x
            else:
                res2=res2^x
        print(res1,res2)
        return res1,res2




arr=[1,3,5,7,1,3,5,9]
arr=[2,4,3,6,3,2,5,5]
Solution().find_exit_one_two(arr)