#!/usr/bin/python
# -*- coding: UTF-8 -*-
from __future__ import division
import os
import sys
import numpy as np
import pandas as pd
import pymysql
import matplotlib.pyplot as plt
import seaborn as sns


sns.palplot(sns.color_palette("hls", 11))

path = os.path.abspath('/Users/anonymous/Desktop/survival/survival_code/')
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='openstack2019', charset='utf8')
cursor = conn.cursor()

with conn.cursor() as cursor:
    sql = 'select distinct company ' \
          'from commits_new ' \
          'where company != %s ' \
          'and company != %s '
    cursor.execute(sql, ('independent', ''))
    com_list = cursor.fetchall()
print('com_list', com_list)
print('len(com_list)', len(com_list))


def compute_interval(vers, intervals):
    itvs = []
    last_v = 19
    for i in range(len(vers)):
        if i+1 < len(vers) and vers[i+1][0] < 18:
            itv = vers[i+1][0] - vers[i][0] - 1
            print('interval', itv)
            itvs.append(itv)
            intervals.append(itv)
        if i == len(vers)-1:
            last_v = (vers[i][0])

    return itvs, last_v

intervals = []
max_intervals = []
leaver_cur_intervals = []
last_vs = []
leave_coms = []
for i in range(len(com_list)):
    com = com_list[i][0]
    with conn.cursor() as cursor:
        sql = 'select distinct version ' \
              'from commits_new ' \
              'where company = %s ' \
              'and version < %s ' \
              'and version != %s ' \
              'order by version'
        cursor.execute(sql, (com, 19, ''))
        c_vs = cursor.fetchall()
    print('c_vs', c_vs)

    c_itvs, last_v = compute_interval(c_vs, intervals)
    cur_itv = 18 - last_v
    last_vs.append(last_v)
    if len(c_itvs) > 0:
        max_itv = max(c_itvs)
        max_intervals.append(max_itv)
    else:
        max_itv = 0

    if cur_itv > max_itv:
        leave_coms.append([com, last_v, 18, cur_itv, max_itv, 'Y'])
        leaver_cur_intervals.append(cur_itv)
    else:
        leave_coms.append([com, last_v, 18, cur_itv, max_itv, 'N'])

    print('com, last_v, 18, cur_itv, max_itv', com, last_v, 18, cur_itv, max_itv)
np.savetxt(path + "/data/leave_companies.csv", leave_coms, fmt="%s", delimiter=",")


intervals = np.array(intervals)
print('len(intervals)', len(intervals))
print('diffs', intervals)
print('max', intervals.max())
print('min', intervals.min())
print('medium', np.median(intervals))
print('mean', intervals.mean())
np.savetxt(path + "/data/com_contribute_intervals.csv", intervals, fmt="%s", delimiter=",")

max_intervals = np.array(max_intervals)
print('len(max_intervals)', len(max_intervals))
print('max_intervals', max_intervals)
print('max', max_intervals.max())
print('min', max_intervals.min())
print('median', np.median(max_intervals))
print('mean', max_intervals.mean())
np.savetxt(path + "/data/com_max_intervals.csv", max_intervals, fmt="%s", delimiter=",")

leaver_cur_intervals = np.array(leaver_cur_intervals)
print('len(leaver_cur_intervals)', len(leaver_cur_intervals))
print('leaver_cur_intervals', leaver_cur_intervals)
print('max', leaver_cur_intervals.max())
print('min', leaver_cur_intervals.min())
print('median', np.median(leaver_cur_intervals))
print('mean', leaver_cur_intervals.mean())
np.savetxt(path + "/data/com_leaver_cur_intervals.csv", leaver_cur_intervals, fmt="%s", delimiter=",")

s1 = pd.Series(np.array(intervals))
s2 = pd.Series(np.array(max_intervals))
s3 = pd.Series(np.array(leaver_cur_intervals))
data = pd.DataFrame({"Overall": s1, "Max": s2, "Withdrawn": s3})
sns.set_style("whitegrid")
figsize = 6, 4
fig, ax = plt.subplots(figsize=figsize)
sns.violinplot(data=data, palette=[sns.xkcd_rgb["pale red"], sns.xkcd_rgb["denim blue"], sns.xkcd_rgb["amber"]],
               scale="width")
plt.ylabel("Version Intervals")
plt.savefig(path + "/pic/intervals.pdf", format='pdf')
plt.show()


