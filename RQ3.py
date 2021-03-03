#!/usr/bin/python
# -*- coding: UTF-8 -*-
from __future__ import division

import os

import numpy as np
import pymysql
import seaborn as sns

sns.palplot(sns.color_palette("hls", 11))
sns.palplot(sns.color_palette("hls", 11))

path = os.path.abspath('/Users/Yuxia/Desktop/survival/survival_code/')
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='openstack2019', charset='utf8')
cursor = conn.cursor()

coms = np.loadtxt(path + "/data/RQ3_dataset.csv", delimiter=",", dtype=np.str, skiprows=1)

REPOS_most_domi = {}

num_bug_ver = [175, 289, 536, 1268, 3394, 2634, 3615, 6070, 10086, 13896, 17092, 17904, 20148, 20047, 7893, 8059, 4879, 5356]

with conn.cursor() as cursor:
    sql = 'select version, count(id), count(distinct repository) ' \
          'from commits_new ' \
          'group by version'
    cursor.execute(sql)
    os_cmt_prj = cursor.fetchall()
    print('os_cmt_prj', os_cmt_prj)

dict_os_cmt_prj = {}
for i in range(len(os_cmt_prj)):
    ver = os_cmt_prj[i][0]
    sum_cmt = os_cmt_prj[i][1]
    sum_prj = os_cmt_prj[i][2]
    dict_os_cmt_prj[ver] = [sum_cmt, sum_prj]


with conn.cursor() as cursor:
    sql = 'select company, max(version), min(version) ' \
          'from commits_new ' \
          'group by company'
    cursor.execute(sql)
    res = cursor.fetchall()
dict_com_start_stop = {}
for i in range(len(res)):
    com = res[i][0]
    max_V = min(int(res[i][1]), 18)
    min_V = res[i][2]
    dict_com_start_stop[com] = [min_V, max_V]


def intensity_extent(com):
    intensity = {}
    extent = {}
    with conn.cursor() as cursor:
        sql = 'select version, count(id), count(distinct repository) ' \
              'from commits_new ' \
              'where company like %s ' \
              'group by version'
        cursor.execute(sql, com)
        com_cmt_prj = cursor.fetchall()

    for i in range(len(com_cmt_prj)):
        ver = com_cmt_prj[i][0]
        com_cmt = com_cmt_prj[i][1]
        com_prj = com_cmt_prj[i][2]

        overall = dict_os_cmt_prj[ver]
        os_cmt = overall[0]
        os_prj = overall[1]

        inten = com_cmt / os_cmt
        exten = com_prj / os_prj

        intensity[ver] = inten
        extent[ver] = exten

    return intensity, extent


def get_com_most_repo(com):
    min_V = dict_com_start_stop[com][0]
    max_V = dict_com_start_stop[com][1]
    com_most_repo = {}
    for i in range(min_V, max_V+1):
        with conn.cursor() as cursor:
            sql = 'select repository, count(*) ' \
                  'from commits_new ' \
                  'where version = %s ' \
                  'and company = %s ' \
                  'group by repository ' \
                  'order by count(*) desc ' \
                  'limit 1'
            cursor.execute(sql, (i, com))
            res = cursor.fetchall()
        if len(res) > 0:
            repo = res[0][0]
            com_most_repo[i] = repo
    return com_most_repo

def calculate_domi(repo, ver):
    with conn.cursor() as cursor:
        sql = 'select count(*) ' \
              'from commits_new ' \
              'where version = %s and repository = %s ' \
              'group by company ' \
              'order by count(*) desc'
        cursor.execute(sql, (ver, repo))
        repo_cmts_list = cursor.fetchall()

    with conn.cursor() as cursor:
        sql = 'select count(*) ' \
              'from commits_new ' \
              'where version = %s and repository = %s'
        cursor.execute(sql, (ver, repo))
        total_cmt = cursor.fetchall()

    if len(repo_cmts_list) > 0:
        sum_cmt = int(total_cmt[0][0])
        the_max = int(repo_cmts_list[0][0])
        domi = the_max / sum_cmt
        key = repo + str(ver)
        REPOS_most_domi[key] = domi
        return domi

def get_domi(repo, ver):
    key = repo + str(ver)
    if key in REPOS_most_domi.keys():
        return REPOS_most_domi[key]
    else:
        return calculate_domi(repo, ver)

final_data = []
for i in range(len(coms)):
    com = coms[i][1]
    status = coms[i][0]
    endpt = status
    scale_level = coms[i][3]
    aim = coms[i][4]

    start = dict_com_start_stop[com][0] - 1
    stop = dict_com_start_stop[com][1]

    intensitys, extents = intensity_extent(com)
    repos = get_com_most_repo(com)

    for ver in range(start+1, stop+1):
        if ver in intensitys.keys():
            intensity = intensitys[ver]
            extent = extents[ver]

            tstart = ver - 1
            tstop = ver

            repo = repos[ver]
            domination = get_domi(repo, ver)

            mtnc_diff = dict_os_cmt_prj[ver][0]

            num_bugs = num_bug_ver[tstart]

            final_data.append([com, status, start, stop, aim, scale_level, intensity, extent, domination, mtnc_diff,
                               num_bugs, tstart, tstop, endpt])
            print('com, status, start, stop, aim, scale_level, intensity, extent, domination, mtnc_diff, num_bugs, '
                  'tstart, tstop, endpt')
            print(com, status, start, stop, aim, scale_level, intensity, extent, domination, mtnc_diff, num_bugs,
                  tstart, tstop, endpt)
print('final data', final_data)
np.savetxt(path + "/data/survival_data_per_ver.csv", final_data, fmt="%s", delimiter=",")


