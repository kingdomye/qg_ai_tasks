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
private:
    Node* head;

public:
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
    
    // 链表奇偶互换
    void oddEvenList() {
        if (!head || !head->next) {
            return;
        }

        Node* dummy = new Node();
        dummy->next = head;
        Node* prev = dummy;

        while (head && head->next) {
            Node* first = head;
            Node* second = head->next;

            prev->next = second;
            first->next = second->next;
            second->next = first;

            prev = first;
            head = first->next;
        }

        head = dummy->next;
    }

    // 析构函数，释放链表内存
    ~LinkedList() {
        Node* cur = head;
        while (cur != nullptr) {
            Node* temp = cur;
            cur = cur->next;
            delete temp;
        }
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
    
    new_list.oddEvenList();
    new_list.traverse();
    
    return 0;
}
