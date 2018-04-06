#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 10:38:21 2018

@author: hanyuxu
"""

import os
import sys
import time
import json
import urllib.request
from Modian_Search import get_yyh_id

time0 = time.time()

path = os.path.dirname(sys.argv[0])
os.chdir(path)

def get_member_list():
    url = 'http://h5.snh48.com/resource/jsonp/members.php?gid=10'
    req = urllib.request.urlopen(url)
    s = req.read()
    s_json = json.loads(s, encoding='utf-8')
    req.close()
    
    snh_group = {}
    snh_group.update({'TeamSII':{}})
    snh_group.update({'TeamNII':{}})
    snh_group.update({'TeamHII':{}})
    snh_group.update({'TeamX':{}})
    snh_group.update({'TeamFt':{}})
    
    for item in s_json['rows']:
        if item['tname'] == 'SII' and item['status'] == '99':
            snh_group['TeamSII'].update({item['sname']:{}})
        if item['tname'] == 'NII' and item['status'] == '99':
            snh_group['TeamNII'].update({item['sname']:{}})
        if item['tname'] == 'HII' and item['status'] == '99':
            snh_group['TeamHII'].update({item['sname']:{}})
        if item['tname'] == 'X' and item['status'] == '99':
            snh_group['TeamX'].update({item['sname']:{}})
        if item['tname'] == 'Ft' and item['status'] == '99':
            snh_group['TeamFt'].update({item['sname']:{}})
    return snh_group

def fill_yyh_id(member_dict):
    for team in member_dict:
        for member_name in member_dict[team]:
            member_dict[team][member_name].update(get_yyh_id(member_name))
            print('Done with %s~' % member_name)

def member_list_main():
    member_dict = get_member_list()
    fill_yyh_id(member_dict)
    return member_dict