import numpy as np
from matplotlib import pyplot as plt

load_arr = np.load('./data/B/init_positions.npy')
x = load_arr[:, 0]
y = load_arr[:, 1]

plt.scatter(x, y)
plt.show()
