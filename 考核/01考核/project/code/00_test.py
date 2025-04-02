import numpy as np
from matplotlib import pyplot as plt

# 读取npy文件
try:
    data = np.load('data/B/init_positions.npy')
except FileNotFoundError:
    print("文件不存在")

# params
n = data.shape[0]       # 智能体数量
p = 0.1                 # 伯努利分布概率
threshold = 1e-2        # 收敛条件
max_iterations = 1000   # 最大迭代次数
num_simulations = 100   # 模拟次数
delta = 0.1             # delta参数
epsilon = 0.1           # epsilon参数
alpha = 1e-6            # alpha参数

# 构建邻接矩阵
A = np.zeros((n, n))
for i in range(n):
    for j in range(i+1, n):
        if (np.random.binomial(1, p) + np.random.binomial(1, p)):
            A[i, j] = 1
            A[j, i] = 1s

D = np.diag(A.sum(axis=1))              # 节点度矩阵
L = D - A                               # 邻接矩阵的拉普拉斯矩阵
d_max = D.max().item()                  # 节点度最大值
h = 0.99 / d_max                        # h参数
theta0 = np.random.normal(50, 10, n)    # 初始状态

