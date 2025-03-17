"""
python自组织链表类
Created by 陈 英锐 on 2024/8/17
Updated on 2024/8/17
"""


class Node:
    def __init__(self):
        self.data = None
        self.next = None


class SelfOrganizeLinkedList:
    def __init__(self):
        self.head = None

    def add_node(self, data):
        new_node = Node()
        new_node.data = data
        if self.head is None:
            self.head = new_node
        else:
            new_node.next = self.head
            self.head = new_node

    def traverse(self):
        cur = self.head
        while cur is not None:
            print(cur.data)
            cur = cur.next

    # 前移方法
    def move_to_front(self, data):
        if self.head is None:
            return False
        else:
            pre = self.head
            cur = self.head.next
            while cur is not None:
                if cur.data == data:
                    pre.next = cur.next
                    cur.next = self.head
                    self.head = cur
                    break
                cur = cur.next
                pre = pre.next

    # 交换方法
    def swap_with_front(self, data):
        if self.head is None:
            return False
        else:
            pre = self.head
            cur = self.head.next
            while cur is not None:
                if cur.data == data:
                    cur.data, pre.data = pre.data, cur.data
                    break
                cur = cur.next
                pre = pre.next


mylist = SelfOrganizeLinkedList()
mylist.add_node(3)
mylist.add_node(2)
mylist.add_node(1)
mylist.traverse()
