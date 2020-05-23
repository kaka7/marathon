import time,random
import queue,threading

q = queue.Queue()

exitFlag = 1

def Producer(name):
  global count
  # while count <10:
  while True and exitFlag:
    print("制造包子ing")
    time.sleep(1)
    q.put(count)
    print('生产者 %s 生产了 %s 包子..' %(name, count))
    count +=1
    #q.task_done()
    #q.join()

def Consumer(name):

    # time.sleep(1)#random.randrange(1)
    count = 0
    while True:
        time.sleep(1)

        # while count <10:
        if (not q.empty() and exitFlag):
            data = q.get()
            #q.task_done()
            #q.join()
            print(data)
            print('消费者 %s 消费了 %s 包子...' %(name, data))
            print("cur queue size {}:".format(q.qsize()))

        else:
            print("包子吃完了")
            count+=1
if __name__=="__main__":
    c1 = threading.Thread(target=Producer, args=('小明',))
    c2 = threading.Thread(target=Producer, args=('小花',))
    c3 = threading.Thread(target=Consumer, args=('小灰',))
    c1.start()
    c2.start()
    c3.start()

    count=0


    if count>5:
        exitFlag=0

    c1.join()
    c2.join()
    c3.join()

    print('结束')

# # 等待队列清空
# while not workQueue.empty():
#     pass
#
# # 通知线程是时候退出
# exitFlag = 1