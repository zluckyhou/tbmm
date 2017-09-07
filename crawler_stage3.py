# -*- coding:utf-8 -*-

# 抓取个性主页联系方式、照片等信息

import os
import re
import requests
from lxml import etree
import random
import datetime
import multiprocessing
import json
import pickle
from tqdm import tqdm

os.chdir(r'D:\MyDrivers\python\tbmm')
headers = [{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'},
           {
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'},
           {
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393'}]

with open('info.pkl','rb') as f:
    info = pickle.load(f)


def downloadImg(user_id,img):
    os.mkdir('{}_img'.format(user_id))
    os.chdir('./{}_img'.format(user_id))
    for i in tqdm(img):
        img_name = i.split('/')[-1].split('_')[0]
        img_file = requests.get(i, headers=random.choice(headers)).content
        with open(img_name + '.jpg', 'wb') as f:
            f.write(img_file)

def GetContent(url):
    try:
        user_id = re.findall('\d+',url)[0]
        print('current user: ',user_id)
        r = requests.get(url,headers=random.choice(headers))
        s = etree.HTML(r.text)
        content = ','.join([e.xpath('string(.)') for e in s.xpath('//div[@class="mm-aixiu-content"]//strong')])
        img = list(set(['https:' + i for i in s.xpath('//div//img[@src]/@src') if i.startswith('//img') and '!!' in i]))
        d = {'img':img,'content':content,'user_id':user_id}
        return json.dumps(d)
    except Exception as e:
        return None

def start_process():
    print('Starting', multiprocessing.current_process().name)

if __name__ == '__main__':
    print('process start...')
    start = datetime.datetime.now()
    pool_size = multiprocessing.cpu_count()
    with multiprocessing.Pool(processes=pool_size, initializer=start_process) as pool:
        # pool.map_async(GetDetailInfo, urls, callback=mycallback)
        pool_outputs = pool.map(GetContent, info['modelCard'])
    with open('contentInfo.pkl', 'wb') as f:
        pickle.dump(pool_outputs, f)
    # pool = multiprocessing.Pool(processes=pool_size, initializer=start_process)
    # for i in tqdm(user['user_id']):
    #     pool.apply_async(GetDetailInfo, args=(i,), callback=mycallback)
    # pool.close()
    # pool.join()
    end = datetime.datetime.now()
    timespan = end - start
    print('Success! The process takes {}'.format(timespan))