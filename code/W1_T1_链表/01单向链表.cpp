//
// Created by 陈英锐 on 25-3-14.
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
            cout << cur->val << endl;
            cur = cur->next;
        }
    }

    // 查找节点
    Node* find_node(int val) {
        Node* cur = head;
        while (cur != nullptr) {
            if (cur->val == val) {
                return cur;
            }
            cur = cur->next;
        }
        return nullptr;
    }

    // 顶部添加节点
    void add_node_to_head(int val) {
        Node* new_node = new Node();
        new_node->val = val;

        if (head == nullptr) {
            head = new_node;
        } else {
            new_node->next = head;
            head = new_node;
        }
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

    // 在指定节点后添加节点
    void add_node_after(int target, int val) {
        Node* new_node = new Node();
        new_node->val = val;

        if (head == nullptr) {
            head = new_node;
        } else {
            Node* cur = head;
            while (cur != nullptr) {
                if (cur->val == target) {
                    new_node->next = cur->next;
                    cur->next = new_node;
                    break;
                }
                cur = cur->next;
            }
        }
    }

    // 删除节点
    void delete_node(int val) {
        if (head == nullptr) {
            return;
        }
        if (head->val == val) {
            Node* temp = head;
            head = head->next;
            delete temp;
            return;
        } else {
            Node* cur = head;
            while (cur->next != nullptr) {
                if (cur->next->val == val) {
                    Node* temp = cur->next;
                    cur->next = cur->next->next;
                    delete temp;
                    break;
                }
                cur = cur->next;
            }
        }
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
    new_list.add_node_to_head(3);
    new_list.traverse();
    return 0;
}