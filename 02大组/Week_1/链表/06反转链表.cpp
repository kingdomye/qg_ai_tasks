//
// Created by 陈英锐 on 25-3-15.
//
#include <iostream>
using namespace std;

// 链表节点类
class Node {
public:
    int val;
    Node* next;

    Node() {
        val = 0;
        next = nullptr;
    }
};

// 链表类
class LinkedList {
public:
    Node* head;
    
    LinkedList() {
        head = nullptr;
    }

    // 遍历链表
    void traverse() {
        Node* cur = head;
        while (cur != nullptr) {
            cout << cur->val;
            cur = cur->next;
            if (cur != NULL) {
                cout << "->";
            }
        }
        cout << endl;
    }

    // 尾部添加节点
    void add_node_to_tail(int val) {
        Node* new_node = new Node();
        new_node->val = val;

        if (head == nullptr) {
            head = new_node;
        } else {
            Node* cur = head;
            while (cur->next != nullptr) {
                cur = cur->next;
            }
            cur->next = new_node;
        }
    }
    
    // 链表反转（迭代法）
    void reverse_one() {
        Node* prev = nullptr;
        Node* cur = head;
        Node* next = nullptr;

        while (cur != nullptr) {
            next = cur->next;
            cur->next = prev;
            prev = cur;
            cur = next;
        }

        head = prev;
    }
    
    // 链表反转（递归法）
    Node* reverse_two_func(Node* node) {
        if (!node || !node->next) {
            return node;
        }
        
        Node* newHead = reverse_two_func(node->next);
        node->next->next = node;
        node->next = nullptr;
        
        return newHead;
    }
    
    void reverse_two() {
        head = reverse_two_func(head);
    }
};

int main() {
    LinkedList new_list;
    new_list.add_node_to_tail(1);
    new_list.add_node_to_tail(2);
    new_list.add_node_to_tail(3);
    new_list.add_node_to_tail(4);
    new_list.add_node_to_tail(5);
    new_list.traverse();
    
    new_list.reverse_one();
    new_list.traverse();
    
    new_list.reverse_two();
    new_list.traverse();
    
    return 0;
}
