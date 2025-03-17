"""
单向链表类py
Created by ricckker on 2024/8/15
Updated on 2024/8/16
"""


# 链表节点类
class Node:
    def __init__(self):
        self.val = None
        self.next = None


# 链表类
class LinkedList:
    def __init__(self):
        self.head = None

    # 遍历链表
    def traverse(self):
        cur = self.head
        while cur is not None:
            print(cur.val)
            cur = cur.next

    # 查找节点
    def find_node(self, val):
        cur = self.head
        while cur is not None:
            if cur.val == val:
                return cur
            cur = cur.next
        return None

    # 顶部添加节点
    def add_node_to_head(self, val):
        new_node = Node()
        new_node.val = val

        if self.head is None:
            self.head = new_node
        else:
            new_node.next = self.head
            self.head = new_node

    # 尾部添加节点
    def add_node_to_tail(self, val):
        new_node = Node()
        new_node.val = val

        if self.head is None:
            self.head = new_node
        else:
            cur = self.head
            while cur.next is not None:
                cur = cur.next
            cur.next = new_node

    # 在指定节点后添加节点
    def add_node_after(self, target, val):
        new_node = Node()
        new_node.val = val

        if self.head is None:
            self.head = new_node
        else:
            cur = self.head
            while cur is not None:
                if cur.val == target:
                    new_node.next = cur.next
                    cur.next = new_node
                    break
                cur = cur.next

    # 删除节点
    def delete_node(self, val):
        if self.head is None:
            return None
        if self.head.val == val:
            self.head = self.head.next
            return self.head
        else:
            cur = self.head
            while cur.next is not None:
                if cur.next.val == val:
                    cur.next = cur.next.next
                    break
                cur = cur.next
            return self.head


if __name__ == '__main__':
    new_list = LinkedList()
    new_list.add_node_to_head(3)

