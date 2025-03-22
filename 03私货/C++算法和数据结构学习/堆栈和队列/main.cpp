//
//  main.cpp
//  堆栈和队列
//
//  Created by 陈英锐 on 2024/9/30.
//

#include <iostream>

//链表整数类型节点
class IntergerCell
{
public:
    int data;
    IntergerCell* next;
    
    IntergerCell(int data):data(data){}
};

//链表类~链表堆栈
class LinkedList
{
public:
    IntergerCell* head;
    
    LinkedList():head(NULL){}
    
    void push(int data);
    int pop();
};

//链表堆栈压入数据（链表数据头插）
void LinkedList::push(int data)
{
    IntergerCell* newNode = new IntergerCell(data);
    newNode->next = this->head;
    this->head = newNode;
}

//链表堆栈弹出数据
int LinkedList::pop()
{
    if (this->head == NULL) {
        return -1;
    } else {
        int result = this->head->data;
        this->head = this->head->next;
        
        std::cout << "The pop number is:" << result << std::endl;
        return result;
    }
}

//栈反转数组
void reverseArray(int arr[], int size)
{
    std::stack<int> s;
    for (int i = 0; i < size; i++) {
        s.push(arr[i]);
    }
    for (int i = 0; i < size; i++) {
        std::cout << s.top() << " ";
        s.pop();
    }
    std::cout << std::endl;
}

//堆栈插入排序
void stackInsertionSort(std::vector<int>& nums)
{
    std::vector<int> tmpVector;
    for (int i = 0; i < nums.size(); i++) {
        int tmpData = nums[nums.size() - 1];
        nums.erase(nums.begin() + nums.size() - 1);
        while (nums.size()) {
            tmpVector.push_back(nums[nums.size() - 1]);
            nums.erase(nums.begin() + nums.size() - 1);
        }
        for (int i = 0; i < tmpVector.size(); i++) {
            if (tmpData > tmpVector[tmpVector.size() - 1]) {
                break;
            }
            nums.push_back(tmpVector[tmpVector.size() - 1]);
            tmpVector.erase(tmpVector.begin() + tmpVector.size() - 1);
        }
        nums.push_back(tmpData);
        while (tmpVector.size()) {
            nums.push_back(tmpVector[tmpVector.size() - 1]);
            tmpVector.erase(tmpVector.begin() + tmpVector.size() - 1);
        }
    }
    
    for (int i = 0; i < nums.size(); i++) {
        std::cout << nums[i] << " ";
    }
    std::cout << std::endl;
}

//堆栈选择排序
void stackSelectionSort(std::stack<int>& nums)
{
    std::stack<int> tmpStack;
    const size_t size = nums.size();
    
    for (int i = 0; i < size; i++) {
        int maximum = nums.top();
        
        for (int j = i; j < size; j++) {
            if (nums.top() > maximum) {
                maximum = nums.top();
            }
            tmpStack.push(nums.top());
            nums.pop();
        }
        
        nums.push(maximum);
        
        while (!tmpStack.empty()) {
            int val = tmpStack.top();
            tmpStack.pop();
            if (val != maximum) {
                nums.push(val);
            }
        }
    }
    
    while (!nums.empty()) {
        std::cout << nums.top() << " ";
        nums.pop();
    }
    std::cout << std::endl;
}

int main() {
    std::stack<int> myst;
    myst.push(10);
    myst.push(30);
    myst.push(20);
    stackSelectionSort(myst);
    
    return 0;
}
