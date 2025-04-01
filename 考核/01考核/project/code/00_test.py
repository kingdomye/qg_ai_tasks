import numpy as np
from matplotlib import pyplot as plt

# 加载数据
load_arr = np.load('./data/B/init_positions.npy')
x = load_arr[:, 0]
y = load_arr[:, 1]

# 抽取50个点
random_indices = np.random.choice(len(x), 100, replace=False)
x = x[random_indices]
y = y[random_indices]

# 创建一个新的图形
plt.figure()

# 绘制每个点
plt.scatter(x, y, color='red', label='Points')

# 将每个点与其他所有点用线连接
for i in range(len(x)):
    for j in range(i + 1, len(x)):
        plt.plot([x[i], x[j]], [y[i], y[j]], color='blue', linestyle='-', linewidth=0.02, alpha=0.5)

# 添加标签和标题
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.title('Fully Connected Points Plot')
plt.legend()
plt.grid(True)

# 显示图形
plt.show()