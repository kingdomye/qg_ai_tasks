import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def normalize(X):
    """归一化：将数据缩放到 [0, 1] 范围内"""
    X_min = np.min(X, axis=0)  # 每列的最小值
    X_max = np.max(X, axis=0)  # 每列的最大值
    X = (X - X_min) / (X_max - X_min)
    return X


class LogisticRegression:
    def __init__(self):
        self.w = None
        self.X = None
        self.y = None

    def read_data(self, filename='./data/iris.csv'):
        """读取数据"""
        df = pd.read_csv(filename)
        self.X = df.iloc[:, 1:-1].values
        self.y = df.iloc[:, -1].values

    def divide_data(self):
        """划分数据集：训练集/测试集"""
        indices = np.arange(0, self.X.shape[0])
        np.random.shuffle(indices)

        train_size = int(self.X.shape[0] * 0.8)
        train_indices = indices[:train_size]
        test_indices = indices[train_size:]

        train_X = self.X[train_indices]
        train_y = self.y[train_indices]
        test_X = self.X[test_indices]
        test_y = self.y[test_indices]

        return train_X, train_y, test_X, test_y

    def train(self, epochs=100, learning_rate=0.01):
        """梯度下降法迭代求解参数w"""
        self.w = np.ones(self.X.shape[1])
        train_X, train_y, _, _ = self.divide_data()
        train_X = normalize(train_X)
        loss_history = []

        for epoch in range(epochs):
            # 计算梯度
            grad = np.mean(
                [((sigmoid(np.dot(self.w.T, train_X[i])) - train_y[i]) * train_X[i]) for i in range(train_X.shape[0])],
                axis=0)
            self.w -= learning_rate * grad

            # 计算损失
            loss = -np.mean([
                (train_y[i] * np.log(sigmoid(np.dot(self.w.T, train_X[i]))) +
                 (1 - train_y[i]) * np.log(1 - sigmoid(np.dot(self.w.T, train_X[i]))))
                for i in range(train_X.shape[0])
            ])
            loss_history.append(loss)

            if (epoch + 1) % 10 == 0:
                print('epoch: {}, loss: {}, w: {}'.format(epoch+1, loss, self.w))

        return loss_history


if __name__ == '__main__':
    lr = LogisticRegression()
    lr.read_data()
    lr_loss = lr.train(epochs=1000, learning_rate=0.1)

    # 绘制损失函数
    plt.title("MSE LINE")
    plt.plot(lr_loss)
    plt.show()
