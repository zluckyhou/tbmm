# -*- coding:utf-8 -*-

import os
import re
import requests
from lxml import etree
import random
import datetime
import multiprocessing
import json
import pickle
from pandas import DataFrame
import numpy as np

os.chdir(r'C:\Users\zluck\Documents\Python_Scripts\爬虫\tbmm')

# read basic info
with open('basicInfo.txt') as f:
    ls = f.readlines()


def ls2df(ls):
    userLs = []
    for i in ls:
        try:
            userLs.append(json.loads(i.strip()))
        except Exception as e:
            print('Exception: ', i)
    return userLs


def str2float(s):
    try:
        return float(s)
    except Exception as e:
        return None


user = DataFrame(ls2df(ls))

user['rank'] = user['rank'].astype('int')
user['age'] = user['age'].astype('int')
# Series([i for i in user['age'] if i > 18 and i < 40]).hist() # 完美的正态分布
user['fans'] = user['fans'].astype('int')
user['fiveStarRate'] = list(map(str2float, user['fiveStarRate']))
user['guide_pictures'] = user['guide_pictures'].astype('int')
user['new_point'] = user['new_point'].astype('int')
user['points'] = user['points'].astype('int')
user['user_id'] = [i.split('?')[1].split('=')[1] for i in user['user_host']]
user.sort_values(by='rank', axis=0, inplace=True)

# read detail info

with open('DetailInfo.pkl', 'rb') as f:
    di = pickle.load(f)

js = [i for i in di if i]  # 过滤掉为None的元素
d = [json.loads(i) for i in js]
detail = DataFrame(d)
detail['user_id'] = [re.findall('\d+',i)[0] for i in detail['modelCard']]

for i in detail['modelCard']:
    try:
        re.findall('\d+',i)
    except Exception as e:
        print(e)
        print(i)