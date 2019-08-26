#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import re

import pandas as pd
import requests
import matplotlib.pyplot as plt

import seaborn as sns
from bs4 import BeautifulSoup

plt.style.use('ggplot')

import numpy as np

__author__ = 'guotengfei'
__time__ = 2019 / 8 / 24

"""
Module comment
"""

LOGGER = logging.getLogger(__name__)

if __name__ == '__main__':
    result = requests.get('https://book.douban.com/tag/%E6%BC%AB%E7%94%BB')
    print(result.text)

    soup = BeautifulSoup(result.text, 'lxml')
    soup.find('div', id='content').h1.text

    lis = soup.find('ul', class_='subject-list').find_all('li')
    print(lis)

    data_list = []
    for li in lis:
        data = {}
        data['书名'] = li.find('div', class_="info").h2.text.replace(' ', '').replace('\n', '')
        data['其他信息'] = li.find('div', class_="pub").text.replace(' ', '').replace('\n', '')
        data['评分'] = li.find('span', class_="rating_nums").text.replace(' ', '').replace('\n', '')
        data['评价人数'] = re.search(r'(\d*)人', li.find('span', class_="pl").text.replace(' ', '').replace('\n', '')).group(
            1)
        data_list.append(data)

    df = pd.DataFrame(data_list)
