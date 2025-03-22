// Written by ricckker
// Guangdong·Guangzhou
// 2025/3/22

// This code implements a simple four - operation calculator using linked stacks.
// It converts infix expressions into Reverse Polish Notation (RPN)
// and evaluates the expressions.

#include <iostream>
#include <cctype>
#include <string>
using namespace std;

struct Node {
    char data;
    Node* next;
};

class LinkStack {
private:
    Node* top;
public:
    LinkStack() {
        top = nullptr;
    }

    ~LinkStack() {
        while (top != nullptr) {
            Node* temp = top;
            top = top->next;
            delete temp;
        }
    }

    bool isEmpty() const {
        return top == nullptr;
    }

    void push(char value) {
        Node* newNode = new Node;
        newNode->data = value;
        newNode->next = top;
        top = newNode;
    }

    char pop() {
        if (isEmpty()) {
            cerr << "Pop error! The stack is null!" << endl;
            exit(1);
        }
        Node* temp = top;
        char value = top->data;
        top = top->next;
        delete temp;
        return value;
    }

    char getTop() const {
        if (isEmpty()) {
            cerr << "Get top error! The stack is null!" << endl;
            exit(1);
        }
        return top->data;
    }
};

int precedence(char op) {
    if (op == '+' || op == '-') return 1;
    if (op == '*' || op == '/') return 2;
    return 0;
}

bool isOperator(char c) {
    return c == '+' || c == '-' || c == '*' || c == '/';
}

string infixToPostfix(const string& infix) {
    LinkStack opStack;
    string postfix;
    for (char c : infix) {
        if (isdigit(c)) {
            postfix += c;
        } else if (c == '(') {
            opStack.push(c);
        } else if (c == ')') {
            while (!opStack.isEmpty() && opStack.getTop() != '(') {
                postfix += opStack.pop();
            }
            if (!opStack.isEmpty()) {
                opStack.pop();
            }
        } else if (isOperator(c)) {
            while (!opStack.isEmpty() && precedence(opStack.getTop()) >= precedence(c)) {
                postfix += opStack.pop();
            }
            opStack.push(c);
        }
    }
    while (!opStack.isEmpty()) {
        postfix += opStack.pop();
    }
    return postfix;
}

int evaluatePostfix(const string& postfix) {
    LinkStack numStack;
    for (char c : postfix) {
        if (isdigit(c)) {
            numStack.push(c - '0');
        } else if (isOperator(c)) {
            int b = numStack.pop();
            int a = numStack.pop();
            switch (c) {
                case '+': numStack.push(a + b); break;
                case '-': numStack.push(a - b); break;
                case '*': numStack.push(a * b); break;
                case '/': numStack.push(a / b); break;
            }
        }
    }
    return numStack.pop();
}

int main() {
    string infix;
    cout << "请输入中缀表达式（仅支持数字和运算符，不支持空格）：";
    cin >> infix;

    string postfix = infixToPostfix(infix);
    cout << "后缀表达式：" << postfix << endl;

    int result = evaluatePostfix(postfix);
    cout << "Result：" << result << endl;

    return 0;
}
