# Differentially private average consensus Obstructions, trade-offs, and optimal algorithm design

> 作者：Erfan Nozari$^{a}$、Pavankumar Tallapragada$^{b}$、Jorge Cortés$^{a}$
> 机构：
>
> $^{a}$Department of Mechanical and Aerospace Engineering, University of California,
>
> $^{b}$San Diego、Department of Electrical Engineering, Indian Institute of Science

## 研究问题 Research Question

### 科学问题 Science Question

针对可以访问系统所有信息的攻击者，本文设计了一种满足差分隐私要求的算法，使得系统内的各智能体几乎可以收敛到初始值的平均值的无偏估计（或者说最后的期望值的平均值与初始值平均值相同），并且讨论了参数的权衡与最优选择。

### 研究核心 Core of the research

- 分析算法最终的收敛状态（不可能达到初始状态的平均值）；

- 权衡网络的隐私性与准确性；
- 最佳噪声参数选择。

### 研究意义 Research significance

- 适用于网络系统，在保护隐私的同时，对系统的整体输出不会有明显的影响；即对隐私和准确性做到了权衡；
- 用于未来设计用于保护网络结构以及参数的算法。

### 现有方法的不足 Shortcomings of existing algorithm

- 首先是文章反复在强调的：无法完全权衡差分隐私与精确收敛；
- Huang等人提出的算法收敛点的期望值取决于网络结构；本文涉及的算法具有几乎必然收敛性，且收敛速度有明确的表明；
- 没有考虑动态平均共识，这同时也是作者的未来研究工作方向。

### 结论 Conclusion

- 证明了系统不能最终准确的收敛到初始状态的平均值；
- 而最终收敛状态的期望值是初始状态平均值的无偏估计；
- 分析了算法的收敛性以及准确性。

---

## 理论与方法 Theory and Method

| 理论                                                         | 方法                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 任何满足差分隐私共识的算法都无法保证最终收敛到初始状态的精确平均值 | 利用差分隐私的定义，发现其与收敛性矛盾                       |
| 收敛性分析                                                   | 利用系统动态方程(论文中式12~14)进行收敛性证明                |
| 最优噪声参数选择                                             | 在固定差分隐私参数的条件下，最小化收敛点的方差值，最后证明s=1时达到下界，并且和网络拓扑结构无关 |

---

## 实验 Experiment

针对论文，笔者做了三个论文相关实验，分别对应模拟实验的fig1、fig3、fig4

| 实验             | 相关内容及结论 |
| ---------------- | -------------- |
| 实验一，对应fig1 |                |
| 实验二，对应fig3 |                |
| 实验三，对应fig4 |                |

---

## 总结与思考 Summary and Reflections

