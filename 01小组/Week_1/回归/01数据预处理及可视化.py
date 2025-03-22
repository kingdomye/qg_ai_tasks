import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns


file = './data/boston.csv'
data = pd.read_csv(file)


def normalize(X):
    """归一化：将数据缩放到 [0, 1] 范围内"""
    X_min = np.min(X, axis=0)
    X_max = np.max(X, axis=0)
    return (X - X_min) / (X_max - X_min)


def standardize(X):
    """标准化：将数据缩放到均值为 0，标准差为 1 的分布"""
    mean = np.mean(X, axis=0)
    std = np.std(X, axis=0)
    return (X - mean) / std


def draw_bars(dataFrame, label):
    """根据对应标签绘制条形图"""
    x = dataFrame.iloc[:, -1]
    y = dataFrame[label]
    y = normalize(y)
    plt.bar(x, y)
    plt.show()


def boston_medv_bars():
    """波士顿房价直方图"""
    sns.displot(data['MEDV'], bins=30, kde=True)
    plt.show()


def boston_boxplot():
    """波士顿房价箱线图"""
    sns.boxplot(data=data)
    plt.show()


def pair_plot():
    """不同参数之间的关系图"""
    sns.pairplot(data)
    plt.show()


def crime_pies():
    """犯罪率饼图"""
    bins = [0, 0.1, 0.2, 0.5, 1, np.inf]
    labels = ['0-0.1', '0.1-0.2', '0.2-0.5', '0.5-1', '>1']
    categories = np.digitize(data['CRIM'], bins) - 1
    categories_count = np.bincount(categories)

    plt.figure(figsize=(12, 8))
    plt.pie(categories_count, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('Boston Crime Pie')
    plt.show()


def heat_map():
    """协方差矩阵热力图"""
    corr = data.corr()
    plt.figure(figsize=(12, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
    plt.show()


if __name__ == '__main__':
    heat_map()
