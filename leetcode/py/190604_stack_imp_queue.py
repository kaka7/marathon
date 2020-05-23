
class my_queue(object):
    def __init__(self):
        self.stack1=[]
        self.stack2=[]
        self.min_stack=[]
    def queue_push(self,x):
        if not len(self.stack1):
            self.min_stack.append(x)
        else:
            if x<self.min_stack[-1]:
                self.min_stack.insert(0,x)
            else:
                self.min_stack.insert(0,self.min_stack[-1])
        self.stack1.append(x)

    def queue_pop(self):
        if not len(self.stack2):
            while len(self.stack1):
                self.stack2.append(self.stack1.pop())
        print("hello,", self.stack2.pop())
        self.min_stack.pop()
        # else:
        #
        #     print("hello,",self.stack2.pop())
    def get_min(self):
        if len(self.min_stack):
            return self.min_stack[-1]
qu=my_queue()
for x in range(10,1,-1):
    qu.queue_push(x)
for x in range(10):
    qu.queue_pop()
    print(qu.get_min())
