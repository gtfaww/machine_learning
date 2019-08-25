#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import logging
from math import radians, atan, tan, sin, cos, acos

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

__author__ = 'guotengfei'
__time__ = 2019 / 8 / 24

"""
std
"""

LOGGER = logging.getLogger(__name__)


def filter_drift_point(data):
    """
    过滤漂移点
    :return:
    """
    data = json.loads(data)['data']

    print(len(data))
    distances = []
    for i in range(0, len(data) - 1):
        distance = calc_distance(float(data[i]['lat']), float(data[i]['lng']), float(data[i + 1]['lat']),
                                 float(data[i + 1]['lng']))
        if distance * 1000 > 10.0:
            distances.append(distance * 1000)
    print(len(distances))
    print(distances)

    std = np.std(distances, ddof=1)
    print("std: {}".format(std))

    mean = np.mean(distances)
    print("mean: {}".format(mean))
    var = np.var(distances)
    print("var: {}".format(var))
    for distance in distances:
        if (mean - 2 * std) < distance < (mean + 2 * std):
            pass
        else:
            print(distance)
            print(distances.index(distance))

    se = pd.Series(distances)
    de = se.describe(percentiles=[.50, .75, .98])
    print(de)

    for distance in distances:
        if distance > de['98%']:
            print(distance)

    xy_df = pd.DataFrame(data)
    print(xy_df)
    print(xy_df[['lat', 'lng']])
    print(xy_df['lat'])
    print(xy_df['lng'])
    xy_df[['lat', 'lng']] = xy_df[['lat', 'lng']].astype(str)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(xy_df['lat'], xy_df['lng'], color='green')
    ax.set_xlabel('lat')
    ax.set_ylabel('lng')
    ax.set_title('gps Scatterplot')


def calc_distance(Lat_A, Lng_A, Lat_B, Lng_B):
    """
    计算两个点之间的距离

    :param Lat_A:
    :param Lng_A:
    :param Lat_B:
    :param Lng_B:
    :return:
    """
    ra = 6378.140
    rb = 6356.755
    flatten = (ra - rb) / ra
    rad_lat_A = radians(Lat_A)
    rad_lng_A = radians(Lng_A)
    rad_lat_B = radians(Lat_B)
    rad_lng_B = radians(Lng_B)
    pA = atan(rb / ra * tan(rad_lat_A))
    pB = atan(rb / ra * tan(rad_lat_B))
    if not (rad_lng_A - rad_lng_B):
        return 0.0
    xx = acos(sin(pA) * sin(pB) + cos(pA) * cos(pB) * cos(rad_lng_A - rad_lng_B))
    if xx == 0:
        distance = 0.0
    else:
        c1 = (sin(xx) - xx) * (sin(pA) + sin(pB)) ** 2 / cos(xx / 2) ** 2
        c2 = (sin(xx) + xx) * (sin(pA) - sin(pB)) ** 2 / sin(xx / 2) ** 2
        dr = flatten / 8 * (c1 - c2)
        distance = ra * (xx + dr)
    return distance


if __name__ == '__main__':
    data = '{"code":1,"msg":"success","data":[{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:23:02","lat":"34.7810615","lng":"113.6124495","location_type":2,"msg_type":6},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:23:42","lat":"34.7813175","lng":"113.6129175","location_type":2,"msg_type":6},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:24:32","lat":"34.7826177","lng":"113.6130089","location_type":2,"msg_type":6},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:24:40","lat":"34.7826069","lng":"113.6129886","location_type":2,"msg_type":5},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:25:15","lat":34.783382,"lng":113.613045,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:25:33","lat":"34.7806101","lng":"113.6114781","location_type":2,"msg_type":6},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:25:33","lat":"34.7806106","lng":"113.6115677","location_type":2,"msg_type":6},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:26:36","lat":34.783592,"lng":113.613106,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:26:46","lat":34.78406,"lng":113.613014,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:26:56","lat":34.78427,"lng":113.612144,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:27:06","lat":34.78451,"lng":113.61105,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:27:16","lat":34.784794,"lng":113.60983,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:27:26","lat":34.78509,"lng":113.60858,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:27:36","lat":34.785423,"lng":113.60728,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:27:46","lat":34.785683,"lng":113.60614,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:27:56","lat":34.785942,"lng":113.60507,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:28:06","lat":34.78625,"lng":113.60401,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:28:16","lat":34.786594,"lng":113.60356,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:28:26","lat":34.787403,"lng":113.60371,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:28:36","lat":34.788376,"lng":113.60391,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:28:46","lat":34.789314,"lng":113.60414,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:28:56","lat":34.789917,"lng":113.6043,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:29:06","lat":34.790337,"lng":113.60445,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:29:16","lat":34.790737,"lng":113.60454,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:29:26","lat":34.791107,"lng":113.60462,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:29:36","lat":34.791267,"lng":113.604675,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:30:03","lat":"34.7916021","lng":"113.6048058","location_type":2,"msg_type":6},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:32:44","lat":34.791496,"lng":113.604706,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:32:54","lat":34.792088,"lng":113.60472,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:33:04","lat":34.79281,"lng":113.60488,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:33:14","lat":34.79336,"lng":113.604996,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:33:34","lat":34.79343,"lng":113.60503,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:33:44","lat":34.793682,"lng":113.60496,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:33:53","lat":34.7938,"lng":113.60462,"location_type":3,"msg_type":5},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:33:54","lat":34.79381,"lng":113.60457,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:34:04","lat":34.79387,"lng":113.60391,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:34:54","lat":34.79399,"lng":113.60317,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:35:04","lat":34.79411,"lng":113.602455,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:35:14","lat":34.79427,"lng":113.601425,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:35:24","lat":34.79443,"lng":113.600266,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:35:34","lat":34.794613,"lng":113.599266,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:35:44","lat":34.79484,"lng":113.59877,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:35:54","lat":34.79555,"lng":113.59868,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:36:04","lat":34.796425,"lng":113.59859,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:36:14","lat":34.797497,"lng":113.59838,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:36:24","lat":34.798485,"lng":113.59817,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:36:34","lat":34.799076,"lng":113.59802,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:36:44","lat":34.799866,"lng":113.59794,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:36:54","lat":34.80097,"lng":113.59791,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:37:04","lat":34.80226,"lng":113.59792,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:37:14","lat":34.80357,"lng":113.59798,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:37:24","lat":34.804832,"lng":113.597946,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:37:34","lat":34.806053,"lng":113.59725,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:37:44","lat":34.807255,"lng":113.59635,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:37:54","lat":34.808666,"lng":113.59568,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:38:04","lat":34.8102,"lng":113.59532,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:38:14","lat":34.81173,"lng":113.59506,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:38:24","lat":34.813274,"lng":113.59481,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:38:34","lat":34.814735,"lng":113.59455,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:38:44","lat":34.815956,"lng":113.59434,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:38:54","lat":34.816616,"lng":113.594215,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:41:04","lat":34.816616,"lng":113.594215,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:41:14","lat":34.816917,"lng":113.59393,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:41:24","lat":34.816986,"lng":113.592995,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:41:34","lat":34.81701,"lng":113.59166,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:41:44","lat":34.817028,"lng":113.59006,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:41:54","lat":34.81705,"lng":113.58834,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:42:04","lat":34.81704,"lng":113.58654,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:42:14","lat":34.81705,"lng":113.58508,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:42:34","lat":34.817074,"lng":113.58478,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:42:44","lat":34.817062,"lng":113.58387,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:42:54","lat":34.817055,"lng":113.58251,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:43:04","lat":34.817055,"lng":113.58091,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:43:14","lat":34.817097,"lng":113.579414,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:43:24","lat":34.81735,"lng":113.577995,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:43:34","lat":34.81798,"lng":113.576805,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:43:44","lat":34.818615,"lng":113.57556,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:43:54","lat":34.819256,"lng":113.5744,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:44:04","lat":34.81999,"lng":113.572945,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:44:14","lat":34.82085,"lng":113.57134,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:44:24","lat":34.821777,"lng":113.569565,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:44:34","lat":34.822628,"lng":113.567955,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:44:44","lat":34.82331,"lng":113.56672,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:46:24","lat":34.8235,"lng":113.56632,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:48:30","lat":34.823784,"lng":113.56587,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:48:31","lat":34.823803,"lng":113.565834,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:48:31","lat":34.823795,"lng":113.565834,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:48:42","lat":34.823975,"lng":113.56545,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:48:52","lat":34.824425,"lng":113.56483,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:49:03","lat":34.825077,"lng":113.564064,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:49:12","lat":34.8252,"lng":113.56378,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:49:22","lat":34.82497,"lng":113.5635,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:49:32","lat":34.82504,"lng":113.56319,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:49:42","lat":34.82499,"lng":113.56293,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:54:30","lat":"34.8243259","lng":"113.5629902","location_type":2,"msg_type":6},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:55:04","lat":"34.8244249","lng":"113.5638433","location_type":2,"msg_type":6},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:55:08","lat":34.824978,"lng":113.56385,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:55:24","lat":"34.8243693","lng":"113.5648964","location_type":2,"msg_type":6},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:55:32","lat":34.824276,"lng":113.56424,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:55:42","lat":34.824226,"lng":113.56437,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:55:52","lat":34.824127,"lng":113.56444,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:56:02","lat":34.824047,"lng":113.5644,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:56:14","lat":"34.8238143","lng":"113.564544","location_type":2,"msg_type":6},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:56:23","lat":34.823814,"lng":113.56429,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:56:33","lat":34.823685,"lng":113.564156,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:56:42","lat":34.823586,"lng":113.56405,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:56:52","lat":34.823586,"lng":113.564026,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:57:02","lat":34.823456,"lng":113.563965,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:57:23","lat":34.823147,"lng":113.56395,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:57:32","lat":34.822975,"lng":113.56393,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:57:43","lat":34.822906,"lng":113.56398,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:57:52","lat":34.822926,"lng":113.56385,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 08:58:02","lat":34.823017,"lng":113.56373,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 15:19:35","lat":34.823368,"lng":113.56347,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 15:19:46","lat":34.823418,"lng":113.56346,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 15:24:16","lat":34.823456,"lng":113.56344,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 15:24:36","lat":34.823467,"lng":113.56344,"location_type":1,"msg_type":5},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 15:25:27","lat":34.823456,"lng":113.56343,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 15:45:21","lat":"34.8231136","lng":"113.5635688","location_type":2,"msg_type":6},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 15:45:33","lat":34.82345,"lng":113.563416,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 15:45:53","lat":"34.8231136","lng":"113.5635688","location_type":2,"msg_type":6},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 15:45:53","lat":"34.8231057","lng":"113.5635867","location_type":2,"msg_type":6},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 15:46:24","lat":34.82345,"lng":113.563416,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 16:02:05","lat":34.82345,"lng":113.563416,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 16:15:00","lat":"34.8230805","lng":"113.5635154","location_type":2,"msg_type":6},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 16:15:50","lat":"34.8230805","lng":"113.5635154","location_type":2,"msg_type":6},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 16:16:30","lat":"34.8230797","lng":"113.5634953","location_type":2,"msg_type":6},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 16:17:31","lat":"34.8230797","lng":"113.5634953","location_type":2,"msg_type":6},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 16:17:37","lat":34.82345,"lng":113.563416,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 16:17:57","lat":"34.8230805","lng":"113.5635154","location_type":2,"msg_type":6},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 16:18:18","lat":34.82345,"lng":113.563416,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 16:22:41","lat":"34.8230805","lng":"113.5635154","location_type":2,"msg_type":6},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 16:22:46","lat":34.823517,"lng":113.56344,"location_type":3,"msg_type":5},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 16:22:50","lat":34.82353,"lng":113.56343,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 16:23:11","lat":34.823498,"lng":113.563416,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 18:04:31","lat":34.82359,"lng":113.56347,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 18:05:42","lat":34.823456,"lng":113.56344,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 19:10:13","lat":34.823578,"lng":113.56334,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 19:10:45","lat":34.82343,"lng":113.56346,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 19:11:05","lat":34.82345,"lng":113.56344,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 19:11:47","lat":34.82345,"lng":113.56344,"location_type":3,"msg_type":5},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 19:47:42","lat":34.8234,"lng":113.563446,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 19:47:53","lat":34.82343,"lng":113.56343,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 19:50:13","lat":34.82343,"lng":113.56347,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 19:50:23","lat":34.82345,"lng":113.56348,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 19:50:53","lat":34.82343,"lng":113.563446,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 19:51:13","lat":"34.8229221","lng":"113.5632023","location_type":2,"msg_type":6},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 19:51:43","lat":34.822887,"lng":113.56332,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 19:51:53","lat":34.822777,"lng":113.56327,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 19:52:03","lat":34.822906,"lng":113.56333,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 19:52:13","lat":34.823036,"lng":113.56341,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:00:24","lat":"34.8230526","lng":"113.5630615","location_type":2,"msg_type":6},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:01:14","lat":"34.8243682","lng":"113.5647797","location_type":2,"msg_type":6},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:02:04","lat":"34.8215988","lng":"113.5663539","location_type":2,"msg_type":6},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:02:54","lat":"34.8194393","lng":"113.566885","location_type":2,"msg_type":6},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:03:02","lat":34.819668,"lng":113.56679,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:03:19","lat":"34.8230716","lng":"113.562701","location_type":2,"msg_type":6},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:03:43","lat":34.819675,"lng":113.56704,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:03:53","lat":34.819336,"lng":113.56723,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:04:03","lat":34.818886,"lng":113.56739,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:04:13","lat":34.818356,"lng":113.56755,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:04:23","lat":34.817833,"lng":113.56772,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:04:33","lat":34.817303,"lng":113.56792,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:04:43","lat":34.81679,"lng":113.56807,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:04:53","lat":34.81623,"lng":113.5681,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:05:03","lat":34.81567,"lng":113.568085,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:05:13","lat":34.81518,"lng":113.568085,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:05:23","lat":34.81477,"lng":113.568085,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:05:53","lat":34.81454,"lng":113.568085,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:06:03","lat":34.81406,"lng":113.5681,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:06:13","lat":34.81363,"lng":113.56807,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:06:23","lat":34.81318,"lng":113.56808,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:06:33","lat":34.81276,"lng":113.56811,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:06:43","lat":34.812237,"lng":113.568115,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:06:53","lat":34.8117,"lng":113.56814,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:07:03","lat":34.811146,"lng":113.56812,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:07:13","lat":34.810635,"lng":113.56814,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:07:23","lat":34.810085,"lng":113.56812,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:07:33","lat":34.809574,"lng":113.56809,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:07:43","lat":34.809013,"lng":113.56804,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:07:53","lat":34.808475,"lng":113.56804,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:08:03","lat":34.808155,"lng":113.56794,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:09:03","lat":34.807915,"lng":113.56805,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:09:13","lat":34.807583,"lng":113.56804,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:09:23","lat":34.807274,"lng":113.568115,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:09:33","lat":34.806904,"lng":113.56809,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:09:43","lat":34.806553,"lng":113.56805,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:09:53","lat":34.80632,"lng":113.56807,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:10:03","lat":34.80585,"lng":113.56801,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:10:13","lat":34.80535,"lng":113.56796,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:10:23","lat":34.80491,"lng":113.567955,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:10:33","lat":34.8044,"lng":113.56792,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:10:43","lat":34.80407,"lng":113.56796,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:10:53","lat":34.803658,"lng":113.56793,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:11:03","lat":34.80319,"lng":113.56799,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:11:13","lat":34.802597,"lng":113.56795,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:11:23","lat":34.802,"lng":113.567986,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:11:43","lat":34.801666,"lng":113.56809,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:11:53","lat":34.801666,"lng":113.56843,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:12:03","lat":34.801937,"lng":113.56847,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:12:13","lat":34.802177,"lng":113.568405,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:12:23","lat":34.802425,"lng":113.56857,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:12:33","lat":34.802517,"lng":113.56884,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:12:43","lat":34.802555,"lng":113.569176,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:13:05","lat":"34.8027192","lng":"113.5692787","location_type":2,"msg_type":6},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:13:25","lat":"34.8026576","lng":"113.5693506","location_type":2,"msg_type":6},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:13:45","lat":"34.8026438","lng":"113.5694089","location_type":2,"msg_type":6},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:14:25","lat":"34.8026576","lng":"113.5693506","location_type":2,"msg_type":6},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:14:35","lat":"34.8027273","lng":"113.5692798","location_type":2,"msg_type":6},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:14:45","lat":"34.8026706","lng":"113.5693704","location_type":2,"msg_type":6},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:15:05","lat":"34.8026438","lng":"113.5694089","location_type":2,"msg_type":6},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:15:25","lat":"34.8026576","lng":"113.5693506","location_type":2,"msg_type":6},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:15:45","lat":"34.8026576","lng":"113.5693506","location_type":2,"msg_type":6},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:16:15","lat":"34.8026576","lng":"113.5693506","location_type":2,"msg_type":6},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:16:23","lat":34.802635,"lng":113.569244,"location_type":1,"msg_type":2},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:19:18","lat":"34.8026752","lng":"113.5693487","location_type":2,"msg_type":6},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:20:07","lat":"34.8026188","lng":"113.5693921","location_type":2,"msg_type":6},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:20:47","lat":"34.8026188","lng":"113.5693921","location_type":2,"msg_type":6},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:21:27","lat":"34.8026449","lng":"113.5693709","location_type":2,"msg_type":6},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 20:22:27","lat":"34.8026449","lng":"113.5693709","location_type":2,"msg_type":6},{"deviceId":"702a8cac-2d03-434d-b120-86e7f23d7a55","timestamp":"2019-07-29 23:37:33","lat":"34.8027393","lng":"113.5693058","location_type":2,"msg_type":6}]}'
    filter_drift_point(data)
