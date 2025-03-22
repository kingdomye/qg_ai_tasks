// Written by ricckker
// Guangdong·Guangzhou
// 2025/3/22

#include <iostream>
using namespace std;

template <typename T>
class QueueNode {
public:
    T data;
    QueueNode<T>* next;

    QueueNode(T data) : data(data), next(nullptr) {}
};

template <typename T>
class LinkQueue {
private:
    QueueNode<T>* front;
    QueueNode<T>* rear;

public:
    LinkQueue() {
        front = nullptr;
        rear = nullptr;
    }

    // 判断队列是否为空
    bool isEmpty() {
        return front == nullptr;
    }

    // 入队操作
    void enQueue(T data) {
        QueueNode<T>* newNode = new QueueNode<T>(data);
        if (isEmpty()) {
            front = newNode;
            rear = newNode;
        } else {
            rear->next = newNode;
            rear = newNode;
        }
    }

    // 出队操作
    T deQueue() {
        if (isEmpty()) {
            cout << "Queue is empty!" << endl;
            exit(0);
        }
        QueueNode<T>* temp = front;
        T data = temp->data;
        front = front->next;
        if (front == nullptr) {
            rear = nullptr;
        }
        delete temp;
        return data;
    }

    // 获取队头元素
    T getFront() {
        if (isEmpty()) {
            cout << "Queue is empty!" << endl;
            exit(0);
        }
        return front->data;
    }

    // 打印队列元素
    void printQueue() {
        QueueNode<T>* current = front;
        while (current != nullptr) {
            cout << current->data << " ";
            current = current->next;
        }
        cout << endl;
    }
};

int main() {
    LinkQueue<int> queue;

    queue.enQueue(10);
    queue.enQueue(20);
    queue.enQueue(30);

    cout << "Queue elements: ";
    queue.printQueue();

    cout << "Front element: " << queue.getFront() << endl;

    cout << "Dequeue element: " << queue.deQueue() << endl;

    cout << "Queue elements after dequeue: ";
    queue.printQueue();

    return 0;
}
