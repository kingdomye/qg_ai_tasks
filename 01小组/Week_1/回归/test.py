import numpy as np

# 创建一个形状为(4, )的数组
a = np.array([1, 2, 3, 4])

# 创建一个形状为(80, 4)的数组
b = np.random.rand(80, 4)

# 将a转换为列向量
a_col = a.reshape(4, 1)

# 将b的每一行与a_col进行点乘
c = np.dot(b, a_col)

# 将c与a进行点乘
d = c * a

# 检查结果的形状
print(d)  # 输出: (80, 4)