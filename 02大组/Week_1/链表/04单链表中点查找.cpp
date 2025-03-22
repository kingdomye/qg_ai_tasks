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
    
    // 中点查找
    Node* findMidPoint() {
        if (!head) {
            return nullptr;
        }
        
        Node* slow = head;
        Node* fast = head;
        
        while (fast != nullptr && fast->next != nullptr) {
            slow = slow->next;
            fast = fast->next->next;
        }
        
        return slow;
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
    
    Node* midNode = new_list.findMidPoint();
    cout << "The middle point is: " << midNode->val << endl;
    
    return 0;
}
