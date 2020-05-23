import abc
from cStringIO import StringIO

"""1.抽象类概念

抽象类是一个特殊的类，只能被继承，不能实例化

2.为什么要有抽象类

其实在未接触抽象类概念时，我们可以构造香蕉、苹果、梨之类的类，然后让它们继承水果这个的基类，水果的基类包含一个eat函数。

但是你有没有想过，我们可以将香蕉、苹果、梨实例化，去吃香蕉、苹果、梨。但是我们却不能将水果实例化，因为我们无法吃到叫水果的这个东西。

所以抽象类中只能有抽象方法（没有实现功能），该类不能被实例化，只能被继承，且子类必须实现抽象方法。

3.抽象类的作用

在不同的模块中通过抽象基类来调用，可以用最精简的方式展示出代码之间的逻辑关系，让模块之间的依赖清晰简单。

抽象类的编程，让每个人可以关注当前抽象类的方法和描述，而不需要考虑过多的实现细节，这对协同开发有很大意义，也让代码可读性更高。
abc模块在Python2&3的兼容问题

为解决兼容性问题，我们需要引入six模块

作者：蝴蝶刀刀
链接：http://www.imooc.com/article/74245
来源：慕课网

"""
class Company(object):
    def __init__(self,emplyee_list):
        self.emplyee=emplyee_list
    def __len__(self):
        return len(self.emplyee)

com=Company(['a','b','c'])
print(com.__len__())

# class ABCWithConcreteImplementation(object):
#     __metaclass__ = abc.ABCMeta
#
#     @abc.abstractmethod
#     def retrieve_values(self, input):
#         print
#         'base class reading data'
#         return input.read()
#
#
# class ConcreteOverride(ABCWithConcreteImplementation):
#
#     def retrieve_values(self, input):
#         base_data = super(ConcreteOverride, self).retrieve_values(input)
#         print
#         'subclass sorting data'
#         response = sorted(base_data.splitlines())
#         return response
#
# if __name__=="__main__":
#     input = StringIO("""line one
#     line two
#     line three
#     """)
#
#     reader = ConcreteOverride()
#     print
#     reader.retrieve_values(input)
#     print