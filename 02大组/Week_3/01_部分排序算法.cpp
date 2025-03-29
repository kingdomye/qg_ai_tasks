//
//  main.cpp
//  排序算法
//
//  Created by 陈英锐 on 2024/9/30.
//

#include <iostream>
#include <cstdlib>
#include <ctime>

void printArray(int* arr, int size);
void printVector(std::vector<int>& vec);
int* createRandomArray(int size);
std::vector<int> createRandomVector(int size);

int* selectionSort(int* arr, int size);
int* insertSort(int* arr, int size);
int* bubbleSort(int* arr, int size);
int* countingSort(int* arr, int size);

void vectorToHeap(std::vector<int>& vec);
int removeTopItem(std::vector<int>& vec);
void heapSort(std::vector<int>& vec);

int main() {
    std::vector<int> myvec = createRandomVector(10);
    heapSort(myvec);
    
    return 0;
}

//打印数组
void printArray(int* arr, int size)
{
    for (int i = 0; i < size; i++) {
        std::cout << arr[i] << " ";
    }
    std::cout << std::endl;
}

void printVector(std::vector<int>& vec)
{
    for (int item : vec) {
        std::cout << item << " ";
    }
    std::cout << std::endl;
}

//创建size长度随机数（0～100）数组
int* createRandomArray(int size)
{
    srand(static_cast<unsigned int>(time(0)));
    int* myarray = new int[size];
    
    for (int i = 0; i < size; i++) {
        myarray[i] = rand() % 100 + 1;
    }
    
    printArray(myarray, size);
    return myarray;
}

std::vector<int> createRandomVector(int size)
{
    srand(static_cast<unsigned int>(time(0)));
    std::vector<int> res;
    
    for (int i = 0; i < size; i++) {
        res.push_back(rand() % 100 + 1);
    }
    
    printVector(res);
    
    return res;
}


//选择排序
int* selectionSort(int* arr, int size)
{
    for (int i = 0; i < size; i++) {
        int minimum = i;
        for (int j = i; j < size; j++) {
            if (arr[j] < arr[minimum]) {
                minimum = j;
            }
        }
        std::swap(arr[i], arr[minimum]);
    }
    
    printArray(arr, size);
    return arr;
}

//插入排序
int* insertSort(int* arr, int size)
{
    for (int i = 1; i < size; i++) {
        for (int j = 0; j < i; j++) {
            if (arr[j] > arr[i]) {
                int tmp = arr[i];
                for (int k = i; k > j; k--) {
                    arr[k] = arr[k-1];
                }
                arr[j] = tmp;
            }
        }
    }
    
    printArray(arr, size);
    return arr;
}

//冒泡排序
int* bubbleSort(int* arr, int size)
{
    bool flag = true;
    while (flag) {
        flag = false;
        for (int i = 1; i < size; i++) {
            for (int j = size - 1; j >= i; j--) {
                if (arr[j - 1] > arr[j]) {
                    flag = true;
                    std::swap(arr[j - 1], arr[j]);
                }
            }
        }
    }
    
    printArray(arr, size);
    return arr;
}

//计数排序
int* countingSort(int* arr, int size)
{
    int countingArray[101];
    memset(countingArray, 0, sizeof(countingArray));
    for (int i = 0; i < size; i++) {
        countingArray[arr[i] + 1] += 1;
    }
    
    int j = 0;
    for (int i = 0; i < 101; i++) {
        while (countingArray[i]--) {
            arr[j++] = i - 1;
        }
    }
    
    printArray(arr, size);
    return arr;
}

//vector调整堆
void vectorToHeap(std::vector<int>& vec)
{
    for (int i = 0; i < vec.size(); i++) {
        int index = i;
        while (index) {
            int parentIndex = (index - 1) / 2;
            if (vec.at(parentIndex) >= vec.at(index)) {
                break;
            }
            std::swap(vec.at(parentIndex), vec.at(index));
            index = parentIndex;
        }
    }
}

//移除堆顶部元素（最大值）
int removeTopItem(std::vector<int>& vec)
{
    int topVal = vec.at(0);
    vec.at(0) = vec.back();
    vec.pop_back();
    
    int index = 0;
    while (index < vec.size()) {
        int child1 = (2 * index + 1 >= vec.size()) ? index : 2 * index + 1;
        int child2 = (2 * index + 2 >= vec.size()) ? index : 2 * index + 2;
        
        if (vec.at(index) >= vec.at(child1) && vec.at(index) >= vec.at(child2)) {
            break;
        }
        
        int swap_index = (vec.at(child1) > vec.at(child2)) ? child1 : child2;
        std::swap(vec.at(index), vec.at(swap_index));
        index = swap_index;
    }
    
    return topVal;
}

//堆排序主函数
void heapSort(std::vector<int>& vec)
{
    vectorToHeap(vec);
    const size_t size = vec.size();
    for (int i = 0; i < size; i++) {
        std::cout << removeTopItem(vec) << " ";
    }
    std::cout << std::endl;
}
