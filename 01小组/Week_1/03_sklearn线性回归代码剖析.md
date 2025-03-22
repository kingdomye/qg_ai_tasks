# sklearn线性回归代码剖析

Written by ricckker 2025/3/21 Guangdong·Guangzhou

Let's take a look at the introduction to linear regression in the code:

```python
'''
Ordinary least squares Linear Regression.

LinearRegression fits a linear model with coefficients w = (w1, ..., wp)
to minimize the residual sum of squares between the observed targets in
the dataset, and the targets predicted by the linear approximation.
'''
```

以上是关于普通最小二乘法的介绍，我们可以用一条简洁且美妙的公式来总结，即是：

```math
\underset{\omega }{min} \left \|X\omega -y  \right \| _{2}^{2} 
```

观察sklearn库的LinearRegression类代码介绍，我们可以发现LinearRegression类具有以下几种属性：

```python
Parameters
----------
fit_intercept : bool, default=True
    Whether to calculate the intercept for this model. If set
    to False, no intercept will be used in calculations
    (i.e. data is expected to be centered).

copy_X : bool, default=True
    If True, X will be copied; else, it may be overwritten.

n_jobs : int, default=None
    The number of jobs to use for the computation. This will only provide
    speedup in case of sufficiently large problems, that is if firstly
    `n_targets > 1` and secondly `X` is sparse or if `positive` is set
    to `True`. ``None`` means 1 unless in a
    :obj:`joblib.parallel_backend` context. ``-1`` means using all
    processors. See :term:`Glossary <n_jobs>` for more details.

positive : bool, default=False
    When set to ``True``, forces the coefficients to be positive. This
    option is only supported for dense arrays.
```

总结成表格即是：

| 属性                | 含义                                                         |
| ------------------- | ------------------------------------------------------------ |
| fit_intercept(bool) | 确定模型是否需要偏置项bias，当数据均值不为0时，可以提高拟合效果，默认为True |
| copy_X(bool)        | 输入数据会被复制一份，保证数据的安全性，默认为True           |
| n_jobs(int)         | 控制用于计算的作业数量，针对庞大的数据集可以加速模型处理     |
| positive(bool)      | 决定回归系数是否强制为正/负，默认为False，即允许变量之间为正相关或负相关 |

至此，对比[我的代码](../code/W1_T2_回归/02线性回归.py)可以发现，sklearn库在**数据的规模大小、安全性以及程序运行的效率**上做了考虑，在训练一个模型时，能保证数据的安全性并且保障程序性能；

下面来看LinearRegression类中的方法fit，用于训练模型，当然在代码介绍中也提到，该模型适用于普通最小二乘法或是非负最小二乘法；

fit方法的参数如下，同样的，也是由**输入、输出及模型参数**构成，就不再赘述：

```python
Parameters
----------
X : {array-like, sparse matrix} of shape (n_samples, n_features)
    Training data.

y : array-like of shape (n_samples,) or (n_samples, n_targets)
    Target values. Will be cast to X's dtype if necessary.

sample_weight : array-like of shape (n_samples,), default=None
    Individual weights for each sample.
```

fit方法的返回值是一个模型对象，下面来看fit方法的数学逻辑；

- fit方法中也有考虑对于程序性能的优化，在进行计算之前，首先验证模型参数（包括参数矩阵形状、非负性）确保模型参数符合要求，避免了输入数据错误所导致的运行错误
- 判断了输入数据X是否需要预处理，能够起到保护数据和节省内存的作用
- 根据positive参数，决定模型是否使用非负最小二乘法计算模型的参数
- 对于多变量和单变量、模型是否具有参数，fit方法都定义了不同的计算函数，用于不同的场景
- **数学求解方法**：仔细观察代码发现fit方法调用了scipy.sparse.linalg.lsqr方法，**将问题转化为稀疏矩阵最小二乘问题**，在大规模的数据上计算更有效率，用于求解最小二乘的模型参数

【总结】综合上述对LinearRegression类的观察与探索，对比个人代码，可以发现sklearn库在**程序性能、错误处理**等方面有充分的考虑。

------

下面我们定位到scipy库，观察scipy.sparse.linalg.lsqr方法是如何处理最小二乘问题的(关于lsqr的源代码可以定位到[lsqr源代码](../code/W1_T2_回归/05lsqr源代码.py))；

全局观察，lsqr包含两个函数_sym_ortho和lsqr主函数，分别实现吉文斯旋转计算和稀疏矩阵最小二乘法，我们重点研究主函数**lsqr**的数学逻辑，其流程大致如下（更加具体的数学逻辑需要更深入的学习，碍于个人能力不作讨论）：

- 将输入数据矩阵A转化为双对角化得到矩阵B
- 防止病态问题发生，对模型进行正则化处理，对矩阵B的元素进行调整
- 判断迭代过程是否收敛

------

执笔至此，不难发现手推的代码和sklearn库中LinearRegression类关于线性回归方程的求解方法无论在数据处理或是数学逻辑上都相差甚远，以下是对手推代码优化的几点可行方案：

- 对数据进行预处理，增强代码的错误处理能力
- 手推代码只适合小型数据的处理，对于更大型的数据集，可以学习lsqr算法，提供更加高效和优雅的求解方法
