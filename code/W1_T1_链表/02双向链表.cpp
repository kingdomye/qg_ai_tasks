//
// Created by 陈英锐 on 25-3-14.
//
#include <iostream>
using namespace std;

// 双向链表节点类
class Node {
public:
    int data;
    Node* next;
    Node* prev;

    Node() {
        data = 0;
        next = nullptr;
        prev = nullptr;
    }
};

// 双向链表类
class DoubleLinkedList {
private:
    Node* head;

public:
    DoubleLinkedList() {
        head = nullptr;
    }

    // 在头部添加节点
    void add_node_to_head(int data) {
        Node* new_node = new Node();
        new_node->data = data;

        if (head == nullptr) {
            head = new_node;
        } else {
            head->prev = new_node;
            new_node->next = head;
            head = new_node;
        }
    }

    // 在尾部添加节点
    void add_node_to_tail(int data) {
        Node* new_node = new Node();
        new_node->data = data;

        if (head == nullptr) {
            head = new_node;
        } else {
            Node* cur = head;
            while (cur->next != nullptr) {
                cur = cur->next;
            }
            cur->next = new_node;
            new_node->prev = cur;
        }
    }

    // 遍历链表
    void traverse() {
        Node* cur = head;
        while (cur != nullptr) {
            cout << cur->data << " ";
            cur = cur->next;
        }
        cout << endl;
    }

    // 析构函数，释放链表内存
    ~DoubleLinkedList() {
        Node* cur = head;
        while (cur != nullptr) {
            Node* temp = cur;
            cur = cur->next;
            delete temp;
        }
    }
};

int main() {
    DoubleLinkedList dll;
    dll.add_node_to_head(10);
    dll.add_node_to_tail(20);
    dll.add_node_to_head(5);
    dll.add_node_to_tail(30);

    cout << "Traversing the doubly linked list: ";
    dll.traverse();

    return 0;
}
