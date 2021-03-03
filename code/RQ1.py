#!/usr/bin/python
# -*- coding: UTF-8 -*-
from __future__ import division
import os
import numpy as np
import pandas as pd
import pymysql
import matplotlib.pyplot as plt
import seaborn as sns
from numpy import median

sns.set_theme(style="whitegrid")
sns.set_palette("husl")

path = os.path.abspath('/Users/Yuxia/Desktop/survival/survival_code/')
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='openstack2019', charset='utf8')
cursor = conn.cursor()
######################################################################
# How common did companies leave OpenStack?
# num_leaving_companies and ratio of leaving companies per version
# get num_active_companies
with conn.cursor() as cursor:
    sql = 'select version, count(distinct company) ' \
          'from commits_new ' \
          'where company != %s and version is not null ' \
          'and version < %s ' \
          'group by version ' \
          'order by version'
    cursor.execute(sql, ('independent', 19))
    active_coms = cursor.fetchall()
    print('active companies: ', active_coms)

active_coms_ver = np.zeros(19)
for i in range(len(active_coms)):
    idx = int(active_coms[i][0])
    active_coms_ver[idx] = int(active_coms[i][1])
print('active_coms_ver', active_coms_ver)

# get num_leaving_companies
with conn.cursor() as cursor:
    sql = 'select company, max(version) ' \
          'from commits_new ' \
          'where 18_is_leave = %s and version < %s ' \
          'group by company ' \
          'order by version'
    cursor.execute(sql, ('Y', 19))
    leaving_coms = cursor.fetchall()
    print('leaving companies: ', leaving_coms)

num_leavers_ver = np.zeros(19) 
dict_coms_leave_ver = {}  
for i in range(len(leaving_coms)):
    idx = int(leaving_coms[i][1])
    num_leavers_ver[idx+1] += 1

    ver = int(leaving_coms[i][1]) + 1  
    com = leaving_coms[i][0]
    dict_coms_leave_ver[com] = ver

print("num_leavers_ver", num_leavers_ver)
print("dict_coms_leave_ver", dict_coms_leave_ver)


with conn.cursor() as cursor:
    sql = 'select company, min(version) ' \
          'from commits_new ' \
          'where company != %s and version < %s ' \
          'group by company ' \
          'order by version'
    cursor.execute(sql, ('independent', 19))
    coms_joined_ver = cursor.fetchall()
    print('new comers: ', coms_joined_ver)

num_join_com_ver = np.zeros(19)
join_coms_ver = {}  
for i in range(len(coms_joined_ver)):
    ver = int(coms_joined_ver[i][1])
    com = coms_joined_ver[i][0]
    num_join_com_ver[ver] += 1

    if ver in join_coms_ver.keys():
        join_coms_ver[ver].append(com)
    else:
        join_coms_ver[ver] = [com]

ver_join_leave_active = []  
for i in range(len(num_join_com_ver)):
    if i < len(num_leavers_ver):
        ver_join_leave_active.append([i, num_join_com_ver[i], num_leavers_ver[i], active_coms_ver[i]])
print('ver_join_leave_active', ver_join_leave_active)
np.savetxt(path + "/data/ver_join_leave_active.csv", ver_join_leave_active, fmt="%s", delimiter=",")

df_new_active_leave_coms = pd.DataFrame(columns=['version', 'status', 'num_coms'])
try_ver = []
try_active = []
try_new = []
try_left = []
for i in range(6, 18):
    # add newcoming companies to dataframe
    new = pd.DataFrame({'version': [i],
                        'status': ['new'],
                        'num_coms': [int(num_join_com_ver[i])]})
    df_new_active_leave_coms = df_new_active_leave_coms.append(new, ignore_index=True)

    # add active companies to dataframe
    active = pd.DataFrame({'version': [i],
                           'status': ['active'],
                           'num_coms': [int(active_coms_ver[i])]})
    df_new_active_leave_coms = df_new_active_leave_coms.append(active, ignore_index=True)

    # add leaving companies to dataframe
    left = pd.DataFrame({'version': [i],
                         'status': ['left'],
                         'num_coms': [int(num_leavers_ver[i])]})
    df_new_active_leave_coms = df_new_active_leave_coms.append(left, ignore_index=True)

    try_ver.append(i)
    try_active.append(int(active_coms_ver[i]))
    try_new.append(int(num_join_com_ver[i]))
    try_left.append(int(num_leavers_ver[i]))
print('df_new_active_leave_coms', df_new_active_leave_coms)


plt.rcParams['figure.figsize'] = (6, 5)
fig, ax1 = plt.subplots()
width = 0.4
x1_list = []
x2_list = []
x3_list = []
for i in range(len(try_ver)):
    x1_list.append(i)
    x2_list.append(i + width)
    x3_list.append(i + width/2)

sns.set_style("whitegrid")
#plt.grid('off')
b1 = ax1.bar(x1_list, try_new, width=width, color=sns.xkcd_rgb["pale red"], tick_label=try_ver)
b2 = ax1.bar(x2_list, try_left, width=width, color=sns.xkcd_rgb["denim blue"])
plt.legend(loc='upper left', labels=['Joined', 'Withdrawn'])
ax1.grid(True)
ax1.tick_params(axis='y', colors='grey')
ax2 = ax1.twinx()
ax2.grid(False)
b3 = ax2.plot(x3_list, try_active, color='black', marker='o', linewidth=1.5)
ax1.set_xlabel('Version', fontsize=12)
ax1.set_ylabel('Number of Companies', fontsize=12)
ax2.set_ylabel('Number of Companies', fontsize=12)
ax2.tick_params(axis='y', colors='grey')
plt.legend(loc='upper right', labels=['Sustaining'], bbox_to_anchor=(0.30, 0.88))
plt.savefig(path + "/pic/new_active_leave_coms.pdf", format='pdf')
plt.show()

with conn.cursor() as cursor:
    sql = 'select min(version) ' \
          'from commits_new ' \
          'where company != %s and version < %s ' \
          'and 18_is_leave = %s ' \
          'group by company ' \
          'order by version'
    cursor.execute(sql, ('independent', 19, 'Y'))
    leavers_joined_ver = cursor.fetchall()
    print('leavers_joined_ver: ', leavers_joined_ver)

ver_join_but_leave = np.zeros(19)
for i in range(len(leavers_joined_ver)):
    ver = int(leavers_joined_ver[i][0])
    ver_join_but_leave[ver] += 1
    
ratio_leaving = []
version = []
for i in range(6, 18):
    ratio_leaving.append(num_leavers_ver[i+1] / active_coms_ver[i])
    version.append(i)
print('ratio_leaving', ratio_leaving)
print('version', version)

sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (6, 4.5)
df1 = pd.DataFrame({'Version': version, 'Ratio': ratio_leavers_joined_same_ver})
plt.plot(df1['Version'], df1['Ratio'], color=sns.xkcd_rgb["pale red"], marker='o', linewidth=1.5)
#b3 = ax2.plot(x3_list, try_active, label='Sustained', color='black', marker='o', linewidth=1.5)
#sns.lineplot(x="Version", y="Ratio", data=df1, color=sns.xkcd_rgb["pale red"], linewidth=2)
df2 = pd.DataFrame({'Version': version, 'Ratio': ratio_leaving})
plt.plot(df2['Version'], df2['Ratio'], color=sns.xkcd_rgb["denim blue"], marker='v')
#sns.lineplot(x="Version", y="Ratio", data=df2, color=sns.xkcd_rgb["denim blue"], linewidth=2)
my_x_ticks = np.arange(6, 18, 1)
plt.xticks(my_x_ticks)
plt.ylim((0, 1))
plt.legend(loc='upper right', labels=['Turnover of the joined companies', 'Turnover of the sustaining companie'])
plt.savefig(path + "/pic/ratio_leavers_ver.pdf", format='pdf')
plt.show()

print('join_com_ver', num_join_com_ver)
print("median left companies", median(num_leavers_ver[1:]))
print("median active companies", median(active_coms_ver[1:]))
print("median ratio", median(ratio_leaving))
print("ratio of leavers joined in the same version", ratio_leavers_joined_same_ver)

rq1_how_common_basic_data = [['version', '#active_coms', '#left_coms', '#joined_coms', '#joined_left_later_coms']]
for i in range(1, 18):
    ver = i
    active_coms = active_coms_ver[ver]
    left_coms = num_leavers_ver[ver]
    joined_coms = num_join_com_ver[ver]
    joined_left_later_coms = ver_join_but_leave[ver]
    rq1_how_common_basic_data.append([ver, active_coms, left_coms, joined_coms, joined_left_later_coms])
print('rq1_how_common_basic_data', rq1_how_common_basic_data)
np.savetxt(path + "/data/rq1_how_common_basic_data.csv", rq1_how_common_basic_data, fmt="%s", delimiter=",")

print('ratio_leavers_joined_same_ver:\n', pd.DataFrame(ratio_leavers_joined_same_ver).describe())
print('ratio_leaving_next_ver:\n', pd.DataFrame(ratio_leaving).describe())
