import numpy as np
from matplotlib import pyplot as plt
from joblib import Parallel, delayed
from tqdm import tqdm

# 读取npy文件
try:
    data = np.load('data/B/init_positions.npy')
except FileNotFoundError:
    print("文件不存在")

# params
n = data.shape[0]                       # 智能体数量
p = 0.1                                 # 伯努利分布概率
threshold = 1e-2                        # 收敛条件
max_iterations = 1000                   # 最大迭代次数
num_simulations = 1000                   # 模拟次数
delta = 0.1                             # delta参数
epsilon = 0.1                           # epsilon参数
alpha = 1e-6                            # alpha参数

# 构建邻接矩阵
A = np.zeros((n, n))
for i in range(n):
    for j in range(i+1, n):
        if (np.random.binomial(1, p) + np.random.binomial(1, p)):
            A[i, j] = 1
            A[j, i] = 1

D = np.diag(A.sum(axis=1))              # 节点度矩阵
L = D - A                               # 邻接矩阵的拉普拉斯矩阵
d_max = D.max().item()                  # 节点度最大值
h = 0.99 / d_max                        # h参数
theta0 = np.random.normal(50, 10, n)    # 初始状态

def simulation_single(theta0, c, A, B, q):
    theta = theta0.copy()
    convergence = False
    q_powered = 1
    for k in range(max_iterations):
        b = c * q_powered
        eta = np.random.laplace(scale=b, size=n)
        next_theta = A @ theta + B @ eta

        if np.max(np.abs(next_theta - theta)) < threshold:
            convergence = True
            theta = next_theta
            break
        theta = next_theta
        q_powered *= q
    # J = (2 * delta ** 2 / n ** 2) * np.sum(theta ** 2)
    J = (2 / n**2) * np.sum((s**2 * c**2) / (1 - q**2))
    # convergence_time = np.max(np.mean(np.square(theta - np.mean(theta0))) / np.mean(np.square(theta0 - np.mean(theta0)))) ** (1 / (2 * k))
    return (k if convergence else max_iterations), J

def simulate_s(s):
    q = alpha + (1 - alpha) * abs(s - 1)
    c = (delta * q) / (epsilon * (q - abs(s - 1)))
    A = np.eye(n) - h * L
    B = s * np.eye(n) - h * L
    
    results = Parallel(n_jobs=-1, verbose=0)(
        delayed(simulation_single)(theta0, c, A, B, q)
        for _ in range(num_simulations)
    )

    convergece_times = [res[0] for res in results]
    Js = [res[1] for res in results]

    return np.mean(convergece_times), Js

if __name__ == '__main__':
    s_values = np.logspace(0.8, 1.2, 50)
    times, vs = [], []

    for s in tqdm(s_values):
        t, var = simulate_s(s)
        times.append(t); vs.append(var)

    plt.figure(figsize=(10, 6))
    plt.subplot(2, 1, 1)
    plt.plot(s_values, vs, label='var')
    plt.xlabel('s'); plt.ylabel('var')
    plt.xlim(0.8, 1.2); plt.grid(True)
    plt.xticks(np.arange(0.8, 1.2, 0.05))

    plt.subplot(2, 1, 2)
    plt.plot(s_values, times, label='times')
    plt.xlabel('s'); plt.ylabel('times')
    plt.xlim(0.8, 1.2); plt.grid(True)
    plt.xticks(np.arange(0.8, 1.2, 0.05))

    plt.tight_layout()
    plt.show()
    