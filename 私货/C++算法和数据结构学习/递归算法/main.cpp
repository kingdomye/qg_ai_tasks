//
//  main.cpp
//  递归算法
//
//  Created by 陈英锐 on 2024/10/7.
//

#include <iostream>

//简单递归实例 1（阶乘计算）
int factorial(int n)
{
    if (n == 0) {
        return 1;
    }
    return n * factorial(n - 1);
}

//简单递归实例 2 （斐波那契数列）
int fibonacci(int n)
{
    if (n <= 1) {
        return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}

//简单递归实例 3 （棒料切割问题）


int main() {
    std::cout << fibonacci(10) << std::endl;

    return 0;
}
