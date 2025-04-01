import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# 固定随机种子以确保可重复性
np.random.seed(42)

n = 8  # 代理数量
p = 0.1  # 边生成概率
threshold = 1e-2  # 收敛阈值
max_iterations = 500  # 最大迭代次数
num_simulations = 100  # 每个s值的模拟次数
delta = 1  # 差分隐私参数
epsilon = 0.1  # 隐私预算
alpha = 1e-6  # 噪声衰减参数

# 生成I矩阵，单位矩阵
A = np.zeros((n, n))

# 设置边权重为两个伯努利试验的和
for i in range(n):
    for j in range(i+1, n):
        w = np.random.binomial(1, 0.1) + np.random.binomial(1, 0.1)
        A[i, j] = w
        A[j, i] = w
print(A)

D = np.diag(A.sum(axis=1))  # 度数矩阵
print(D)
# L = D - A  # 拉普拉斯矩阵
# d_max = D.max().item()  # 最大度数
# h = 0.99 / d_max  # 步长满足稳定性条件

# # 初始化代理状态（固定种子）
# theta0 = np.random.normal(50, 10, n)

# def simulate_s(s):
#     np.random.seed()  # 进程独立随机种子
#     q = alpha + (1 - alpha) * abs(s - 1)
#     c = delta * q / (epsilon * (q - abs(s - 1)))
#     S = s * np.eye(n)
#     B = S - h * L
#     A_matrix = np.eye(n) - h * L  # 状态转移矩阵

#     theta_infinites = []
#     convergence_times = []

#     for _ in range(num_simulations):
#         theta = theta0.copy()
#         converged = False
#         for k in range(max_iterations):
#             b = c * q ** k
#             eta = np.random.laplace(scale=b, size=n)
#             x = theta + eta
#             next_theta = A_matrix @ theta + B @ eta
#             if np.linalg.norm(next_theta - theta) < threshold:
#                 converged = True
#                 break
#             theta = next_theta.copy()
#         convergence_times.append(k if converged else max_iterations)
#         theta_avg = np.mean(theta)
#         theta_infinites.append(theta_avg)

#     variance = np.var(theta_infinites)
#     avg_time = np.mean(convergence_times)
#     return variance, avg_time

# s_values = np.logspace(np.log10(0.8), np.log10(1.2), num=100)
# # s_values = np.linspace(np.log10(0.8), np.log10(1.2), num=100)
# # s_values = np.logspace(0.8, 1.2, num=100)
# plt.plot(s_values)
# plt.show()

# # 单核计算
# variances = []
# times = []
# for s in s_values:
#     variance, avg_time = simulate_s(s)
#     variances.append(variance)
#     times.append(avg_time)

# # 图3(a): 方差随s的变化
# plt.figure(figsize=(10, 6))
# plt.semilogx(s_values, np.sqrt(variances), 'o-', markersize=5)
# plt.xlabel('s (log scale)')
# plt.ylabel('Empirical Standard Deviation')
# plt.title('Accuracy vs. Design Parameter s')
# plt.grid(True)

# # 图3(b): 收敛时间随s的变化
# plt.figure(figsize=(10, 6))
# plt.semilogx(s_values, times, 'o-', markersize=5)
# plt.xlabel('s (log scale)')
# plt.ylabel('Convergence Time (iterations)')
# plt.title('Convergence Speed vs. Design Parameter s')
# plt.grid(True)

# plt.show()
