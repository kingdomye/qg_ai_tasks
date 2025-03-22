import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def read_data(filename='./banana.dat'):
    """读取数据集"""
    dataset = pd.read_csv(filename)
    return dataset


def divide_dataset(dataset):
    """划分数据集"""
    X, y = dataset.iloc[:, :-1].values, dataset.iloc[:, -1].values
    y = np.where(y < 0, 0, 1)
    y = np.array([[item] for item in y])

    index_train = np.random.permutation(int(len(X) * 0.8))
    X_train, y_train = X[index_train], y[index_train]
    index_test = np.random.permutation(int(len(X) * 0.2))
    X_test, y_test = X[index_test], y[index_test]

    return X, X_train, X_test, y, y_train, y_test


def draw_data(filename='./banana.dat'):
    """可视化数据集"""
    dataset = read_data(filename)
    X, X_train, X_test, y, y_train, y_test = divide_dataset(dataset)
    plt.scatter(X[:, 0], X[:, 1], c=y)
    plt.show()


def normalize(X):
    """归一化：将数据缩放到 [0, 1] 范围内"""
    X_min = np.min(X, axis=0)  # 每列的最小值
    X_max = np.max(X, axis=0)  # 每列的最大值
    X = (X - X_min) / (X_max - X_min)
    return X


def sigmoid(x):
    """神经元激活函数"""
    return 1 / (1 + np.exp(-x))


def sigmoid_derivative(x):
    """激活函数导数"""
    return sigmoid(x) * (1 - sigmoid(x))


class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        self.hidden_input = None
        self.hidden_output = None
        self.final_input = None
        self.final_output = None

        self.weights_input_to_hidden = np.random.uniform(-1, 1, (input_size, hidden_size))
        self.bias_hidden = np.random.uniform(-1, 1, (1, hidden_size))
        self.weights_hidden_to_output = np.random.uniform(-1, 1, (hidden_size, output_size))
        self.bias_output = np.random.uniform(-1, 1, (1, output_size))

    def forward(self, X):
        """数据前向传播"""
        # 输入层到隐藏层
        self.hidden_input = np.dot(X, self.weights_input_to_hidden) + self.bias_hidden
        self.hidden_output = sigmoid(self.hidden_input)

        # 隐藏层到输出层
        self.final_input = np.dot(self.hidden_output, self.weights_hidden_to_output) + self.bias_output
        self.final_output = sigmoid(self.final_input)
        return self.final_output

    def backward(self, X, y, learning_rate):
        """反向传播梯度下降法"""
        error = y - self.forward(X)
        delta_output = error * sigmoid_derivative(self.forward(X))

        self.weights_hidden_to_output += learning_rate * self.hidden_output.T.dot(delta_output)
        self.bias_output += np.sum(delta_output, axis=0, keepdims=True) * learning_rate

        error_hidden = delta_output.dot(self.weights_hidden_to_output.T)
        d_hidden = error_hidden * sigmoid_derivative(self.hidden_output)

        self.weights_input_to_hidden += X.T.dot(d_hidden) * learning_rate
        self.bias_hidden += np.sum(d_hidden, axis=0, keepdims=True) * learning_rate

    def train(self, X, y, epochs, learning_rate):
        """训练模型"""
        for epoch in range(epochs):
            self.forward(X)
            self.backward(X, y, learning_rate)
            loss = np.mean(np.square(y - self.final_output))
            print(f"Epoch {epoch}, Loss: {loss}")

    def predict(self, X):
        """预测输出"""
        return np.round(self.forward(X))


if __name__ == '__main__':
    draw_data()
    # 模型创建和训练
    nn = NeuralNetwork(2, 10, 1)
    X, x_train, x_test, y, y_train, y_test = divide_dataset(read_data())
    x_train = normalize(x_train)
    nn.train(x_train, y_train, epochs=10, learning_rate=0.00065)

    # 预测输出及模型评估
    predicts = nn.predict(x_test)
    true_count = 0
    for i in range(len(predicts)):
        print(f"Predicted label: {int(predicts[i][0])}, Actual label: {int(y_test[i][0])}")
        if int(predicts[i][0]) == int(y_test[i][0]):
            true_count += 1
    true_rate = true_count / len(predicts)
    print(f"True rate: {true_rate}")
