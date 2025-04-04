import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigvals

# 参数设置
n = 50
delta = 1
epsilon = 0.1
s = 0.9
q = 0.2
num_trials = 50
max_iter = 100

# 生成邻接矩阵（两次伯努利试验）
np.random.seed(42)
A = np.random.binomial(1, 0.1, (n,n)) + np.random.binomial(1, 0.1, (n,n))
A = np.triu(A, 1) + np.triu(A, 1).T
D = np.diag(A.sum(axis=1))
L = D - A
d_max = D.max().astype(float)
h = 0.99 / d_max  # 步长满足h < 1/d_max

# 理论收敛率计算
A_matrix = np.eye(n) - h * L
Pi_n = np.ones((n,n)) / n
A_tilde = A_matrix - Pi_n
eigenvalues = np.abs(eigvals(A_tilde))
lambda_bar = eigenvalues.max()
mu_theory = max(q, lambda_bar)

# 初始化存储
errors = np.zeros((num_trials, max_iter))
abs_term = np.abs(s - 1)
denominator = q - abs_term
c = (delta * q) / (epsilon * denominator)  # c_i计算

for trial in range(num_trials):
    theta = np.random.normal(50, 10, n)
    theta_true = theta.copy()
    
    # 动态计算θ∞理论值（假设已知初始平均）
    theta_avg_initial = theta.mean()
    noise_series = [np.random.laplace(0, c*(q**k), n) for k in range(1000)]
    theta_inf = theta_avg_initial + (s/n) * sum([noise.sum() for noise in noise_series])/1000
    
    # 迭代更新
    for k in range(max_iter):
        # 生成噪声η(k)
        # scale = c * (q ​** k)
        scale = c * (q ** k)
        eta = np.random.laplace(0, scale, n)
        
        # 消息生成与状态更新
        x = theta + eta
        S = s * np.eye(n)
        B = S - h * L
        theta = (np.eye(n) - S) @ theta + B @ x  # 正确矩阵运算
        
        # 计算误差（对比动态θ_inf）
        current_avg = theta.mean()
        # error = np.linalg.norm(theta - current_avg * np.ones(n)) ​** 2
        error = np.linalg.norm(theta - current_avg * np.ones(n)) ** 2
        errors[trial, k] = error
    
    # 归一化误差
    # initial_error = np.linalg.norm(theta_true - theta_true.mean() * np.ones(n)) ​** 2
    initial_error = np.linalg.norm(theta_true - theta_true.mean() * np.ones(n)) ** 2
    errors[trial] /= initial_error

# 计算经验收敛率
k_vals = np.arange(1, max_iter+1)
mu_empirical = np.zeros(max_iter)
for k in range(max_iter):
    avg_ratio = np.mean(errors[:,k])
    # mu_empirical[k] = avg_ratio ​** (1/(2*(k+1)))
    mu_empirical[k] = avg_ratio ** (1/(2*(k+1)))

# 绘图
plt.figure(figsize=(10,6))
plt.plot(k_vals, mu_empirical, label='Empirical μ')
plt.axhline(mu_theory, color='r', linestyle='--', label='Theoretical μ')
plt.xlabel('Iteration k')
plt.ylabel('Convergence Rate')
plt.legend()
plt.grid(True)
plt.title('Corrected Convergence Rate Validation')
plt.show()