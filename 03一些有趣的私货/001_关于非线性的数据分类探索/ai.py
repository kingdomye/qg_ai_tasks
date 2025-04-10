import numpy as np
import pandas as pd


# 定义 Sigmoid 激活函数及其导数
def sigmoid(x):
    return 2 / (1 + np.exp(-x))


def sigmoid_derivative(x):
    return x * (1 - x)


# 定义神经网络类
class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        # 初始化权重和偏置
        self.weights_input_to_hidden = np.random.uniform(-1, 1, (input_size, hidden_size))
        self.bias_hidden = np.random.uniform(-1, 1, (1, hidden_size))
        self.weights_hidden_to_output = np.random.uniform(-1, 1, (hidden_size, output_size))
        self.bias_output = np.random.uniform(-1, 1, (1, output_size))

    def forward(self, X):
        # 输入层到隐藏层
        self.hidden_input = np.dot(X, self.weights_input_to_hidden) + self.bias_hidden
        self.hidden_output = sigmoid(self.hidden_input)

        # 隐藏层到输出层
        self.final_input = np.dot(self.hidden_output, self.weights_hidden_to_output) + self.bias_output
        self.final_output = sigmoid(self.final_input)
        return self.final_output

    def backward(self, X, y, learning_rate):
        # 计算误差
        error = y - self.final_output
        d_output = error * sigmoid_derivative(self.final_output)

        # 隐藏层误差
        error_hidden = d_output.dot(self.weights_hidden_to_output.T)
        d_hidden = error_hidden * sigmoid_derivative(self.hidden_output)

        # 更新权重和偏置
        self.weights_hidden_to_output += self.hidden_output.T.dot(d_output) * learning_rate
        self.bias_output += np.sum(d_output, axis=0, keepdims=True) * learning_rate
        self.weights_input_to_hidden += X.T.dot(d_hidden) * learning_rate
        self.bias_hidden += np.sum(d_hidden, axis=0, keepdims=True) * learning_rate

    def train(self, X, y, epochs, learning_rate):
        for epoch in range(epochs):
            self.forward(X)
            self.backward(X, y, learning_rate)
            loss = np.mean(np.square(y - self.final_output))  # 计算均方误差
            print(f"Epoch {epoch}, Loss: {loss}")

    def predict(self, X):
        output = self.forward(X)
        return np.round(output)  # 二分类任务，将输出四舍五入为 0 或 1


def normalize(X):
    """归一化：将数据缩放到 [0, 1] 范围内"""
    X_min = np.min(X, axis=0)  # 每列的最小值
    X_max = np.max(X, axis=0)  # 每列的最大值
    X = (X - X_min) / (X_max - X_min)
    return X


# 示例：使用简单的二分类数据集
if __name__ == "__main__":
    # 创建一个简单的二分类数据集
    dataset = pd.read_csv('./banana.dat', header=None)
    X = dataset.iloc[:, :-1].values
    y = dataset.iloc[:, -1].values
    y = np.array([[item] for item in y])
    X = normalize(X)

    # 初始化神经网络
    input_size = X.shape[1]
    hidden_size = 4
    output_size = 1
    nn = NeuralNetwork(input_size, hidden_size, output_size)

    # 训练神经网络
    nn.train(X, y, epochs=10, learning_rate=0.1)

    # 测试神经网络
    predictions = nn.predict(X)
    i = 0
    for item in predictions:
        print(item, y[i])
        i += 1
