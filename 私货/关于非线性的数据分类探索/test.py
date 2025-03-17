import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

df = pd.read_csv('banana.dat', header=None)
x = df.iloc[:, :2].values
y = df.iloc[:, 2].values.ravel()
plt.scatter(x[:, 0], x[:, 1], c=y)
plt.show()
