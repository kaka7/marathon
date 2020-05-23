#encoding=utf-8
"""
-------------------------------------------------
   File Name：     090603linklistReverse
   Description :
   Author :       naruto
   date：          6/3/19
-------------------------------------------------
   Change Activity:
                   6/3/19:
-------------------------------------------------
"""
__author__ = 'naruto'

class linkNode(object):
    def __init__(self,data=None):
        self.data=data
        self.next=None
    def insert(self,data):
        self.next=data

def linklistReverse(head):
    new_linkList=None #每次都将原有的ｌｉｎｋ通过ｐ切断得到一个新的节点，然后再指向new_linkList
    if  not head or not head.next:
        return head
    # head1=head
    # else:
    # new_linkList=new_linkList
    while head:
        p=head# p 临时指针，每次都指向头 ｐ是当前需要操作的节点所以翻转就是将当前节点的next指向之前已经反转好的节点链表　对应第三步

        head=head.next #移动头指针 不能移动到最后！！！　否则下一步机会使head为none ；head被截断

        p.next=new_linkList #反转，然后就形成新的ｌｉｎｋ　＃ｐ被截断　p.next
        new_linkList=p #p不是一个　是一个地址的开始，所以可以这样　将最新的翻转好的赋值

    return new_linkList
def reverse_link_by_stack(link):
    new_l=[]
    while link!=None:
        new_l.append(link.data)#todo error
        link=link.next
    print(new_l)

def print_linklist(link):
    while link != None:  # link.data!=None or
        print(link.data)
        link = link.next
def find_kth_tail(link,k):
    #倒数第K个即为正数n-k,常规是找到长度n,然后求n-k个元素(也可反向链表,然后求第k个),复杂度是o(n+k)
    高级方法:快慢指针,快的走k-1,然后再一起走,最后当快的走完,慢的就走了n-k+1 复杂度是o(n)
    if k<0 or link==None:
        return None
    fast,slow=link,link
    for i in range(1,k):
        if fast.next:
            fast=fast.next
        else :
            return None
    while fast.next:
        fast=fast.next
        slow=slow.next
    return slow.data
def merge2link(link1,link2):#合并两个有序链表
    if not link1 :
        return link2
    elif not link2:
        return link1
    else:
        new_l=linkNode()
        tmp=new_l
        while link1 and link2:#link1 不为null则对应的data也不为None
            # if link1.data and link2.data:
            if link1.data<link2.data:
                tmp.next=linkNode(link1.data)
                tmp=tmp.next
                link1=link1.next
            else:
                tmp.next=linkNode(link2.data)
                tmp=tmp.next
                link2=link2.next
        while link2:
            tmp.next=linkNode(link2.data)
            tmp = tmp.next
            link2 = link2.next
        while link1:
            tmp.next=linkNode(link1.data)
            tmp = tmp.next
            link1 = link1.next

    return new_l

    pass
def delete_same_node(link):
    new_=linkNode()
    tmp=new_#一定要有这个指针
    if not link:
        return None
    while link:
        pre=link.data#
        if not link.next:#由于这里需要获取当前节点的下一个节点，如果没有说明到了末尾，所以此时直接返回
            tmp.next = linkNode(pre)
            return new_
        link=link.next
        if pre!=link.data and pre!=None:
            tmp.next=linkNode(pre)
            tmp=tmp.next
            pre=link.data
        else:
            link = link.next #跳过下一个节点
            pre=None

    return new_
def find_loop_linklist_entry(root):#todo error
    """
    找环的中间位置
    倒数第ｋ个节点
    :param root:
    :return:
    """
    if not root:
        return None
    slow=root
    fast=root.next.next
    count=0
    while slow.data!=fast.data:
        count+=1
        if fast.next==None or fast.next.next:#没有环
            return None
        slow = slow.next
        fast = fast.next.next

    slow = root
    while slow.data!=fast.data:
        slow = slow.next
        fast = fast.next
        # if slow.data==fast.data:
    return slow
    # for i in range(count+1):
    #     slow = slow.next
    #     fast = fast.next
    #     if slow.data==fast.data:
    #         return slow






# 复制复杂链表
# 找到两个链表的第一个公共节点
# 链表回文，栈翻转，一半栈翻转，





if __name__=="__main__":
    #初始化
    l=[0,1,3,5,7,1,3,5,7]

    # l=[1,3,5,7,9,13,5,15]
    link=linkNode(l[0])
    tmp_link=link #next 也是对象，
    for i in l[1:]:
        tmp_link.next=linkNode(i)
        tmp_link=tmp_link.next
    print_linklist(link)

    # #反转
    tmp_link=link

    # new_l=linklistReverse(tmp_link)
    # tmp_link=new_l
    # #打印
    # print_linklist(tmp_link)

    # reverse_link_by_stack(tmp_link)

    #尾部第ｋ个节点
    # tmp_link=link
    # print(find_kth_tail(tmp_link,2))

# 　　 删除重复的节点
#     tmp_link=link
#     tmp_link=delete_same_node(tmp_link)
#     print_linklist(tmp_link)

    # # 合并两个链表
    # l=[2,4,6,8]
    # link1=linkNode(l[0])
    # tmp_link=link1 #next 也是对象，
    # for i in l[1:]:
    #     tmp_link.next=linkNode(i)
    #     tmp_link=tmp_link.next
    #
    # print_linklist(merge2link(link,link1))

    result=find_loop_linklist_entry(tmp_link)
    if result:
        print(result.data)
    else:
        print(None)




