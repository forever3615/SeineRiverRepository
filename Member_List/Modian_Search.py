#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 11:56:55 2018

@author: hanyuxu
"""

import os
import requests
from bs4 import BeautifulSoup
import sys

path = os.path.dirname(sys.argv[0])
os.chdir(path)

def get_yyh_id(kwd):
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
        }
    
    url = 'https://zhongchou.modian.com/search?key='
    
    r = requests.get(url + kwd, headers = header)
    r.encoding = 'utf-8'
    r = r.text
    soup = BeautifulSoup(r, 'lxml')
    
    proj_list = soup.findAll('div', attrs = {'class':'author'})
    
    member_yyh = dict()
    
    for item in proj_list:
        proj_info = str(item.select('a')).split('"')
        author_id = proj_info[1][-7:]
        author_name = proj_info[8].replace('></div>\n<p>','').replace('</p>\n</a>]','')
        if author_id == '1655350' or (author_id == '98779' and kwd == '陈观慧'):
            pass
        else:
            if author_name in member_yyh.keys():
                member_yyh[author_name]['proj_num'] += 1
            else:
                member_yyh.update({author_name : {'name' : author_name,
                                                  'id' : author_id.replace('=',''),
                                                      'proj_num': 1}})
        
    return member_yyh