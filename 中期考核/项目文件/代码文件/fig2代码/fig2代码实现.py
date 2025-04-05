import numpy as np
from matplotlib import pyplot as plt

p = 0.1         # 生成边的概率

data = np.load('../data/B/init_positions.npy')
plt.scatter(data[:, 0], data[:, 1])

for i in range(len(data)):
    for j in range(i + 1, len(data)):
        if (np.random.binomial(1, p) + np.random.binomial(1, p)):
            plt.plot([data[i, 0], data[j, 0]], [data[i, 1], data[j, 1]], alpha=0.1)
plt.show()
