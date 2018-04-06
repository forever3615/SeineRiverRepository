#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 16:06:53 2018

@author: hanyuxu
"""

import json
import os
import sys
import time

chinese_name = {'cl' :'陈  琳',
                'cyl':'陈韫凌',
                'fxf':'冯晓菲',
                'lj' :'李  晶',
                'lyl':'林忆宁',
                'lz' :'李  钊',
                'pyq':'潘瑛琪',
                'qj' :'祁  静',
                'sxr':'宋昕冉',
                'sxw':'孙歆文',
                'wjl':'汪佳翎',
                'ws' :'汪  束',
                'wxj':'王晓佳',
                'xsq':'徐诗琪',
                'xty':'谢天依',
                'yby':'杨冰怡',
                'yyy':'杨韫玉',
                'zds':'张丹三',
                'zjy':'张嘉予'
                }

time0 = time.time()

path = os.path.dirname(sys.argv[0])
os.chdir(path)

def read_json(json_file_name):
    '''
    take an arguement of a dict, output a .json file for this dict
    '''
    os.chdir(path)
    json_file_name = json_file_name + '.json'
    
    with open(json_file_name, 'r') as f:
        data = json.load(f)
        
    return data

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

def digit_input(msg):
    
    while True:
        input_digit = input(msg)
        try:
            input_digit == float(input_digit)
        except ValueError:
            print('请输入数字。')
        else:
            break
    return input_digit

def input_mvp_list():
    
    while True:
        date1 = digit_input('请输入公演日期？')
        if not(len(date1) == 8):
            print('日期只能由八位数字组成。')
        else:
            date2 = digit_input('再次输入公演日期？')
            if not(len(date2) == 8):
                print('日期只能由八位数字组成。')
            if date1 == date2:
                break
            else:
                print('两次输入不一致。')
    
    date = date1
    
    current_tickets = dict()
    
    while True:
        member = input('成员缩写？')
        if member in chinese_name.keys():
            tickets = float(digit_input('%s 获得票数？'%chinese_name[member]))
            current_tickets.update({chinese_name[member]:tickets})
        else:
            if member == 'end':
                print('榜单输入结束。')
                break
            else:
                print('该成员不存在。')
    
    return current_tickets, date

def main():
    current_tickets, date = input_mvp_list()
    
    try:
        mvp_dic = read_json('MVP')
    except FileNotFoundError:
        mvp_dic = dict()
        pass
    
    if date in mvp_dic.keys():
        for member in current_tickets.keys():
            if member in mvp_dic[date].keys():
                if current_tickets[member] == mvp_dic[date][member]:
                    print('1')
                    pass
                else:
                    mvp_dic[date][member] = current_tickets[member]
                    print('已更新 %s 在 %s 公演中的得票数。' % (member,date))
            else:
                mvp_dic[date].update({member:current_tickets[member]})
                print('已添加 %s 在 %s 公演中的得票数。' % (member,date))
    else:
        mvp_dic.update({date:current_tickets})
        print('已添加 %s 公演中的得票数。' % date)
    
    out_to_json(path, mvp_dic, 'MVP')

while True:
    switch = input('是否输入数据？')
    if switch == 'end':
        break
    else:
        main()