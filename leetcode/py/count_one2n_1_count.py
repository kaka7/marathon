#为此他特别数了一下1~13中包含1的数字有1、10、11、12、13因此共出现6次,但是对于后面问题他就没辙了。ACMer希望你们帮帮他,并把问题更加普遍化,可以很快的求出任意非负整数区间中1出现的次数（从1 到 n 中1出现的次数）。
# zhaochuchongfushuzuiduo
#kdianyouxi
class Solution():
    def NumberOf1Between1AndN_Solution(self, n):
        if(n==0):return 0
        assert(n>=1)
        sum=0
        for x in range(1,n+1):
            sum=sum+self.count_one(x)
        return sum
    def count_one(self,x):

        count=0
        tmp=x
        while(x):
            if(x%10==1):
                count=count+1
            x=x//10
        print(tmp,":",count)
        return count
if __name__=="__main__":
    print(Solution().NumberOf1Between1AndN_Solution(0))