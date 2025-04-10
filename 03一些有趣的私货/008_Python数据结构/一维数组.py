"""
一维数组
Created by ricckker on 2024/9/4
Updated on 2024/9/4
"""

import random

# 生成随机数组
def createRandomArray(size):
    arr = []
    for i in range(size):
        arr.append(random.randint(1, 100))
    return arr

# 查找元素
def indexOf(arr, element):
    for i in range(len(arr)):
        if arr[i] == element:
            return i
    return False

# 查找最小值
def findMinimum(arr):
    res = arr[0]
    for i in range(1, len(arr)):
        if arr[i] < res:
            res = arr[i]
    return res

# 查找最大值
def findMaxmum(arr):
    res = arr[0]
    for i in range(1, len(arr)):
        if arr[i] > res:
            res = arr[i]
    return res

# 查找平均值
def findAverage(arr):
    total = 0
    for item in arr:
        total += item
    res = total / len(arr)
    return res
