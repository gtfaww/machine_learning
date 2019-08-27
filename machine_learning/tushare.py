#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

import pandas as pd
from pyecharts.charts import Line

__author__ = 'guotengfei'
__time__ = 2019 / 8 / 24

"""
std
"""

LOGGER = logging.getLogger(__name__)

if __name__ == '__main__':
    df = pd.read_csv('C:/git/machine_learning/machine_learning/data/资料01_商铺数据(2)(9).csv')

    df1 = df[df['comment'].str.contains('条')]
    df1['comment'] = df1['comment'].str.split(' ').str[0]
    df1['comment'] = df1['comment'].astype('int')

    df1 = df[df['price'].str.contains('￥')]
    df1['price'] = df1['price'].str.split('￥').str[-1]
    df1['price'] = df1['price'].astype('float')
    df1 = df1[df1['price'] > 50]

    import tushare as ts

    df = ts.get_day_all()
    df = df.round(2)

    df2 = ts.get_hist_data('600848')
    x = df2.index.tolist()[:20]
    y = df2[['open', 'close', 'low', 'high']]
    y1 = df2['open'].iloc[:20]
    ma5 = df2['ma5']
    ma10 = df2['ma10']
    ma20 = df2['ma20']

    line = Line("我的第一个图表", "这里是副标题", width="800px", height="400px")
    line.add('开盘价', x, y1)
    line.render('C:/git/machine_learning/machine_learning/data/1.html')
