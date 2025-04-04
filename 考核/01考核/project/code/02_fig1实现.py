import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def phi(alpha, s):
    a = s ** 2 * (alpha + (1 - alpha) * abs(s - 1)) ** 2
    b = (alpha ** 2 * (1 - abs(s - 1)) ** 2) * (1 - (alpha + (1 - alpha) * abs(s - 1)) ** 2)
    
    # 避免除以零
    if b == 0:
        return np.nan  # 返回 NaN 或其他特殊值
    return a / b

def phi2(alpha, s):
    a = (alpha + (1 - alpha) * abs(s - 1)) * s
    b = alpha * (1 - abs(s - 1))
    if b == 0:
        return np.nan  # 返回 NaN 或其他特殊值
    return a / b

# 绘制phi图像
alpha_arr = np.linspace(0.01, 0.99, 1000)
s_arr = np.linspace(0.01, 1.99, 1000)

# 创建网格
X, Y = np.meshgrid(alpha_arr, s_arr)

# 计算phi值
phi_arr = []
for i in range(len(s_arr)):
    phi_row = []
    for j in range(len(alpha_arr)):
        phi_row.append(min(7, phi(alpha_arr[j], s_arr[i])))
    phi_arr.append(phi_row)
phi_arr = np.array(phi_arr)

# 绘制三维图像
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# 绘制曲面
ax.plot_surface(X, Y, phi_arr, cmap='viridis', edgecolor='none')

# 设置轴标签
ax.set_xlabel('alpha')
ax.set_ylabel('s')
ax.set_zlabel('phi')

# 设置刻度间隔
ax.set_xticks(np.arange(0, 1.1, 0.5))  # x轴间隔为0.5
ax.set_yticks(np.arange(0, 2.1, 0.2))  # y轴间隔为0.2

# 显示图像
plt.show()