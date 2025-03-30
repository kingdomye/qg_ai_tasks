import numpy as np
import matplotlib.pyplot as plt

# 参数设置
n = 50  # 智能体数量
delta = 1  # 隐私参数
num_simulations = 100  # 模拟次数
tolerance = 1e-2  # 收敛容忍度


# 生成随机图的邻接矩阵
def generate_random_graph(n, p=0.1):
    A = np.random.rand(n, n) < p
    A = A + A.T  # 保证无向图
    np.fill_diagonal(A, 0)
    return A


# 生成拉普拉斯噪声
def laplace_noise(scale):
    return np.random.laplace(0, scale)


# 模拟平均共识算法
def simulate_consensus(A, s, alpha, initial_states, num_steps=1000):
    n = len(initial_states)
    L = np.diag(np.sum(A, axis=1)) - A  # 拉普拉斯矩阵
    h = 1 / np.max(np.diag(np.sum(A, axis=1)))  # 步长
    S = s * np.eye(n)
    q = alpha + (1 - alpha) * np.abs(s - 1)
    c = delta * q / (alpha * (q - np.abs(s - 1))) * np.ones(n)  # 确保 c 是一个长度为 n 的数组

    states = initial_states.copy()
    for k in range(num_steps):
        noise = np.array([laplace_noise(ci * q ** k) for ci in c])
        messages = states + noise
        states = states - h * np.dot(L, messages) + np.dot(S, noise)
        if np.linalg.norm(states - np.mean(states)) < tolerance:
            return states, k + 1
    return states, num_steps


# 生成随机图和初始状态
A = generate_random_graph(n)
initial_states = np.random.normal(50, 10, n)

# 扫描 s 的值
s_values = np.logspace(-1, 0.2, 10)  # 从 0.1 到 1.6
std_devs = []
settling_times = []

for s in s_values:
    std_dev = []
    settling_time = []
    for _ in range(num_simulations):
        final_states, steps = simulate_consensus(A, s, 1e-6, initial_states)
        std_dev.append(np.std(final_states))
        settling_time.append(steps)
    std_devs.append(np.mean(std_dev))
    settling_times.append(np.mean(settling_time))

# 绘制样本标准差
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(s_values, std_devs, marker='o')
plt.xscale('log')
plt.xlabel('s')
plt.ylabel('Sample Standard Deviation')
plt.title('Empirical Standard Deviation of Convergence Point')
plt.grid(True)

# 绘制收敛时间
plt.subplot(1, 2, 2)
plt.plot(s_values, settling_times, marker='o')
plt.xscale('log')
plt.xlabel('s')
plt.ylabel('Settling Time')
plt.title('Settling Time of Consensus Algorithm')
plt.grid(True)

plt.tight_layout()
plt.show()