"""
循环链表类py
Created by ricckker on 2024/8/18
Updated on 2024/8/18
"""


class Node:
    def __init__(self):
        self.data = None
        self.next = None
        self.visited = None


class CircularLinkedList:
    def __init__(self):
        self.head = None

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

    def add_circular_node(self, data):
        new_node = Node()
        new_node.data = data
        if self.head is None:
            self.head = new_node
            self.head.next = self.head
        else:
            cur = self.head
            while cur.next is not self.head:
                cur = cur.next
            cur.next = new_node
            new_node.next = self.head

    # 节点标记法
    def has_loop_marking(self):
        has_loop = False
        cur = self.head
        while cur.next is not None:
            # 断开环路，终止循环
            if cur.next is not None:
                if cur.next.visited:
                    has_loop = True
                    return has_loop
            cur = cur.next
            if cur is not None:
                cur.visited = True

        # 重新遍历链表清除访问标志
        cur = self.head
        while cur.next is not None:
            cur.visited = False
            cur = cur.next
        return has_loop

    # 使用哈希表
    def has_loop_hash_table(self):
        hashtable = {}
        cur = self.head
        while cur.next is not None:
            if cur in hashtable:
                cur.next = None
                return True
            hashtable[cur] = None
            cur = cur.next
        return False

    # 链表回溯
    def has_loop_retracing(self):
        if self.head.next is self.head:
            return True

        cur = self.head
        while cur.next is not None:
            tracer = self.head
            while tracer is not cur:
                if tracer is cur.next:
                    cur.next = None
                    return True
                tracer = tracer.next
            cur = cur.next
        return False

    # 链表反转
    def reverse_list(self):
        pre = None
        cur = self.head
        while cur is not None:
            cur_next = cur.next
            cur.next = pre
            pre = cur
            cur = cur_next
        return pre

    def has_loop_reverse(self):
        pass

    def traverse(self):
        if self.head is None:
            return False
        cur = self.head
        while cur is not None:
            print(cur.data, "->", end=" ")
            cur = cur.next


if __name__ == "__main__":
    mylist = CircularLinkedList()
    mylist.add_circular_node(2)
    mylist.add_circular_node(3)
    mylist.add_circular_node(1)

    mylist1 = CircularLinkedList()
    mylist1.add_node_to_tail(2)
    mylist1.add_node_to_tail(3)
    mylist1.add_node_to_tail(1)

    mylist2 = CircularLinkedList()
    mylist2.add_circular_node(1)

    print(mylist.has_loop_retracing())
    print(mylist1.has_loop_retracing())
    print(mylist2.has_loop_retracing())
