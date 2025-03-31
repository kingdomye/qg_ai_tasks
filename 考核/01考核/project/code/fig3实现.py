import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse.csgraph import connected_components

# 固定随机种子
np.random.seed(42)

# 生成邻接矩阵A
n = 200
A = np.zeros((n, n))
for i in range(n):
    for j in range(i+1, n):
        b1 = np.random.binomial(1, 0.1)
        b2 = np.random.binomial(1, 0.1)
        A[i, j] = b1 + b2
        A[j, i] = A[i, j]  # 对称矩阵

# 检查图的连通性
n_components, _ = connected_components(A, directed=False)
assert n_components == 1, "生成的图不连通，请调整随机种子或参数"

# 计算拉普拉斯矩阵和步长
D = np.diag(np.sum(A, axis=1))
L = D - A
d_max = np.max(np.sum(A, axis=1))
h = 0.9 / d_max  # 步长设置

# 生成初始状态
np.random.seed(1200003)
theta0 = np.random.normal(loc=50, scale=10, size=n)
true_average = np.mean(theta0)

# 参数设置
delta = 1.0
epsilon = 0.1
num_simulations = 100  # 模拟次数
max_steps = 1000         # 最大迭代步数
tolerance = 1e-2         # 收敛阈值

# 生成s值（对数刻度）
s_values = np.exp(np.linspace(np.log(0.8), np.log(1.2), 100))
# s_values = np.exp(np.linspace(0.8, 1.2, 20))

# 存储结果
std_devs = []
settling_times = []

for s in s_values:
    # 计算噪声参数
    alpha = 1e-6
    q = alpha + (1 - alpha) * abs(s - 1)
    denominator = q - abs(s - 1)
    c = (delta * q) / (epsilon * denominator)
    S = s * np.eye(n)
    
    theta_infty_samples = []
    sim_settling_times = []
    
    # 并行优化建议：此处可改用多进程加速
    s_index = s_values.tolist().index(s)
    for sim in range(num_simulations):
        if (sim+1) % 100 == 0:
            print(f"Processing s={s_index}/{len(s_values)}, simulation {sim+1}/{num_simulations}...")
        np.random.seed(sim)  # 每次模拟独立种子
        theta = theta0.copy()
        converged = False
        
        for k in range(max_steps):
            # 生成拉普拉斯噪声
            b = c * (q ** k)
            eta = np.random.laplace(loc=0, scale=b, size=n)
            
            # 向量化状态更新
            x = theta + eta
            theta_next = theta - h * L @ x + S @ eta
            
            # 计算收敛条件
            error = np.linalg.norm(theta_next - np.mean(theta_next))
            if error < tolerance:
                sim_settling_times.append(k+1)
                converged = True
                break
            theta = theta_next
        
        if not converged:
            sim_settling_times.append(max_steps)
        
        # 记录最终平均值
        theta_infty_samples.append(np.mean(theta))
    
    # 计算统计量
    std_devs.append(np.std(theta_infty_samples))
    settling_times.append(np.mean(sim_settling_times))

# 绘图
plt.figure(figsize=(12, 5))

# 图3(a): 经验标准差
plt.subplot(121)
plt.semilogx(s_values, std_devs, 'bo-', markersize=5)
plt.xlabel('s (log scale)')
plt.ylabel('Empirical Standard Deviation')
plt.title('Fig 3(a): Standard Deviation vs. s')

# 图3(b): 收敛时间
plt.subplot(122)
plt.semilogx(s_values, settling_times, 'ro-', markersize=5)
plt.xlabel('s (log scale)')
plt.ylabel('Settling Time (steps)')
plt.title('Fig 3(b): Settling Time vs. s')

plt.tight_layout()
plt.show()