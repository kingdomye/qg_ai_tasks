# K-means类封装实验报告

**【问题描述】**

鸢尾花数据集（Iris Dataset）由英国生物学家和统计学家 Ronald A. Fisher 于 1936 年在他的论文《The use of multiple measurements in taxonomic problems》中首次引入。这个数据集包含了 150 个鸢尾花样本，每个样本有 4 个特征和 1 个目标变量。

数据集指标名称和含义如下表：

| 标签         | 含义     |
| ------------ | -------- |
| sepal length | 花萼长度 |
| sepal width  | 花萼宽度 |
| petal length | 花瓣长度 |
| petal width  | 花瓣宽度 |

目标变量：鸢尾花的品种，有三种类别：山鸢尾（Iris Setosa）、变色鸢尾（Iris Versicolour）以及 维吉尼亚鸢尾（Iris Virginica）

------

**【算法思路】**

**1、选择K值**：设定簇的数量 K = 3

**2、初始化簇中心**：从数据集中随机抽取三组数据作为初始簇中心

**3、分配步骤**：对于数据集中的每个点，将它分配到最近的簇中心对应的簇。这里的“距离”通常使用欧氏距离

**4、更新步骤**：根据当前的簇分配，重新计算每个簇的中心，即计算簇内所有点的均值作为新的簇中心。

**5、重复3、4**：不断重复分配和更新步骤，达到指定的最大迭代次数100次。

------

### 代码实现

代码所需库：

```python
import pandas as pd
import numpy as np
import random
from matplotlib import pyplot as plt
```

计算点与簇中心的欧氏距离：

```python
def calculate_distance(x, y):
    distance = np.linalg.norm(x - y)
    return distance
```

K-means类的封装

包含文件读取、数据切分、更新簇中心、分类主函数

```python
class KMeans:
    def __init__(self, n_clusters=3, max_iter=100):
        self.data = None
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.X = None
        self.Y = None

    def read_data(self, filename="./iris_data/iris.csv"):
        self.data = pd.read_csv(filename)
        self.X, self.Y = self.data.iloc[:, 1: -1], self.data.iloc[:, -1]
        self.X = self.X.values

    def get_clusters(self, clusters_center):
        distances = np.linalg.norm(self.X[:, np.newaxis] - clusters_center, axis=2)
        new_clusters = np.argmin(distances, axis=1)
        return new_clusters

    def update_clusters(self, new_clusters):
        new_center = []
        for i in range(self.n_clusters):
            sum = np.zeros(self.X.shape[1])
            cnt = 0
            for j in range(self.X.shape[0]):
                if new_clusters[j] == i:
                    cnt += 1
                    sum += self.X[j]
            mean = sum / cnt
            new_center.append(mean)
        new_center = np.array(new_center)
        return new_center

    def classify(self):
        clusters_center = np.array(random.sample(self.X.tolist(), self.n_clusters))
        print(clusters_center)

        for _ in range(self.max_iter):
            new_clusters = self.get_clusters(clusters_center)
            clusters_center = self.update_clusters(new_clusters)
            print(clusters_center)
```

------

**【模型评估】**

本次模型评估采用**准确率（Accuracy）**评估：正确预测的样本数占总样本数的比例。

程序运行结束，我们输出以最终簇中心为准分类的数据classify_distance：

```python
[2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
 2 2 2 2 2 2 2 2 2 2 2 2 2 0 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 0 0 0 0 1 0 0 0 0
 0 0 1 1 0 0 0 0 1 0 1 0 1 0 0 1 1 0 0 0 0 0 1 0 0 0 0 1 0 0 0 1 0 0 0 1 0
 0 1]
```

其中对应数字表示的花的种类如下表：

| 数字 | 种类       |
| ---- | ---------- |
| 0    | setosa     |
| 1    | versicolor |
| 2    | virginica  |

我们可以通过字典将其转换后计算该模型最终准确率：**89.3%**

