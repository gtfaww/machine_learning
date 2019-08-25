#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

import pandas as pd
import requests
import matplotlib.pyplot as plt

import seaborn as sns

plt.style.use('ggplot')

import numpy as np

__author__ = 'guotengfei'
__time__ = 2019 / 8 / 24

"""
Module comment
"""

LOGGER = logging.getLogger(__name__)


def get_data(file):
    r = requests.get('https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data')
    with open(file, 'w') as f:
        f.write(r.text)


if __name__ == '__main__':
    PATH = r'C:/git/machine_learning/machine_learning/data/'
    file = PATH + 'iris.data'

    # get_data(file)

    # os.chdir(PATH)
    names = ['sepal length', 'sepal width', 'petal length', 'petal width', 'class']
    df = pd.read_csv(file, names=names)
    print(df.head())
    print(df['sepal length'])
    print(df.ix[:3, :2])
    print(df.loc[:3, :])
    print(df.loc[:3, names[:2]])
    print(df.loc[:3, [x for x in df.columns if 'width' in x]])
    print(df['class'].unique())
    print(df[df['class'] == 'Iris-versicolor'])
    print(df.count())
    print(df[df['class'] == 'Iris-versicolor'].count())

    versicolor = df[df['class'] == 'Iris-versicolor'].reset_index(drop=True)
    print(versicolor)

    print(df[(df['class'] == 'Iris-versicolor') & (df['petal width'] > 1.0)])

    print(df.describe(percentiles=[.50, .80, .95]))  # 描述性统计信息

    print(df.corr())  # 相关系数信息
    print(df.corr(method="spearman"))  # 相关系数信息
    print(df.corr(method="kendall"))  # 相关系数信息

    # 绘图
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(df['petal width'])
    ax.set_ylabel('Count', fontsize=12)
    ax.set_xlabel('Width', fontsize=12)
    plt.title('Iris Petal Width', fontsize=14, y=1.01)
    plt.tight_layout()

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(df['petal length'])
    ax.set_ylabel('Specimen Number', fontsize=12)
    ax.set_xlabel('Petal Length', fontsize=12)
    plt.title('Petal Length Plot', fontsize=14, y=1.01)

    fig, ax = plt.subplots(figsize=(6, 6))
    bar_width = .8
    labels = [x for x in df.columns if 'length' in x or 'width' in x]
    ver_y = [df[df['class'] == 'Iris-versicolor'][x].mean() for x in labels]
    vir_y = [df[df['class'] == 'Iris-virginica'][x].mean() for x in labels]
    set_y = [df[df['class'] == 'Iris-setosa'][x].mean() for x in labels]
    x = np.arange(len(labels))
    ax.bar(x, vir_y, bar_width, bottom=set_y, color='darkgrey')
    ax.bar(x, set_y, bar_width, bottom=ver_y, color='white')
    ax.bar(x, ver_y, bar_width, color='black')
    ax.set_xticks(x + (bar_width / 2))
    ax.set_xticklabels(labels, rotation=-70, fontsize=12)
    ax.set_title('Mean Feature Measurement By Class', y=1.01)
    ax.legend(['Virginica', 'Setosa', 'Versicolor'])

    fig, ax = plt.subplots(2, 2, figsize=(7, 7))
    sns.set(style='white', palette='muted')
    sns.violinplot(x=df['class'], y=df['sepal length'], ax=ax[0, 0])
    sns.violinplot(x=df['class'], y=df['sepal width'], ax=ax[0, 1])
    sns.violinplot(x=df['class'], y=df['petal length'], ax=ax[1, 0])
    sns.violinplot(x=df['class'], y=df['petal width'], ax=ax[1, 1])
    fig.suptitle('Violin Plots', fontsize=16, y=1.03)
    for i in ax.flat:
        plt.setp(i.get_xticklabels(), rotation=-90)
    fig.tight_layout()

    df.groupby('class')['petal width'].agg({'delta': lambda x: x.max() - x.min(), 'max': np.max, 'min': np.min})

    import statsmodels.api as sm

    y = df['sepal length'][:50]
    x = df['sepal width'][:50]
    X = sm.add_constant(x)

    results = sm.OLS(y, X).fit()
    print(results.summary())
