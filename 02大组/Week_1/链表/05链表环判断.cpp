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
    
    // 链表环判断
    bool hasCircle() {
        if (!head) {
            return false;
        }
        Node* slow = head;
        Node* fast = head;
        
        while (fast != nullptr && fast->next != nullptr) {
            slow = slow->next;
            fast = fast->next->next;
            
            if (slow == fast) {
                return true;    //成环为true
            }
        }
        
        return false;
    }
};

int main() {
    LinkedList new_list;
    new_list.add_node_to_tail(1);
    new_list.add_node_to_tail(2);
    new_list.add_node_to_tail(3);
    new_list.add_node_to_tail(4);
    new_list.add_node_to_tail(5);
    new_list.head->next->next->next->next = new_list.head->next;    //创建环
    
    bool ans = new_list.hasCircle();
    cout << ans << endl;
    
    
    return 0;
}
