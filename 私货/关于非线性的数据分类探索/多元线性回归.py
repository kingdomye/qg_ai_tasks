import pandas as pd
import numpy as np
import random
from matplotlib import pyplot as plt


class LinearRegression:
    def __init__(self):
        self.data = None
        self.X = None
        self.Y = None

    def read_data(self, filename='./banana.dat'):
        self.data = pd.read_csv(filename)

    def divide_dataset(self):
        self.X = self.data.iloc[:, :-1]
        self.Y = self.data.iloc[:, -1]

    def normalize(self):
        """归一化：将数据缩放到 [0, 1] 范围内"""
        X_min = np.min(self.X, axis=0)  # 每列的最小值
        X_max = np.max(self.X, axis=0)  # 每列的最大值
        self.X = (self.X - X_min) / (X_max - X_min)

    def standardize(self):
        """标准化：将数据缩放到均值为 0，标准差为 1 的分布"""
        mean = np.mean(self.X, axis=0)  # 每列的均值
        std = np.std(self.X, axis=0)  # 每列的标准差
        self.X = (self.X - mean) / std

    # 解析解法
    def solution_one(self):
        X = self.X.to_numpy()
        Y = self.Y.to_numpy()
        theta = np.linalg.inv(X.T.dot(X)).dot(X.T).dot(Y)
        print(theta)

    # 梯度下降法
    def solution_two(self, alpha=0.0001):
        X = self.X.to_numpy()
        Y = self.Y.to_numpy()

        theta = np.zeros(X.shape[1])
        for _ in range(1000):
            grad = X.T.dot(np.dot(X, theta) - Y)
            theta = theta - alpha * grad
        print(theta)


if __name__ == '__main__':
    linear_regression = LinearRegression()
    linear_regression.read_data()
    linear_regression.divide_dataset()
    linear_regression.normalize()
    linear_regression.solution_one()
