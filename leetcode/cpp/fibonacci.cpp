class Solution {
public:
    int temp;
    int temp1;//由于只需要保存两个,所以也可用队列保存,
    int temp0;
    int sum=0;
    int count=2;
    int Fibonacci(int n) {
        
        temp0=0;
        temp1=1;  
        if(n==0) return temp0;
        if(n==1) return temp1;
        while(count<=n)
        {
            temp=temp1;
            temp1=temp0+temp;
            temp0=temp;
            count++;
        }

        return temp1;

    }
};