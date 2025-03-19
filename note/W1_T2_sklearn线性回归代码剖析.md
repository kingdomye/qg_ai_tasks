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
