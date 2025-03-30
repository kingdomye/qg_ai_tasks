import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# 定义函数 phi
def phi(alpha, s):
    term = alpha + (1 - alpha) * np.abs(s - 1)
    return (s ** 2 * term ** 2) / (alpha ** 2 * (1 - np.abs(s - 1)) ** 2 * (1 - term ** 2))


# 创建参数网格
s = np.linspace(0.01, 1.99, 100)  # s ∈ (0, 2)
alpha = np.linspace(0.01, 0.99, 100)  # α ∈ (0, 1)
S, Alpha = np.meshgrid(s, alpha)

# 计算函数值
Phi = phi(Alpha, S)

# 绘制 3D 曲面图
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(S, Alpha, Phi, cmap='viridis', edgecolor='none')

# 添加颜色条
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10)

# 设置标签
ax.set_xlabel('s', labelpad=10)
ax.set_ylabel('α', labelpad=10)
ax.set_zlabel('φ(α, s)', labelpad=10)
ax.set_title('Local Objective Function φ(α, s)', pad=20)

# 显示图像
plt.show()
