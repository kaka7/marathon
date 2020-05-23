
# max(a[l:r])<min(b[l:r])

# printf(tf.__version__)

def max_min(a,b):
    assert len(a)==len(b)
    l_len=len(a)
    assert l_len>0
    count=0
    # q_a=[a[0]]
    # q_b=[b[0]]
    # if a[0]<q_b[-1]: count+=1
    for i in range(l_len+1):
        # q_a.pop(0)
        # q_b.pop(0)

        for j in range(i+1,l_len+1):
            if max(a[i:j])<min(b[i:j]):
                count+=1
    print("max less min :",count)
a=[0,1,2,3]
b=[4,5,6,7]
max_min(a,b)