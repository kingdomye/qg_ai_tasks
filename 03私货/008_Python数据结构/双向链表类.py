"""
双向链表类py
Created by ricckker on 2024/8/16
Updated on 2024/8/16
"""


class Node:
    def __init__(self):
        self.data = None
        self.next = None
        self.prev = None


class DoubleLinkedList:
    def __init__(self):
        self.head = None

    def add_node_to_head(self, data):
        new_node = Node()
        new_node.data = data

        if self.head is None:
            self.head = new_node
        else:
            self.head.prev = new_node
            new_node.next = self.head

    def add_node_to_tail(self, data):
        new_node = Node()
        new_node.data = data
        if self.head is None:
            self.head = new_node
        else:
            cur = self.head
            while cur.next is not None:
                cur = cur.next
            cur.next = new_node
            new_node.prev = cur

    def traverse(self):
        cur = self.head
        while cur is not None:
            print(cur.data)
            cur = cur.next
