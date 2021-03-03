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
from matplotlib.pyplot import MultipleLocator

sns.set_theme(style="whitegrid")
sns.set_palette("husl")

path = os.path.abspath('/Users/anonymous/Desktop/survival/survival_code/')
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='openstack2019', charset='utf8')
cursor = conn.cursor()

######################################################################
# How important has the leaving companies played in OpenStack?
# The distribution of the number of commits submitted by the exiting companies to a single project per version.
with conn.cursor() as cursor:
    sql = 'select company, count(distinct author_ID), count(distinct id), ' \
          'count(distinct repository), count(distinct version) ' \
          'from commits_new ' \
          'where 18_is_leave = %s ' \
          'and company != %s ' \
          'and version between %s and %s ' \
          'group by company'
    cursor.execute(sql, ('Y', 'independent', 1, 18))
    coms_performs = cursor.fetchall()
print('coms_performs', coms_performs)

num_dvpr = []
num_cmt = []
num_repo = []
num_ver = []
for i in range(len(coms_performs)):
    num_dvpr.append(coms_performs[i][1])
    num_cmt.append(coms_performs[i][2])
    num_repo.append(coms_performs[i][3])
    num_ver.append(coms_performs[i][4])

print('num_dvpr:\n', pd.DataFrame(num_dvpr).describe())
print('num_cmt:\n', pd.DataFrame(num_cmt).describe())
print('num_repo:\n', pd.DataFrame(num_repo).describe())
print('num_ver:\n', pd.DataFrame(num_ver).describe())

fig, axes = plt.subplots(2, 2)
plt.subplots_adjust(wspace=0.4, hspace=0.2)
sns.violinplot(data=num_dvpr, ax=axes[0, 0], color=sns.xkcd_rgb["pale red"])
ax0 = axes[0, 0]
ax0.axes.set_ylabel("Number")
ax0.axes.set_xlabel("Developers")
ax0.axes.set_xticks([])

sns.violinplot(data=num_cmt, ax=axes[0, 1], color=sns.xkcd_rgb["denim blue"])
ax1 = axes[0, 1]
ax1.axes.set_ylabel("Number")
ax1.axes.set_xlabel("Commits")
ax1.axes.set_xticks([])

sns.violinplot(data=num_repo, ax=axes[1, 0], color=sns.xkcd_rgb["amber"])
ax2 = axes[1, 0]
ax2.axes.set_ylabel("Number")
ax2.axes.set_xlabel("Repositories")
ax2.axes.set_xticks([])

sns.violinplot(data=num_ver, ax=axes[1, 1], color=sns.xkcd_rgb["faded green"])
ax3 = axes[1, 1]
ax3.axes.set_ylabel("Number")
ax3.axes.set_xlabel("Versions")
ax3.axes.set_xticks([])

plt.savefig(path + "/pic/left_coms_pfms.pdf", format='pdf')
plt.show()

df_intensity_extent = pd.read_csv(path + "/data/same_version_join_intensity_extent_df.csv")
print('df_intensity_extent', df_intensity_extent)
print('median of left companies\' intensity', median(df_intensity_extent.loc[df_intensity_extent['status'] == 'left', 'intensity']))
print('median of active companies\' intensity', median(df_intensity_extent.loc[df_intensity_extent['status'] == 'active', 'intensity']))
print('median of left companies\' extent', median(df_intensity_extent.loc[df_intensity_extent['status'] == 'left', 'extent']))
print('median of active companies\' extent', median(df_intensity_extent.loc[df_intensity_extent['status'] == 'active', 'extent']))

df_intensity_extent.columns = ['ID', 'Version', 'Status', 'Intensity', 'Extent']
print("df_intensity_extent.loc[df_intensity_extent['status'] == 'left', 'intensity']", df_intensity_extent.loc[df_intensity_extent['Status'] == 'left', 'Intensity'])
left_intensity = df_intensity_extent.loc[df_intensity_extent['Status'] == 'left', 'Intensity'].tolist()
active_intensity = df_intensity_extent.loc[df_intensity_extent['Status'] == 'active', 'Intensity'].tolist()
ratio_intensity = []

left_extent = df_intensity_extent.loc[df_intensity_extent['Status'] == 'left', 'Extent'].tolist()
active_extent = df_intensity_extent.loc[df_intensity_extent['Status'] == 'active', 'Extent'].tolist()
ratio_extent = []
version = []
for i in range(len(left_intensity)):
    ratio_intensity.append(active_intensity[i]/left_intensity[i])
    ratio_extent.append(active_extent[i]/left_extent[i])
    version.append(i+1)

print('ratio_intensity', ratio_intensity)
print('ratio_extent', ratio_extent)

plt.rcParams['figure.figsize'] = (6.5, 5)
fig, ax1 = plt.subplots()
width = 0.4
x1_list = []
x2_list = []
x3_list = []
for i in range(len(version)):
    x1_list.append(i)
    x2_list.append(i + width)
    x3_list.append(i + width/2)

sns.set_style("whitegrid")
b1 = ax1.bar(x1_list, active_intensity, width=width, label='Active', color=sns.xkcd_rgb["pale red"], tick_label=version)
b2 = ax1.bar(x2_list, left_intensity, width=width, label='Left', color=sns.xkcd_rgb["denim blue"])
plt.legend(loc='upper right', labels=['Sustaining', 'Withdrawn'])
ax1.grid(True)
ax1.tick_params(axis='y', colors='grey')
ax2 = ax1.twinx()
ax2.grid(False)
b3 = ax2.plot(x3_list, ratio_intensity, label='Ratio', color='black', marker='o', linewidth=1.5)
ax1.set_xlabel('Version', fontsize=12)
ax1.set_ylabel('Intensity', fontsize=12)
ax2.set_ylabel('Ratio', fontsize=12)
ax2.tick_params(axis='y', colors='grey')
y_major_locator = MultipleLocator(1)
ax2.yaxis.set_major_locator(y_major_locator)
plt.legend(loc='upper right', labels=[' Ratio        '], bbox_to_anchor=(1, 0.88))
plt.savefig(path + "/pic/coms_same_ver_intensity_with_ratio.pdf", format='pdf')
plt.show()


plt.rcParams['figure.figsize'] = (6.5, 5)
fig, ax1 = plt.subplots()
width = 0.4
x1_list = []
x2_list = []
x3_list = []
for i in range(len(version)):
    x1_list.append(i)
    x2_list.append(i + width)
    x3_list.append(i + width/2)

sns.set_style("whitegrid")
b1 = ax1.bar(x1_list, active_extent, width=width, label='Active', color=sns.xkcd_rgb["pale red"], tick_label=version)
b2 = ax1.bar(x2_list, left_extent, width=width, color=sns.xkcd_rgb["denim blue"])
plt.legend(loc='upper right', labels=['Sustaining', 'Withdrawn'])
ax1.grid(True)
ax1.tick_params(axis='y', colors='grey')
ax2 = ax1.twinx()
ax2.grid(False)
b3 = ax2.plot(x3_list, ratio_extent, color='black', marker='o', linewidth=1.5)
ax1.set_xlabel('Version', fontsize=12)
ax1.set_ylabel('Extent', fontsize=12)
ax2.tick_params(axis='y', colors='grey')
ax2.set_ylabel('Ratio', fontsize=12)
y_major_locator = MultipleLocator(0.5)
ax2.yaxis.set_major_locator(y_major_locator)
plt.legend(loc='upper right', labels=[' Ratio        '], bbox_to_anchor=(1, 0.88))
plt.savefig(path + "/pic/coms_same_ver_extent_with_ratio.pdf", format='pdf')
plt.show()


