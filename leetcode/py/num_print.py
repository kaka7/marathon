def check(arr):
    cout=[]
    out=[]
    if len(arr) <= 1:
        cout=[arr]
    else:
        temp = []
        temp.append(arr[0])
        for i in range(1, len(arr)):
            a=arr[i]
            temp.append(arr[i])
            if arr[i]-arr[i-1]!=1:
                temp=temp[:-1]
                cout.append(temp)
                temp=[arr[i]]
            if i==len(arr)-1:
                cout.append(temp)

    for x in cout:
        if(len(x)==1):
            out.append(str(x[0]))
        else:
            out.append(str(x[0])+"-"+str(x[-1]))

    return out
if __name__ == '__main__':
    arr=[1,2,3,4,6,8,9,10]
    print("please input arr with sep=,\n")
    arr=input()
    arr=[int(x) for x in arr.split(",")]
    print(check(arr))




