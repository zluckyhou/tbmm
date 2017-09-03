# -*- coding:utf-8 -*-

import os
import requests
from lxml import etree
import random
import datetime
from multiprocessing import Pool, Lock,cpu_count
import json

os.chdir(r'C:\Users\zluck\Documents\Python_Scripts\爬虫\淘宝MM')
headers = [{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'},
           {
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'},
           {
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393'}]


# url = 'https://mm.taobao.com/tstar/search/tstar_model.do?_input_charset=utf-8'
# def GetPageNum(url, headers):
#     params = {"q": "", "viewFlag": "A", "sortType": "default", "searchStyle": "", "searchRegion": "city:",
#               "searchFansNum": "", "currentPage": "1", "pageSize": "100"}
#
#     r = requests.post(url, headers=random.choice(headers), params=params)
#     d = r.json()
#     # d.keys()
#     # d['data'].keys()
#     total_page = d['data']['totalPage']
#     return total_page
# def GetInfoList(url, headers, params):
#     r = requests.post(url, headers=random.choice(headers), params=params)
#     d = r.json()
#     searchDOList = d['data']['searchDOList']
#     return searchDOList
# def GetTotalUserList(total_page):
#     total_ls = []
#     for i in tqdm(range(1, total_page + 1)):
#         # print('This is page {}'.format(i))
#         params = {"q": "", "viewFlag": "A", "sortType": "default", "searchStyle": "", "searchRegion": "city:",
#                   "searchFansNum": "", "currentPage": "{}".format(i), "pageSize": "100"}
#         try:
#             searchDOList = GetInfoList(url, headers, params)
#             total_ls.extend(searchDOList)
#         except Exception as e:
#             print(e)
#             print('relax, you need to sleep a while...')
#             time.sleep(60)
#         time.sleep(random.random())
#     return total_ls



def GetPageLs(url):
    with lock:
        print('current url: ', url)
        # lock.release()
        r = requests.post(url, headers=random.choice(headers))
        html = r.text
        s = etree.HTML(html)
        ItemLs = s.xpath('//div[@class="list-item"]')
        for i in range(len(ItemLs)):
            try:
                d = {}
                d['page'] = url
                d['rank'] = (s.xpath('//div[@class="list-item"][{}]//div[@class="list-info"]//div[@class="popularity"]//dl//dt/text()'.format(i+1))+[''])[0].strip()
                # personal_info
                d['lady_name'] = (s.xpath(
                    '//div[@class="list-item"][{}]//div[@class="personal-info"]//p[@class="top"]//a[@class="lady-name"]/text()'.format(
                        i + 1)) + [''])[0]
                d['user_host'] = 'https:' + (s.xpath(
                    '//div[@class="list-item"][{}]//div[@class="personal-info"]//p[@class="top"]//a[@class="lady-name"]/@href'.format(
                        i + 1)) + [''])[0]
                d['age'] = (s.xpath(
                    '//div[@class="list-item"][{}]//div[@class="personal-info"]//p[@class="top"]//em//strong/text()'.format(
                        i + 1)) + [''])[0]
                d['city'] = (s.xpath(
                    '//div[@class="list-item"][{}]//div[@class="personal-info"]//p[@class="top"]//span[position()=1]/text()'.format(
                        i + 1)) + [''])[0]
                d['profession'] = (s.xpath(
                    '//div[@class="list-item"][{}]//div[@class="personal-info"]//p[position()=2]//em[position()=1]/text()'.format(
                        i + 1)) + [''])[0]
                d['fans'] = (s.xpath(
                    '//div[@class="list-item"][{}]//div[@class="personal-info"]//p[position()=2]//em[position()=2]//strong/text()'.format(
                        i + 1)) + [''])[0]
                # list_info
                d['points'] = (s.xpath(
                    '//div[@class="list-item"][{}]//div[@class="list-info"]//div[@class="popularity"]//dl/dd/text()[2]'.format(
                        i + 1)) + [''])[0].strip()
                # info_detail
                d['new_point'] = (s.xpath(
                    '//div[@class="list-item"][{}]//div[@class="list-info"]//ul[@class="info-detail"]//li[1]/strong/text()'.format(
                        i + 1)) + [''])[0]
                d['fiveStarRate'] = (s.xpath(
                    '//div[@class="list-item"][{}]//div[@class="list-info"]//ul[@class="info-detail"]//li[2]/strong/text()'.format(
                        i + 1)) + [''])[0]
                d['guide_pictures'] = (s.xpath(
                    '//div[@class="list-item"][{}]//div[@class="list-info"]//ul[@class="info-detail"]//li[3]/strong/text()'.format(
                        i + 1)) + [''])[0]
                d['contract_num'] = (s.xpath(
                    '//div[@class="list-item"][{}]//div[@class="list-info"]//ul[@class="info-detail"]//li[4]/strong/text()'.format(
                        i + 1)) + [''])[0]
                d['description'] = (s.xpath(
                    '//div[@class="list-item"][{}]//div[@class="list-info"]//p[@class="description"]/text()'.format(
                        i + 1)) + [''])[
                    0].strip()
            except Exception as e:
                print('Exception for page {} and user {}'.format(url, i + 1), e)
            with open('basicInfo.txt', 'a') as f:
                f.write(json.dumps(d) + '\n')


def init_child(lock_):
    global lock
    lock = lock_


def main():
    print('process start...')
    start = datetime.datetime.now()
    urls = ['https://mm.taobao.com/json/request_top_list.htm?page={}'.format(i) for i in range(1, 4302)]
    poolsize = cpu_count()
    lock = Lock()
    with Pool(poolsize, initializer=init_child, initargs=(lock,)) as pool:
        pool.map(GetPageLs, urls)
    end = datetime.datetime.now()
    timespan = end - start
    print('Success! The process takes {}'.format(timespan))


if __name__ == '__main__':
    main()

