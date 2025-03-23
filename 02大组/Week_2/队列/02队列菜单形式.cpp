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
            cout << "Pop error! The stack is empty!" << endl;
            return;
        }
        Node* temp = top;
        top = top->next;
        delete temp;
    }

    // 获取栈顶元素
    int getTop() const {
        if (isEmpty()) {
            cout << "Get top error! The stack is empty!" << endl;
            return -1;
        }
        return top->data;
    }

    // 清空链栈
    void clear() {
        while (!isEmpty()) {
            pop();
        }
    }

    // 打印链栈
    void print() const {
        Node* current = top;
        cout << "Stack (top to bottom): ";
        while (current != nullptr) {
            cout << current->data << " ";
            current = current->next;
        }
        cout << endl;
    }

    // 获取链栈长度
    int size() const {
        int count = 0;
        Node* current = top;
        while (current != nullptr) {
            count++;
            current = current->next;
        }
        return count;
    }

    // 重新初始化链栈
    void reinitialize() {
        clear();
    }
};

int main() {
    LinkStack stack;
    int choice, value;

    string menu = "1、元素入栈\n2、元素出栈\n3、判断栈是否为空\n4、获取栈顶元素\n5、清空栈\n6、销毁栈\n7、获取栈的长度\n8、重新初始化栈\n9、打印栈\n10、退出程序";

    while (true) {
        cout << menu << endl;
        cout << "请输入你的选择：";
        cin >> choice;

        switch (choice) {
            case 1: // 元素入栈
                cout << "请输入要入栈的元素：";
                cin >> value;
                stack.push(value);
                break;
            case 2: // 元素出栈
                stack.pop();
                break;
            case 3: // 判断栈是否为空
                if (stack.isEmpty()) {
                    cout << "栈为空。" << endl;
                } else {
                    cout << "栈不为空。" << endl;
                }
                break;
            case 4: // 获取栈顶元素
                value = stack.getTop();
                if (value != -1) {
                    cout << "栈顶元素是：" << value << endl;
                }
                break;
            case 5: // 清空栈
                stack.clear();
                cout << "栈已清空。" << endl;
                break;
            case 6: // 销毁栈
                stack.~LinkStack();
                cout << "栈已销毁。" << endl;
                return 0;
            case 7: // 获取栈的长度
                cout << "栈的长度为：" << stack.size() << endl;
                break;
            case 8: // 重新初始化栈
                stack.reinitialize();
                cout << "栈已重新初始化。" << endl;
                break;
            case 9: // 打印栈
                stack.print();
                break;
            case 10: // 退出程序
                return 0;
            default:
                cout << "无效的选择，请重新输入。" << endl;
        }
    }

    return 0;
}