#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 25 14:31:48 2018

@author: hanyuxu
"""

import os
import sys
import time
import json

time0 = time.time()

path = os.path.dirname(sys.argv[0])
os.chdir(path)

def read_json(json_file_name):
    '''
    take an arguement of a dict, output a .json file for this dict
    '''
    os.chdir(path)
    
    with open(json_file_name, 'r') as f:
        data = json.load(f)
        
    return data

entities = read_json('MVP.json')

#month = input('MVP月份？')
month = '0203'

mvp_summary = dict()

for item in entities:
    if item[4:6] in month:
        for member in entities[item]:
            if member in mvp_summary:
                pass
            else:
                mvp_summary.update({member:0})
            mvp_summary[member] = entities[item][member] + mvp_summary[member]