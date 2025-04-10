"""
python有序链表类
Created by 陈 英锐 on 2024/8/17
Updated on 2024/8/17
"""


class Node:
    def __init__(self):
        self.data = None
        self.next = None


class SortedLinkedList:
    def __init__(self):
        self.head = None

    def add_node(self, data):
        new_node = Node()
        new_node.data = data
        if self.head is None:
            self.head = new_node
        else:
            cur = self.head
            if data <= cur.data:
                new_node.next = cur
                self.head = new_node
            else:
                while cur.next is not None and cur.next.data <= data:
                    cur = cur.next
                new_node.next = cur.next
                cur.next = new_node


    def traverse(self):
        cur = self.head
        while cur is not None:
            print(cur.data)
            cur = cur.next


mylist = SortedLinkedList()
mylist.add_node(2)
mylist.add_node(1)
mylist.add_node(3)
mylist.traverse()
        