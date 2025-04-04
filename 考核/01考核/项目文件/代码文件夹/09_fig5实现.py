import numpy as np
import matplotlib.pyplot as plt

# 参数设置
n = 50          # 节点数
delta = 1       # 邻接边界
epsilon = 0.1   # 隐私参数
s = 1           # S矩阵对角线元素
q = 0.0         # 噪声衰减率（实际设为0）
num_runs = 10**6 # 运行次数

# 计算c_i（命题5.10）
c = delta / epsilon  # 当s=1时，c_i=delta/(epsilon)

# 生成初始状态θ0 ~ N(50, 10^2)
true_mean = 50
theta0 = np.random.normal(loc=true_mean, scale=10, size=(num_runs, n))

# 计算真实平均Ave(θ0)
true_ave = theta0.mean(axis=1)

# 生成拉普拉斯噪声η_i ~ Lap(c)
noise = np.random.laplace(loc=0, scale=c, size=(num_runs, n))

# 计算θ∞ = Ave(θ0) + sum(s_i * η_i)/n
theta_inf = true_ave + noise.sum(axis=1) / n

# 绘制直方图
plt.figure(figsize=(10,6))
plt.hist(theta_inf, bins=100, density=True, alpha=0.7, label='Empirical')
plt.axvline(true_mean, color='r', linestyle='dashed', linewidth=2, label='True Mean')
plt.xlabel('θ∞')
plt.ylabel('Density')
plt.title('Histogram of θ∞ (n=50, 1e6 runs)')
plt.legend()
plt.grid(True)
plt.show()

# 计算均值和标准差
print(f"Sample Mean: {theta_inf.mean():.4f}, Theoretical Mean: {true_mean}")
print(f"Sample Std: {theta_inf.std():.4f}, Theoretical Std: {np.sqrt(200/n):.4f}")