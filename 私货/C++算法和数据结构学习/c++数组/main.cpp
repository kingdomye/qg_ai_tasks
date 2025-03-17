//
//  main.cpp
//  c++数组
//
//  Created by 陈英锐 on 2024/9/27.
//

#include <iostream>

int IndexOf(int* arr, int size, int target);
int FindMinimum(int* arr, int size);
int FindMaxmum(int* arr, int size);
float FindAverage(int* arr, int size);

int main() {
    int myarray[10] = {11, 30, 20, 35, 78, 29, 8, 192, 18, 36};
    int size = 10;
    
    float aver = FindAverage(myarray, size);
    std::cout << aver << std::endl;
    
    return 0;
}

int IndexOf(int* arr, int size, int target)
{
    for (int i = 0; i < size; i++) {
        if (arr[i] == target) {
            return i;
        }
    }
    
    return -1;
}

int FindMinimum(int* arr, int size)
{
    int minimum = arr[0];
    for (int i = 1; i < size; i++) {
        if (arr[i] < minimum) {
            minimum = arr[i];
        }
    }
    
    return minimum;
}

int FindMaxmum(int* arr, int size)
{
    int maxmum = arr[0];
    for (int i = 1; i < size; i++) {
        if (arr[i] > maxmum) {
            maxmum = arr[i];
        }
    }
    
    return maxmum;
}

float FindAverage(int* arr, int size)
{
    float total = 0;
    for (int i = 0; i < size; i++) {
        total += arr[i];
    }
    
    return total/size;
}
