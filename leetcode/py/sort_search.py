#encoding=utf-8
"""
-------------------------------------------------
   File Name：     sort_search
   Description :
   Author :       naruto
   date：          3/7/19
-------------------------------------------------
   Change Activity:
                   3/7/19:
-------------------------------------------------
"""
__author__ = 'naruto'

import os


FLAG = None

import numpy as np
#assert

def quick_sort(a_list):
    if len(a_list)<2:
        return a_list
    random_index=int(np.random.choice(len(a_list),1))
    split_v=a_list[random_index]
    less_list=[x for x in a_list if x <split_v]
    bigger_list=[x for x in a_list if x >split_v]
    return quick_sort(less_list)+[split_v]+quick_sort(bigger_list)


def MyClass():
    def __init__():
        pass


def bin_search(a_list_sorter,to_searched):
    bin_index=len(a_list_sorter) // 2
    bin_v = a_list_sorter[bin_index]
    if bin_v==to_searched:
        print ("searched")
        return
    else:
        if to_searched < bin_v:
            bin_search(a_list_sorter[:bin_index],to_searched)
        else:
            bin_search(a_list_sorter[bin_index+1:],to_searched)



if __name__ == "__main__":
    a_list=[3,7,78,57,42,36,28]
    a_list_sorter=quick_sort(a_list)
    print(a_list_sorter)
    to_searched=78
    bin_search(a_list_sorter,to_searched)

