# class Test(object):
#     def __init__(self):
#         print("obj created!")
#     def __str__(self):
#         info="call"
#         return info
# a=Test()
# print(str(a))

def test1(a,b):
    c=a+b
    def test2():
        return c
    return test2
test=test1(1,2)
print(test())