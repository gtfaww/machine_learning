#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

import numpy as np

__author__ = 'guotengfei'
__time__ = 2019 / 8 / 24

"""
Module comment
"""

LOGGER = logging.getLogger(__name__)

if __name__ == '__main__':

    # 计算内部收益率
    l = []
    l.append(-50000)
    # l.append(1015.07)
    for i in range(0, 11):
        l.append(465)
    l.append(50465)
    print(l)
    irr = round(np.irr(l), 5)
    print("内部收益率IRR = {}%".format(irr * 100))

    # 计算年化收益率（复利公式）
    pa = round((irr + 1) ** 12 - 1, 4)
    print("实际年化贷款利率 = {}%".format(pa * 100))
