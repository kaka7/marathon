class tree_node(object):
    def __init__(self,data,left=None,right=None):
        self.node_data=data
        self.node_left=left
        self.node_right=right
class bin_tree():
    def __init__(self,root):
        self.tree_root=root
        self.tree2list=[]
    def pre_print(self,root):#（1）访问根节点；（2）采用先序递归遍历左子树；（3）采用先序递归遍历右子树；
        if root !=None:
            data=root.node_data
            print(data, end="")
            self.pre_print(root.node_left)
            self.pre_print(root.node_right)
        else:
            pass
            # print("None")
    def pre_print2(self,root): #非递归　堆　广度优先 递归的艘可以用非递归表示，递归只是用了程序的栈
        if not root:
            return
        stack=[root]
        res=[]
        while stack:#精髓
            cur_node=stack.pop()
            res.append(cur_node.node_data)
            if cur_node.node_right:
                stack.append(cur_node.node_right)
            if cur_node.node_left:
                stack.append(cur_node.node_left)
        print(res)
        return res

    def mid_print(self,root):
        if root !=None:
            self.mid_print(root.node_left)
            print(root.node_data, end="")
            self.mid_print(root.node_right)
    def mid_print2(self,root):
        if not root:
            return
        stack=[]
        stack.append(root)
        cur_node=root#初始化迭代很重要
        while stack:
            if cur_node.node_left:#左右可能同时有数　二者是不是互斥的？？？
                stack.append(cur_node.node_left)
                cur_node=cur_node.node_left
            else:
                cur_node=stack.pop()
                print(cur_node.node_data,end="")
                if cur_node.node_right:
                    stack.append(cur_node.node_right)
                    cur_node=cur_node.node_right


    def get_kth_ele(self,root):
        if root !=None:
            self.get_kth_ele(root.node_left)
            self.tree2list.append(root.node_data)
            self.get_kth_ele(root.node_right)

    def post_print(self,root):
        if root !=None:
            self.post_print(root.node_left)
            self.post_print(root.node_right)
            print(root.node_data, end="")
    # def post_print2(self,root): #栈　深度优先　队列　广度优先 #???难度大　todo
    #     if not root:
    #         return
    #     queue=[root]
    #     res=[]
    #     cur_node=root
    #     while queue:#精髓
    #         if cur_node.node_left:
    #             queue.append(cur_node.node_left)
    #         cur_node = queue.pop()
    #         res.append(cur_node.node_data)
    #         if cur_node.node_right:
    #             queue.append(cur_node.node_right)
    #     print(res)
    #     return res
    def post_print2(self,root):
        if not root:
            return
        stack=[]
        stack2=[]
        stack.append(root)
        # cur_node=root#初始化迭代很重要
        while stack:
            cur_node=stack.pop()
            stack2.append(cur_node)

            if cur_node.node_left:
                stack.append(cur_node.node_left)
                # cur_node=cur_node.node_left
            else:
                pass
            if cur_node.node_right:
                stack.append(cur_node.node_right)
                # cur_node=cur_node.node_right
            else:
                pass
                # stack2.append(stack.pop())
                # print(cur_node.node_data, end="")
        while stack2:
            print(stack2.pop().node_data,end="")


    def get_deepth(self,root,deepth=0):
        if root !=None:
            deepth+=1
            d1=self.get_deepth(root.node_left,deepth)
            d2 = self.get_deepth(root.node_right, deepth)
            return d1 if d1>d2 else d2
        else:return deepth
    def get_leaf_num(self,root):#todo 仿照获取树深度来写
        if root!=None:
            if root.node_left == None and root.node_right == None:
                return 1
            elif root.node_left != None and root.node_right == None:#1
                return self.get_leaf_num(root.node_left)
            elif root.node_left == None and root.node_right != None:#2 如果没有1 和２　n2或n1可能有一个为空
                return self.get_leaf_num(root.node_right)
            else:
            # num=1
                n1=self.get_leaf_num(root.node_left)
                n2=self.get_leaf_num(root.node_right)
                return n1+n2
    def exchange_leaf_node(self,root):#函数内的函数
        def __exchange_node(root):
            if root!=None:
                root.node_left,root.node_right=root.node_right,root.node_left

                if root.node_left!=None or root.node_right!=None:
                    __exchange_node(root.node_left)
                    __exchange_node(root.node_right)
            else: return
        __exchange_node(root)
        print("done")
    def printBylevel(self,root):#广度优先 queue
        """
        cur_data==cur_last cur_last=nlast queue!=null
        :param root: obj node
        :return:
        """
        if root.node_data==None:
            return # 空
        queue=[]
        queue.append(root)#迭代对象
        i=1
        cur_last=root.node_data#初始化
        print("level {}:".format(i))
        while len(queue):
            cur_node=queue.pop(0)
            cur_data=cur_node.node_data
            print(cur_data,end="")#fifo
            if cur_node.node_left!= None:
                nlast=cur_node.node_left.node_data
                queue.append(cur_node.node_left)#fifo
                # root=root.node_left
            if cur_node.node_right!= None:
                nlast=cur_node.node_right.node_data
                queue.append(cur_node.node_right)
                # root=root.node_right
            if cur_data==cur_last and queue:
                i+=1
                cur_last=nlast
                print()
                print("level {}:".format(i),end="")
    def printBylevel2(self,root):
        res=[]#存放结果
        temp=[]#存放每一层的结果,下一层时清空
        layer_queue=[]#将只要当前节点的子节点不为空就顺序的放到队列末尾,如果当前节点走到了当前层的末尾,则说明这一层走完了
        cur_layer_end=root
        layer_queue.append(root)
        while(len(layer_queue)):
            cur_node = layer_queue[0]#当前节点总是指向队列首
            print("cur:",cur_node.node_data)
            temp.append(layer_queue.pop(0).node_data)#弹出当前节点
            if cur_node.node_left:#
                layer_queue.append(cur_node.node_left)
                next_layer_end=cur_node.node_left#更新当前节点
            if cur_node.node_right:
                layer_queue.append(cur_node.node_right)
                next_layer_end=cur_node.node_right

            if cur_node==cur_layer_end and len(layer_queue):#到了层尾
                res.append(temp)
                temp=[]#下一层时清空
                cur_layer_end=next_layer_end#更新cur_layer_end
        res.append(temp)#最后的结果
        print("\nhello")
        for i,x in enumerate(res):
            print(i,":",x)
        layer_queue.__len__()





    def get_node(self,root):#递归 递归的结果一定要赋值给一个变量
        if not root:
            return
        List=[root.node_data]#叶子节点是一个单独的[]形式
        if root.node_left:
            List.append(self.get_node(root.node_left))#深度优先 stack
        if root.node_right:
            List.append(self.get_node(root.node_right))
        return List
    def get_node2(self,root):#非递归???
        pass #todo


    def find_common_ancestor(self, root, a, b):
        if root == None or a == None or b == None: return None
        # if root==None || a==root || b==None:return root
        left = self.find_common_ancestor(root.left, a, b)
        right = self.find_common_ancestor(root.right, a, b)

        if left == None:  # 只找到一个就只返回另一边的，然后继续找
            return right
        elif right == None:
            return left
        else:  # 左右分别包含a,b，所以root即使祖先
            return root.data
# find_common_ancestor(root,1,3)

node1=tree_node(2,tree_node(1),tree_node(3))#不能是　node1=tree_node(2,１,３)　保证每个叶子都是Ｎｏｎｅ

node2=tree_node(6,tree_node(5),tree_node(7))
# node3=tree_node(5,node1)
# node4=tree_node(6,node2)
node=tree_node(4,node1,node2)

# node=tree_node(4,tree_node(2))
bin_tree=bin_tree(node)
root=bin_tree.tree_root

# print("\n先序\n")
# bin_tree.pre_print(root)
# bin_tree.pre_print2(root)
# print("\n中序\n")
# bin_tree.mid_print(root)
# print()
# bin_tree.mid_print2(root)

print("\n后序\n")
bin_tree.post_print(root)
print()
bin_tree.post_print2(root)
#
# bin_tree.get_kth_ele(root)
# print(bin_tree.tree2list[3])

# print("\n")
# deep=bin_tree.get_deepth(root,0)
# print("deepth:{}\n".format(deep))
# num_leaf=bin_tree.get_leaf_num(root)
# print("leaf num:{}\n".format(num_leaf))
#
# bin_tree.exchange_leaf_node(root)
# root=bin_tree.tree_root
# print("\n先序\n")
# bin_tree.pre_print(root)
# print("\n中序\n")
# bin_tree.mid_print(root)
# print("\n后序\n")
# bin_tree.post_print(root)
# print("\n")

bin_tree.printBylevel(root)
bin_tree.printBylevel2(root)

# print(bin_tree.get_node(root))
# print(bin_tree.get_node2(root))







###########################################################

# class BinTree():
#     def __init__(self,data_list):
#         # self.it=iter(data_list) #list 需要判断长度　iter　直接next
#         self.it=data_list
#         self.deepth=0
#         self.List=[]


# def create_tree(self,bt=None):
#     try:
#         next_data=next(self.it)
#         if next_data is "#":
#             bt = None
#         else :
#             bt=TreeNode(next_data) #树叶子节点一定要有none
#             print(next_data)
#             bt.node_left=self.create_tree()#非平衡的二叉树，全部集中在左节点
#             bt.node_right=self.create_tree()
#     except Exception as e:
#         print(e)
#     else:#和try结合，并非一样，如果ｔｒｙ执行成功才执行ｅｌｓｅ
#         # print("no except")
#         pass
#
#     finally:
#         return bt


# def printTreeNode(self,root):
#     def printNode(root):
#         if root.node_data==None:
#             return
#         else:
#             self.List.expand(root.node_data)
#         if
#     if root.node_data:self.List.expand(root.node_data)
#     while self.List:
#         if len(self.List)==0:
#             return
#         elif len(self.List)==1:
#             print(self.List.pop(),"\n")
#         else:
#             self.List.insert(0,root.node_left)
#             self.List.insert(0,root.node_right)


# while True:
#     yield
# next


# 问题　数据流中的中位数，判断奇数长度和偶数长度
