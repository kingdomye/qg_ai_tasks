"""
关于代码的公式推导可详见笔记note部分：
W1_T2_线性回归公式推导.md
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class LinearRegression:
    def __init__(self):
        self.data = None
        self.X = None
        self.Y = None

    def read_data(self, filename='./data/boston.csv'):
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
        return theta

    # 预测数据可视化
    def visualize_features(self):
        """绘制每个特征与目标值的关系图"""
        features = self.X.columns
        num_features = len(features)
        fig, axes = plt.subplots(nrows=num_features, figsize=(10, 5 * num_features))

        for i, feature in enumerate(features):
            axes[i].scatter(self.X[feature], self.Y, alpha=0.5)
            axes[i].set_title(f"{feature} && Target")
            axes[i].set_xlabel(feature)
            axes[i].set_ylabel("Target")

        plt.tight_layout()
        plt.show()

    def visualize_predictions(self, theta):
        """绘制预测结果与真实值的对比图"""
        X = self.X.to_numpy()
        Y_pred = X.dot(theta)
        plt.figure(figsize=(10, 6))
        plt.scatter(range(len(self.Y)), self.Y, label="True Values", alpha=0.5)
        plt.scatter(range(len(Y_pred)), Y_pred, label="Predictions", alpha=0.5, color="red")
        plt.xlabel("Index")
        plt.ylabel("Value")
        plt.title("True && Predictions")
        plt.legend()
        plt.show()


if __name__ == '__main__':
    # model training part
    linear_regression = LinearRegression()
    linear_regression.read_data()
    linear_regression.divide_dataset()
    linear_regression.normalize()
    theta = linear_regression.solution_two()

    # 可视化特征与目标值的关系
    linear_regression.visualize_features()

    # 可视化预测结果与真实值的对比
    linear_regression.visualize_predictions(theta)