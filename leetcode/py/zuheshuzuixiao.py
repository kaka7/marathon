# #输入一个正整数数组，把数组里所有数字拼接起来排成一个数，打印能拼接出的所有数字中最小的一个。例如输入数组{3，32，321}，则打印出这三个数字能排成的最小数字为321323。
# # -*- coding:utf-8 -*-
#
# class Solution(object):
#     def PrintMinNumber(self, numbers):
#         numbers=[str(x) for x in numbers]
#         min_bit=min([int(x[0]) for x in numbers])
#         min_num=[x for x in numbers if (x[0]==min_bit)]
#         # list.remove()
#         if len(min_num)>1:
#
#             pass
#
#         else:
#             pass
#         numbers.remove(min_num[0])
#         return min_num[0]+self.PrintMinNumber(numbers)
#
#     def helper(self,numbers):
#
#         pass
#
#
#         # write code here
# # if __name__="__main__":
#
#
#  # list.pop()

# def count1(x):
#     if(x==0):
#         return 0
#     count=0
#     while(x):
#         count=count+1
#         x=x&(x-1)
#     return count
# print(count1(2))
print(count1(number))



