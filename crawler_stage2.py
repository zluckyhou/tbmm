# -*- coding:utf-8 -*-

# 抓取主页详细信息

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
from tqdm import tqdm

os.chdir(r'D:\MyDrivers\python\tbmm')
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


def GetDetailInfo(user_id):
    try:
        url = 'https://mm.taobao.com/self/info/model_info_show.htm?user_id={}'.format(user_id)
        print('current url: ', url)
        r = requests.get(url, headers=random.choice(headers))
        html = r.text
        s = etree.HTML(html)

        # base info
        base_key = [re.sub('[\u3000\s:]', '', i) for i in
                    s.xpath('//div[@class="mm-p-info mm-p-base-info"]//li/label/text()')]
        base_value = [i.text for i in s.iterfind('.//div[@class="mm-p-info mm-p-base-info"]//li/span')]

        base_key.extend(
            [i.split('-')[-1] for i in s.xpath('//div[@class="mm-p-info mm-p-base-info"]//li[position()>=8]/@class')])
        base_value.extend([i.text for i in s.iterfind('.//div[@class="mm-p-info mm-p-base-info"]//li/p')])

        # photo info
        photo_key = s.xpath('//div[@class="mm-p-info mm-p-photo-info"]//li/label/text()')
        photo_value = [re.sub('\s*', '', i) for i in
                       [e.xpath('string(.)') for e in s.xpath('//div[@class="mm-p-info mm-p-photo-info"]//li/span')]]

        # domain info
        domain_key = s.xpath('//div[@class="mm-p-info mm-p-domain-info"]//li/label/text()')
        domain_value = ['https:' + i for i in
                        s.xpath('//div[@class="mm-p-info mm-p-domain-info"]//li/span[position()=1]/text()')]

        # experience info
        exp_key = s.xpath('//div[@class="mm-p-info mm-p-experience-info"]/h4/@title')
        exp_value = [e.xpath('string(.)').strip().replace(' ', '') for e in
                     s.xpath('//div[@class="mm-p-info mm-p-experience-info"]//p')]

        # sheShow
        modelCard_key = [i.split('-')[-1] for i in s.xpath('//div[@class="mm-p-right mm-p-sheShow"]/div/@class')]
        modelCard_value = ['https:' + i for i in s.xpath('//div[@class="mm-p-right mm-p-sheShow"]//a/@href')]

        tag_key = [i.split('-')[-1] for i in s.xpath('//div[@class="mm-p-right mm-p-sheShow"]//ul/@class')]
        tag_value = s.xpath('//div[@class="mm-p-right mm-p-sheShow"]//ul/li/text()')

        # merge key and value
        key = base_key + photo_key + domain_key + exp_key + modelCard_key + tag_key
        value = base_value + photo_value + domain_value + exp_value + modelCard_value + tag_value
        # def key_map(key):
        #     mapping = {'学校/专业': 'edu/major', '所在城市': 'city', '昵称': 'nickname', '生日': 'birthday', '职业': 'profession',
        #                '血型': 'blood_type', '风格': 'style', 'weight': 'weight', 'shose': 'shose', 'height': 'height',
        #                'bar': 'bar', 'size': 'size'}
        #     return mapping[key]

        info = dict(zip(key, value))
        info['user_id'] = user_id
        return json.dumps(info)
    except Exception as e:
        print(e)
        return None


def mycallback(x):
    with open('detailInfo.txt', 'a') as f:
        f.write(x + '\n')


def start_process():
    print('Starting', multiprocessing.current_process().name)


if __name__ == '__main__':
    print('process start...')
    start = datetime.datetime.now()
    pool_size = multiprocessing.cpu_count()*2
    with multiprocessing.Pool(processes=pool_size, initializer=start_process) as pool:
        # pool.map_async(GetDetailInfo, urls, callback=mycallback)
        pool_outputs = pool.map(GetDetailInfo, user['user_id'])
    with open('DetailInfo2.pkl', 'wb') as f:
        pickle.dump(pool_outputs, f)
    # pool = multiprocessing.Pool(processes=pool_size, initializer=start_process)
    # for i in tqdm(user['user_id']):
    #     pool.apply_async(GetDetailInfo, args=(i,), callback=mycallback)
    # pool.close()
    # pool.join()
    end = datetime.datetime.now()
    timespan = end - start
    print('Success! The process takes {}'.format(timespan))
