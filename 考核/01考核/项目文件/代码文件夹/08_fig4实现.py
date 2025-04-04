import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

# =====================
# 1. 参数初始化
# =====================
np.random.seed(42)  
n = 50               # 代理数量
delta = 1.0          # 相邻状态差异上限
true_avg = 50.0      # 真实平均值（固定值方便可视化）
num_epsilons = 20    # ε采样点数
num_runs = 25        # 每个ε的仿真次数
max_iter = 1000      # 最大迭代次数
tol = 1e-2           # 收敛阈值

# 生成ε对数采样（10^-2到10^2）
epsilons = np.logspace(-2, 2, num_epsilons)

# =====================
# 2. 网络拓扑生成（同图3）
# =====================
def generate_network(n_nodes=50, p=0.1):
    A = np.ones((n_nodes, n_nodes))
    A = A * (np.random.binomial(1, p, (n_nodes, n_nodes)) + np.random.binomial(1, p, (n_nodes, n_nodes)))
    A = (A + A.T) / 2
    np.fill_diagonal(A, 0)
    D = np.diag(A.sum(axis=1))
    L = D - A
    return L

L = generate_network(n)

# =====================
# 3. 修改后的共识算法（单次噪声注入）
# =====================
def one_shot_consensus(theta0, L, epsilon, max_iter=1000):
    """s=1, q=0的单次扰动算法"""
    n = len(theta0)
    c = delta / epsilon  # 理论最优参数
    
    # 初始噪声注入（仅k=0时刻）
    eta0 = np.random.laplace(scale=c, size=n)
    theta = theta0.copy() + eta0
    
    # 纯拉普拉斯共识（无后续噪声）
    h = 0.99 / np.max(np.diag(L))  # 稳定步长
    A = np.eye(n) - h * L
    
    for _ in range(max_iter):
        new_theta = A @ theta
        if np.linalg.norm(new_theta - theta) < tol:
            break
        theta = new_theta
    
    return theta.mean()  # 返回最终平均值

# =====================
# 4. 运行仿真收集数据
# =====================
# 存储结果
errors = []
variances = []
theoretical_var = []

# 固定初始状态（便于比较）
theta0 = np.random.normal(50, 10, n)  # 均值为50，标准差10

for eps in tqdm(epsilons):
    # 运行多次实验
    final_avgs = []
    for _ in range(num_runs):
        final_avg = one_shot_consensus(theta0, L, epsilon=eps, max_iter=max_iter)
        final_avgs.append(final_avg)
    
    # 记录结果
    errors.extend([(avg - true_avg) for avg in final_avgs])
    variances.append(np.var(final_avgs))
    theoretical_var.append(2 * delta**2 / (n * eps**2))  # 理论公式

# =====================
# 5. 可视化结果
# =====================
plt.figure(figsize=(12, 5))

# 图4(a): 误差散点图
plt.subplot(121)
for i, eps in enumerate(epsilons):
    plt.scatter([eps]*num_runs, 
                np.array(errors[i*num_runs : (i+1)*num_runs]), 
                s=20, alpha=0.6,
                c=plt.cm.viridis(np.log10(eps)/2 + 0.5))  # 颜色映射
    
plt.xscale('log')
plt.xlabel('$\epsilon$ (log scale)')
plt.ylabel('$\\theta_{\\infty} - \\mathrm{Ave}(\\theta_0)$')
plt.title('a) Estimation Error vs Privacy Level')
plt.grid(True, which='both', linestyle='--')

# 图4(b): 方差对比
plt.subplot(122)
plt.plot(epsilons, variances, 'ro', label='Empirical Variance', alpha=0.7)
plt.plot(epsilons, theoretical_var, 'k--', lw=2, label='Theoretical Bound')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('$\epsilon$ (log scale)')
plt.ylabel('Variance (log scale)')
plt.title('b) Privacy-Accuracy Trade-off')
plt.legend()
plt.grid(True, which='both', linestyle='--')

plt.tight_layout()
plt.show()