#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 20:59:04 2018

@author: hanyuxu
"""

import json
import os
import sys
import csv
import time
from read_excel import read_excel
time0 = time.time()

path = os.path.dirname(sys.argv[0])
os.chdir(path)

def read_json(path, json_file_name):
    '''
    take an arguement of a dict, output a .json file for this dict
    '''
    os.chdir(path)
    
    with open(json_file_name, 'r') as f:
        data = json.load(f)
        
    return data

def json_to_csv():
    data = read_json(path, 'Modian_Summary.json')
    
    with open("test.csv","w") as csvfile: 
        writer = csv.writer(csvfile)
    
        writer.writerow(['Team','Name','Total Amount','Headcount','Average'])
        
        htt, lyt = read_excel()
        
        for team in data:
            for name in data[team]:
                if name == '黄婷婷':
                    total_amount = round(data[team][name]['总计金额'] + htt,2)
                else:
                    if name == '李艺彤':
                        total_amount = round(data[team][name]['总计金额'] + lyt,2)
                    else:
                        total_amount = data[team][name]['总计金额']
                headcount = data[team][name]['集资人数']
                average = data[team][name]['人均集资']
                line = [team, name, total_amount, headcount, average]
                writer.writerow(line)
    
    print('已更新test.csv文件')
            

def main2():
    json_to_csv()

