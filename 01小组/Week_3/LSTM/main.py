import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = 'SimHei' # 设置中文显示
plt.rcParams['axes.unicode_minus'] = False

df_train = pd.read_csv('delhi_weather.csv', index_col=0, parse_dates=['date'])
df_test = pd.read_csv('delhi_weather.csv', index_col=0, parse_dates=['date'])
print(df_train)
