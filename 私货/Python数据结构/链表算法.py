"""
python链表算法
Created by 陈 英锐 on 2024/8/17
Updated on 2024/8/17
"""


class Node:
    def __init__(self):
        self.data = None
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def traverse(self):
        cur = self.head
        while cur is not None:
            print(cur.data)
            cur = cur.next

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

    def add_sort_node(self, data):
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

    def delete_node(self, data):
        if self.head is None:
            return False
        if self.head.data == data:
            self.head = self.head.next
            return self.head
        else:
            cur = self.head
            while cur.next is not None:
                if cur.next.data == data:
                    cur.next = cur.next.next
                    break
                cur = cur.next

    def find_max_data(self):
        if self.head is None:
            return False
        else:
            cur = self.head
            max_data = 0
            while cur is not None:
                max_data = max(max_data, cur.data)
                cur = cur.next
            return max_data


# 插入排序
def insertion_sort(ls):
    new_list = LinkedList()
    cur = ls.head
    while cur is not None:
        new_list.add_sort_node(cur.data)
        cur = cur.next
    return new_list


# 选择排序
def select_sort(ls):
    new_list = LinkedList()
    while ls.head is not None:
        max_num = ls.find_max_data()
        new_list.add_node_to_tail(max_num)
        ls.delete_node(max_num)
    return new_list
