# sklearn线性回归代码剖析

Let's take a look at the introduction to linear regression in the code:

```python
'''
Ordinary least squares Linear Regression.

LinearRegression fits a linear model with coefficients w = (w1, ..., wp)
to minimize the residual sum of squares between the observed targets in
the dataset, and the targets predicted by the linear approximation.
'''
```

以上是关于普通最小二乘法的介绍，我们可以用一条简洁且美妙的公式来表达，即：

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

    .. versionadded:: 0.24
```

总结成表格即是：

| 属性                | 含义                                                         |
| ------------------- | ------------------------------------------------------------ |
| fit_intercept(bool) | 确定模型是否需要偏置项bias，当数据均值不为0时，可以提高拟合效果，默认为True |
| copy_X(bool)        | 输入数据会被复制一份，保证数据的安全性，默认为True           |
| n_jobs(int)         | 控制用于计算的作业数量，针对庞大的数据集可以加速模型处理     |
| positive(bool)      | 决定回归系数是否强制为正/负，默认为False，即允许变量之间为正相关或负相关 |

至此，对比[我的代码](../code/W1_T2_回归/02线性回归.py)可以发现，sklearn库在**数据的规模大小、安全性以及程序运行的效率**上做了考虑，在训练一个模型时，能保证数据的安全性并且保障程序的运行速度；

同时，类中有一个方法fit，用于训练该模型，当然在代码介绍中也提到，该模型适用于普通最小二乘法或是非负最小二乘法
