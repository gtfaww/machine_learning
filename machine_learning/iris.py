#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

import pandas as pd
import requests
import matplotlib.pyplot as plt

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


