#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 15:30:00 2018

@author: hanyuxu
"""

import os
import sys
import requests
import time
import datetime
import hashlib
import urllib.parse
from bs4 import BeautifulSoup
import json
from Member_List import member_list_main

time0 = time.time()

path = os.path.dirname(sys.argv[0])
os.chdir(path)

def convert_timestamp_to_timestr(timestamp):
    """
    将13位时间戳转换为字符串
    :param timestamp:
    :return:
    """
    timeArray = time.localtime(timestamp / 1000)
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return time_str

def ksort(d):
    return [(k, d[k]) for k in sorted(d.keys())]

class ModianEntity:
    def __init__(self, link, title, pro_id, need_display_rank=False, current=0.0, target=0.0, support_num=0):
        self.link = link
        self.title = title
        self.pro_id = pro_id
        self.need_display_rank = need_display_rank
        self.current = current
        self.target = target
        self.support_num = support_num

class ModianHandler:
    def __init__(self, modian_project_array):
        self.session = requests.session()
        self.modian_project_array = modian_project_array
    
        self.modian_fetchtime_map = {}  # 各集资项目上次查询订单的时间
        self.jizi_rank_list = []
        self.daka_rank_list = []
        # self.order_queues = []
        self.init_order_queues()
    
    def init_order_queues(self):
        # TODO: 初始化订单队列，用于发送集资播报
        for modian_entity in self.modian_project_array:
            self.modian_fetchtime_map[modian_entity.pro_id] = time.time()
    
    def modian_header(self):
        """
        微打赏header信息
        """
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.3408.400 QQBrowser/9.6.12028.40',
        }
        return header

    def query_project_orders(self, modian_entity, page=1):
        """
        查询项目订单（摩点API版本）
        :param page:
        :param modian_entity:
        :return:
        """
#        print('查询项目订单, pro_id: %s'% modian_entity.pro_id)
        api = 'https://wds.modian.com/api/project/orders'
        params = {
            'pro_id': modian_entity.pro_id,
            'page': page
        }
        r = requests.post(api, self.make_post_params(params), headers=self.modian_header()).json()
        if int(r['status']) == 0:
            orders = r['data']
#            print('项目订单: page: %s, 已完成' % page)
            return orders
        if int(r['status']) == 2:  # 该页没有订单
            print('项目订单: page: %s, 数据为空' % page)
            return []
        else:
            raise RuntimeError('获取项目订单查询失败')
            
    def make_post_params(self, post_fields):
        """
        获取post请求需要的参数
        :param post_fields:
        :return:
        """
        sign = self.__make_signature(post_fields)
        post_fields['sign'] = sign
        print('正在查询: %s' % post_fields)
        return post_fields

    def __make_signature(self, post_fields):
        """
        生成调用微打赏接口所需的签名

        PHP的例子：
            $post_fields = $_POST;
            ksort($post_fields);
            $md5_string = http_build_query($post_fields);
            $sign = substr(md5($md5_string), 5, 21);

        :param post_fields: post请求的参数
        :return:
        """
        post_fields_sorted = ksort(post_fields)
        md5_string = urllib.parse.urlencode(post_fields_sorted) + '&p=das41aq6'
        sign = hashlib.md5(md5_string.encode('utf-8')).hexdigest()[5:21]
        return sign

    def get_current_and_target(self, modian_entity):
        """
        获取当前进度和总额（摩点API版本）
        :param modian_entity:
        :return:
        """
        print()
        print('获取当前进度和总额: %s'% modian_entity.title)
        api = 'https://wds.modian.com/api/project/detail'
        params = {
            'pro_id': modian_entity.pro_id
        }
        r = requests.post(api, self.make_post_params(params), headers=self.modian_header()).json()
        if int(r['status']) == 0:
            data_json = r['data'][0]
            pro_name = data_json['pro_name']
            modian_entity.target = float(data_json['goal'])
            modian_entity.current = data_json['already_raised']
            print('目标: %s, 当前进度: %s'% (modian_entity.target, modian_entity.current))
            print()
            return modian_entity.target, modian_entity.current, pro_name
        else:
            raise RuntimeError('获取项目筹款结果查询失败')
    
    def get_support_num(self, modian_entity):
        support_num = len(self.get_ranking_list(modian_entity))
        modian_entity.support_num = support_num
        print()
        return support_num
    
    def get_ranking_list(self, modian_entity, type0=1):
        """
        获取排名所有的列表
        :param modian_entity:
        :param type0: 1为集资，2为打卡
        :return:
        """
        ranking_list = []
        page = 1
        if type0 == 1:
            print('查询项目集资榜')
        elif type0 == 2:
            print('查询项目打卡榜')
        else:
            print('type0参数不合法')
            raise RuntimeError('type0参数不合法！')
        while True:
            rank_page = self.get_modian_rankings(modian_entity, type0, page)
            if len(rank_page) > 0:
                ranking_list.extend(rank_page)
                page += 1
            else:
                return ranking_list

    def get_modian_rankings(self, modian_entity, type0=1, page=1):
        """
        查询项目集资榜和打卡榜
        :param type0: 排名类型，1代表集资榜，2代表打卡榜
        :param modian_entity:
        :param page: 页号，每页默认返回20条
        :return:
        """
        api = 'https://wds.modian.com/api/project/rankings'
        params = {
            'pro_id': modian_entity.pro_id,
            'type': type0,
            'page': page
        }
        r = requests.post(api, self.make_post_params(params), headers=self.modian_header()).json()
        if int(r['status']) == 0:
            # pro_name = r['data']['pro_name']
            rankings = r['data']
            return rankings
        else:
            raise RuntimeError('获取项目排名失败, type=%d', type0)
    
def monitor_modian(update = True):
    """
    监控摩点
    :return:
    """
    global modian, modian_handler
    print('查询项目集资情况: %s'% modian.title)
    time1 = time.time()
    page_num = 0
    r_list = [{}]
    while True:
        page_num += 1
        r = modian_handler.query_project_orders(modian, page_num)
        retry_time = 0
        while retry_time < 1:
            retry_time += 1
            if len(r) == 0:
                r = modian_handler.query_project_orders(modian, page_num)
                print(('请求订单失败，第%s次重试' % retry_time))
            else:
                break
        if len(r) == 0:
            break
        else:
            r_list.extend(r)
            pass
        if update is True:
            if time.mktime(time.strptime(r_list[1]['pay_time'],'%Y-%m-%d %H:%M:%S')) > \
            time.mktime(time.strptime((datetime.datetime.now()+datetime.timedelta(hours=-1)).strftime('%Y-%m-%d 00:00:00'),'%Y-%m-%d %H:%M:%S')):
                continue
            else:
                print('该集资项目本日无更新！')
                print()
                return False
    modian_handler.get_current_and_target(modian)
    modian_handler.get_support_num(modian)
    r_list[0]= {'项目ID':modian.pro_id, 
                 '项目名称':modian.title, 
                 '项目链接':modian.link, 
                 '目标金额':modian.target,
                 '当前金额':modian.current,
                 '支持人数':modian.support_num
                 }
    print('查询摩点集资情况所消耗的时间为: %.2f秒'% round((time.time() - time1),2))
    print()
    return r_list

def get_member_proj_id(url):
    r = requests.get(url).text
    soup = BeautifulSoup(r, 'lxml')
    all_proj = str(soup.body.find_all('div', attrs = {'class':'myproject clearfix'}))
    proj_id_list = []
    for item in all_proj.split('"'):
        if 'zhongchou.modian.com/item/' in item:
            try:
                if int(item[34:39]) not in proj_id_list:
                    proj_id_list.append(int(item[34:39]))
            except ValueError:
                pass
    return proj_id_list

def get_html(proj_id):
    header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
    }
    url = 'https://zhongchou.modian.com/item/' + str(proj_id) + '.html'
    r = requests.get(url, headers = header)
    r.encoding = 'utf-8'
    r = r.text
    soup = BeautifulSoup(r, 'lxml')
    title = soup.find('h3', attrs = {'class':'title'}).string[:]
    return url, title, proj_id

def out_to_json(cd, dict, file_name, sort = False):
    try:
        os.chdir(cd)
    except FileNotFoundError:
        os.makedirs(cd)
        os.chdir(cd)
    with open(file_name+'.json','w') as outfile:
        json.dump(dict,outfile,ensure_ascii=False,sort_keys = sort)
        outfile.write('\n')
        print('已更新： %s.json' % file_name)
        print()

def main0():
    
    global modian_handler, modian
    
    snh_group = dict()
    
    member_dict = member_list_main()
#    member_dict = {'TeamX': {'冯晓菲': {'SNH48冯晓菲应援会': {'id': '1170704',
#                                                           'name': 'SNH48冯晓菲应援会',
#                                                           'proj_num': 4}}, 
#                             '杨冰怡': {'SNH48杨冰怡应援会': {'id': '998668',
#                                                           'name': 'SNH48杨冰怡应援会',
#                                                           'proj_num': 7},
#                                       'dream雪中寻梦': {'id': '984989', 
#                                                        'name': 'dream雪中寻梦', 
#                                                        'proj_num': 1}}}}
    
    yyh_base_url = 'https://me.modian.com/user?type=index&id='
    
    for team in member_dict:
        print(team)
        if team in snh_group:
            pass
        else:
            snh_group.update({team:{}})
        for member_name in member_dict[team]:
            print('正在获取 %3s 集资项目ID...' % member_name)
            if member_name in snh_group[team]:
                pass
            else:
                snh_group[team].update({member_name:[]})
            for yyh_name in member_dict[team][member_name]:
                iden = member_dict[team][member_name][yyh_name]['id']
                snh_group[team][member_name] += (get_member_proj_id(yyh_base_url + iden))
    
    for team in snh_group:
        for name in snh_group[team]:
            MODIAN_ARRAY = []
            for item in snh_group[team][name]:
                url, title, proj_id = get_html(item)
                modian = ModianEntity(url, title, proj_id, False)
                MODIAN_ARRAY.append(modian)                
            
            modian_handler = ModianHandler([])
            
            for modian in MODIAN_ARRAY:
                try:
                    cd = path + '/Modian_Items/' + team + '/' + name + '/'
                    os.chdir(cd)
                    open(str(modian.pro_id) + '_' + modian.title + '.json')
                except FileNotFoundError:
                    r = monitor_modian(False)
                else:
                    r = monitor_modian(True)   # update switch
                if r is False:
                    pass
                else:
                    cd = path + '/Modian_Items/' + team + '/' + name + '/'
                    out_to_json(cd, r, str(modian.pro_id) + '_' + modian.title.replace('/',''))
    
    print('查询全部完成！所消耗的时间为: %.2f秒'% round((time.time() - time0),2))

if __name__ == "__main__":
    main0()