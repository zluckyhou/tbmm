# -*- coding:utf-8 -*-

import os
import requests
from lxml import etree
import random
import datetime
from multiprocessing import Pool, Lock
import json
import pandas as pd
from pandas import DataFrame

os.chdir(r'C:\Users\zluck\Documents\Python_Scripts\爬虫\淘宝MM')
headers = [{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'},
           {
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'},
           {
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393'}]

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

user['age'] = user['age'].astype('int')
user['fans'] = user['fans'].astype('int')
user['fiveStarRate'] = list(map(str2float,user['fiveStarRate']))
user['guide_pictures'] = user['guide_pictures'].astype('int')
user['new_point'] = user['new_point'].astype('int')
user['points'] = user['points'].astype('int')
user['user_id'] = [i.split('?')[1].split('=')[1] for i in user['user_host']]

url = 'https://mm.taobao.com/self/info/model_info_show.htm?user_id={}'.format(user['user_id'][0])
r = requests.get(url,headers=random.choice(headers))
html = r.text
s = etree.HTML(html)