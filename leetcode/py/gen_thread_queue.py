# !/usr/bin/python
# -*- coding: UTF-8 -*-
from queue import Queue
from threading import Thread
import threading

def add_1(l,q):
    print("cur thread {}, result {}".format(l+1,threading.current_thread()))
    # print(threading.enumerate())
    q.put(l+1)
def gen_random_num():
    import numpy as np
    while True:
        x=np.random.rand(1)
        # print(x)
        yield x

import time
if __name__=="__main__":
    threads=[]
    q=Queue(-1)
    for i in  range(6):
    # while True:
        t=Thread(target=add_1,args=(next(gen_random_num()),q))
        time.sleep(1)
        t.start()
        threads.append(t)
    while not q.empty():
        data=q.get()
        print(data)


