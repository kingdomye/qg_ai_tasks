import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


# 分类感知器
class Perceptron:
    def __init__(self, input_size, learning_rate=0.01):
        self.weigths = np.zeros(input_size)
        self.bias = 0.0
        self.lr = learning_rate
        self.history = {'loss': [], 'accuracy': []}

    # 阶跃激活函数
    def activation(self, z):
        return np.where(z >= 0, 1, -1)

    def predict(self, X):
        z = np.dot(X, self.weigths) + self.bias
        return self.activation(z)

    #训练函数
    def fit(self, X, y, epochs):
        X = np.array(X)
        y = np.array(y)
        for epoch in range(epochs):
            # 随机打乱数据
            i = list(range(len(y)))
            np.random.shuffle(i)
            X_shuffle = X[i]; y_shuffle = y[i]

            total_loss = 0
            correct = 0
            for xi, yi in zip(X_shuffle, y_shuffle):
                prediction = self.predict(xi)
                error = yi - prediction

                # 更新权重和偏置
                self.weigths = self.weigths + self.lr * error * xi
                self.bias = self.bias + self.lr * error

                total_loss = total_loss + int(prediction != yi)
                correct = correct + int(prediction == yi)

            # 记录训练过程
            avg_loss = total_loss / len(y)
            avg_correct = correct / len(y)
            self.history['loss'].append(avg_loss)
            self.history['accuracy'].append(avg_correct)


# 分割训练集和测试集
def divide(len_data):
    train_num = int(0.8 * len_data)
    indices = list(range(len_data))
    np.random.shuffle(indices)
    train = indices[:train_num]
    test = indices[train_num:]
    return train, test

def normalize(X):
    """归一化：将数据缩放到 [0, 1] 范围内"""
    X_min = np.min(X, axis=0)  # 每列的最小值
    X_max = np.max(X, axis=0)  # 每列的最大值
    X = (X - X_min) / (X_max - X_min)
    return X

if __name__ == '__main__':
    df = pd.read_csv('./banana.dat', header=None)
    x = df.iloc[:, :2].values
    print(x)
    y = df.iloc[:, 2].values.ravel()
    plt.scatter(x[:, 0], x[:, 1], c=y)

    len_data = len(y)
    train, test = divide(len_data)

    # 训练集
    x_train = x[train]
    y_train = y[train]
    # 测试集
    x_test = x[test]
    y_test = y[test]

    # 将训练集数据输入感知器
    perceptron = Perceptron(2, 0.01)
    perceptron.fit(normalize(x_train), y_train, 100)

    y_predict = perceptron.predict(x_test)
    y = np.c_[y_test, y_predict]
    y = pd.DataFrame(y)
    # y.to_csv('./practise1.csv')
    
    # 绘制决策边界
    x1_min, x1_max = x[:, 0].min() - 1, x[:, 0].max() + 1
    x2_min, x2_max = x[:, 1].min() - 1, x[:, 1].max() + 1
    xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, 0.01),
                           np.arange(x2_min, x2_max, 0.01))
    Z = perceptron.predict(np.c_[xx1.ravel(), xx2.ravel()])
    Z = Z.reshape(xx1.shape)
    plt.contourf(xx1, xx2, Z, alpha=0.3)
    plt.show()
