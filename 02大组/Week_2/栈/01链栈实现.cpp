// Written by ricckker Guangdong·guangzhou
// 2025/3/22

// This code implements the basic functionalities of a linked stack,
// including creation, push, pop, checking for emptiness,
// and obtaining the top element.

#include <iostream>
using namespace std;

// 定义链栈的节点
struct Node {
    int data;
    Node* next;
};

// 定义链栈
class LinkStack {
private:
    Node* top;
public:
    // 构造函数：初始化链栈
    LinkStack() {
        top = nullptr;
    }

    // 析构函数：销毁链栈
    ~LinkStack() {
        while (top != nullptr) {
            Node* temp = top;
            top = top->next;
            delete temp;
        }
    }

    // 判断链栈是否为空
    bool isEmpty() const {
        return top == nullptr;
    }

    // 入栈
    void push(int value) {
        Node* newNode = new Node;
        newNode->data = value;
        newNode->next = top;
        top = newNode;
    }

    // 出栈操作
    void pop() {
        if (isEmpty()) {
            cout << "Pop error! The stack is null!" << endl;
            return;
        }
        Node* temp = top;
        top = top->next;
        delete temp;
    }

    // 获取栈顶元素
    int getTop() const {
        if (isEmpty()) {
            cout << "Get top error! The stack is null!" << endl;
            return -1;
        }
        return top->data;
    }
};

int main() {
    LinkStack stack;

    // test part
    stack.push(10);
    stack.push(20);
    stack.push(30);

    cout << stack.getTop() << endl;

    stack.pop();
    cout << stack.getTop() << endl;

    if (stack.isEmpty()) {
        cout << "Null stack!" << endl;
    } else {
        cout << "the stack is not null" << endl;
    }

    return 0;
}
