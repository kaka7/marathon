# -*- coding: utf-8 -*-
#*y truple **b dict
# array * - 对应操作
# >>> a = np.ones((2,2))
# >>> b = np.eye(2)
# >>> print np.vstack((a,b))
# [[ 1.  1.]
#  [ 1.  1.]
#  [ 1.  0.]
#  [ 0.  1.]]
# >>> print np.hstack((a,b))
# [[ 1.  1.  1.  0.]
#  [ 1.  1.  0.  1.]]
# print a.transpose()

# class Dog:
#     kind = 'canine'         # class variable shared by all instances
#     def __init__(self, name):
#         self.name = name    # instance variable unique to each instance

import numpy as np
from compiler.ast import flatten
def Sigmod(x):
    return 1.0/(1+np.exp(-x))#not math
def Dsigmod(x):
    # return Sigmod(x)*(1-Sigmod(x)) this need to be recalled ,not good
    return x*(1-x)#because the output of every layer is the result of active function
def Tanh(x):
    return np.tanh(x)
def Dtanh(x):
    return 1-x^2 #1-x**2
class feed_everylayer_params():
    def __init__(self, weights, bia,num,func,index):
        self.num=num
        self.func = func
        self.ind=index
        self.w=weights
        self.b=bia
        self.name=None

class model_structure_param_init():
    def __init__(self, every_layer_neural_num_lists,every_layer_active_func_lists):
        every_layer_neural_num_lists_flat_flat=flatten(every_layer_neural_num_lists)
        self.every_layer_neural_num_lists_flat=every_layer_neural_num_lists_flat_flat#每一层的神经元个数
        self.every_layer_active_func_lists =every_layer_active_func_lists
        self.sample_num=4
        self.input_dim=2
        self.output_dim=1

    # def initcoeff(self):
        # self.every_layer_active_func_lists=self.every_layer_active_func_lists.append('line')#覆盖内容
        self.model_layers_param_lists=[]
        for i, neural_num in enumerate(self.every_layer_neural_num_lists_flat):
            if i==0:
                self.model_layers_param_lists.append(feed_everylayer_params([],[],neural_num,'none',i))
            else:
                last=self.every_layer_neural_num_lists_flat[i-1]
                current=self.every_layer_neural_num_lists_flat[i]
                self.model_layers_param_lists.append(feed_everylayer_params(np.random.randn(self.sample_num,last,current),np.random.randn(self.sample_num,self.output_dim,current),neural_num,self.every_layer_active_func_lists[i-1],i))#every_layer_neural_num_lists[i-1]
        # if isinstance(every_layer_active_func_lists[1],list):
class model():
    def __init__(self,model_struct_param_init, itertimes =100, mul=0.01,tolerance=0.02,):
        self.model_struct_param_init = model_struct_param_init
        self.itertimes = itertimes
        self.mul = mul
        self.tolerance = tolerance
    def forward(self,x,y):
        self.model_struct_param_init.x=np.array(x)
        self.model_struct_param_init.y=np.array(y)
        self.model_layer_num=len(self.model_struct_param_init.every_layer_active_func_lists)
        for i in range(self.model_layer_num):
            if i == 0:
                cur_layer = self.model_struct_param_init.model_layers_param_lists[i]#laysNSneuralparam 是個列表型對象
                cur_layer.input = self.model_struct_param_init.x
                cur_layer.output = self.model_struct_param_init.x
                continue
            last_layer = self.model_struct_param_init.model_layers_param_lists[i-1]
            cur_layer = self.model_struct_param_init.model_layers_param_lists[i]
            cur_layer.input = last_layer.input.dot(cur_layer.w)+cur_layer.b
            # cur_layer.input = np.array(last_layers.input)*np.array(cur_layer.w)+np.array(cur_layer.b)
            # print ("h",cur_layer.input, "b",self.model_struct_param_init.NSevery_layer_neural_num_lists[i-1])
            cur_layer.output = self.actfunc(cur_layer.input, self.model_struct_param_init.every_layer_active_func_lists[i-1])
        self.forward_output=cur_layer.output
        # print ("current_layser output:",self,cur_layer.output)
    def train(self):
        y_=self.model_struct_param_init.y
        predict=self.forward_output
        print(np.shape(predict))
        error=(predict.T-y_)
        tol=self.tolerance
        print ("sumerror:", abs(np.sum(error, axis=1)) / len(y_))
        for i in range(self.itertimes):
            if np.array(abs(np.sum(error,axis=1))/len(y_)).all() < tol:
                print "hellO"
                break
            self.backpropagation()
    def backpropagation(self):
        num_layers=self.model_layer_num
        # print("print:",range(2,num_layers),list(range(2,num_layers)).reverse())
        # index=list(range(2,num_layers))
        # print (index,"index")
        # index=index.reverse()
        for i in range(num_layers-1,1,-1):
        # for i in list(range(2,self.model_layer_num).reverse()):
            llast_layer=self.model_struct_param_init.model_layers_param_lists[i-2]
            last_layer = self.model_struct_param_init.model_layers_param_lists[i-1]
            curr_layer = self.model_struct_param_init.model_layers_param_lists[i]
            if i ==5:
                # print("self.model_struct_param_init.y.T:",self.forward_output.shape,np.reshape(self.model_struct_param_init.y,(1,4)).transpose())
                layererror=self.forward_output-np.reshape(self.model_struct_param_init.y,(len(self.model_struct_param_init.y),1))#
                # delta=layererror*self.actfuncgrad(curr_layer.input,curr_layer.func)
                # print ("param:",curr_layer.input,self.model_struct_param_init.laysNSneuralparam[i].func,curr_layer.func)
                # print("curr_layer.input:",curr_layer.input,type(curr_layer.input))
                # print("param",self.model_struct_param_init.laysNSneuralparam[i].func,type(self.model_struct_param_init.laysNSneuralparam[i].func))
                #4X1,
                act=model.actfuncgrad(np.array(curr_layer.input),self.model_struct_param_init.laysNSneuralparam[i].func)
                #4X1
                delta = layererror*(model.actfuncgrad(np.array(curr_layer.input),self.model_struct_param_init.laysNSneuralparam[i].func))

                # print("self.mul*delta",self.mul*delta)
                # print ("shape:",NN.model_struct_param_init.laysNSneuralparam[i-1].w.shape)
                # delta = np.array(layererror).T*(self.actfuncgrad(np.array(curr_layer.input.T),self.model_struct_param_init.laysNSneuralparam[i].func))
                model.model_struct_param_init.laysNSneuralparam[i-1].w-=self.mul*delta*last_layer.output
                self.model_struct_param_init.laysNSneuralparam[i-1].b-=self.mul*delta
                continue
            # last_layererror=self.model_struct_param_init.laysNSneuralparam[i].w*layererror
            delta = layererror * self.actfuncgrad(curr_layer.input,self.model_struct_param_init.laysNSneuralparam[i].func)
            self.model_struct_param_init.laysNSneuralparam[i-1].w -= self.mul * delta*self.model_struct_param_init.laysNSneuralparam[i].w\
                                                       *self.actfuncgrad(curr_layer.input,curr_layer.func)*last_layer.output
            self.model_struct_param_init.laysNSneuralparam[i-1].b -= self.mul * delta*self.model_struct_param_init.laysNSneuralparam[i].w\
                                                       *self.actfuncgrad(curr_layer.input,curr_layer.func)



    def actfunc(self, input,func="sigmod"):

        # def actfunc(self,input,func="sigmod"):
        # print "func:",func

        if func=="sigmod":
            return Sigmod(input)
        elif func == "line":
            return input
        elif func == "dtanh":
            return Tanh(input)

    def actfuncgrad(self,input,func):
        # print ("input:",input)
        # print("func:",func)
        x=self.actfunc(input,func)
        # x=self.actfunc(self.input,func)
        # x=NN.actfunc(self.input,func)


        if func=="sigmod":
            return Dsigmod(x)
        elif func=="tanh":
            return Dtanh(x)
        elif func=="line":
            return x

if __name__=="__main__":
    datas=[[0,0],[0,1],[1,0],[1,1]]
    lables=[0,0,0,1]
    every_layer_active_func_lists=['sigmod','sigmod','sigmod','sigmod','line']#sigmod
    every_layer_neural_num_lists=[2, [5, 5, 5, 5], 1]
    model_params=model_structure_param_init(every_layer_neural_num_lists, every_layer_active_func_lists)
    model=model(model_params)
    # for x,y in zip(data,lable):
    model.forward(datas, lables)
    model.train()
    pass

