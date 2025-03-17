//
//  main.cpp
//  链表类
//
//  Created by 陈英锐 on 2024/9/26.
//

#include <iostream>

class IntergerCell
{
public:
    int data;
    IntergerCell* next;
    
    IntergerCell(int data):data(data), next(NULL){}
};

class LinkedList
{
public:
    IntergerCell* head;
    
    LinkedList() {
        head = NULL;
    }
    
    void add_node_to_head(int value);
    void add_node_to_tail(int value);
    void add_node_after(int targetValue, int value);
    void delete_node(int value);
    void traverse(void);
    IntergerCell* find_node(int value);
};

void LinkedList::add_node_to_head(int value)
{
    IntergerCell* newNode = new IntergerCell(value);
    newNode->next = this->head;
    this->head = newNode;
}

void LinkedList::add_node_to_tail(int value)
{
    IntergerCell* newNode = new IntergerCell(value);
    
    if (this->head == NULL) {
        this->head = newNode;
    } else {
        IntergerCell* cur = this->head;
        while (cur->next != NULL) {
            cur = cur->next;
        }
        cur->next = newNode;
    }
}

void LinkedList::add_node_after(int targetValue, int value)
{
    IntergerCell* newNode = new IntergerCell(value);
    
    if (this->head == NULL) {
        this->head = newNode;
    } else {
        IntergerCell* cur = this->head;
        while (cur != NULL) {
            if (cur->data == targetValue) {
                newNode->next = cur->next;
                cur->next = newNode;
                break;
            }
            cur = cur->next;
        }
    }
}

void LinkedList::delete_node(int value)
{
    if (this->head == NULL) {
        std::cout << "LinkedList is NULL!" << std::endl;
    }
    if (this->head->data == value) {
        this->head = this->head->next;
    } else {
        IntergerCell* cur = this->head;
        while (cur->next != NULL) {
            if (cur->next->data == value) {
                cur->next = cur->next->next;
                break;
            }
            cur = cur->next;
        }
    }
}

void LinkedList::traverse(void)
{
    IntergerCell* cur = this->head;
    while (cur != NULL) {
        std::cout << cur->data << " -> ";
        cur = cur->next;
    }
    std::cout << std::endl;
}

IntergerCell* LinkedList::find_node(int value)
{
    IntergerCell* cur = this->head;
    while (cur != NULL) {
        if (cur->data == value) {
            std::cout << "Find target node:" << cur->data << std::endl;
            return cur;
        }
        cur = cur->next;
    }
    
    return NULL;
}

int main() {
    LinkedList mylist;
    mylist.add_node_to_head(30);
    mylist.add_node_to_head(10);
    mylist.add_node_to_tail(1000);
    mylist.add_node_after(10, 200);
    mylist.delete_node(30);
    mylist.traverse();
    
    IntergerCell* targetNode = mylist.find_node(10);
    std::cout << targetNode->data << std::endl;
    
    return 0;
}
