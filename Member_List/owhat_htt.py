#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 22:54:02 2018

@author: hanyuxu
"""

import os
import requests
from bs4 import BeautifulSoup
import sys

path = os.path.dirname(sys.argv[0])
os.chdir(path)

header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:59.0) Gecko/20100101 Firefox/59.0'
    }


proj_id = 34446

url = 'https://www.owhat.cn/shop/supportdetail.html?id=' + str(proj_id)
r = requests.get(url, headers = header)
r.encoding = 'utf-8'
r = r.text
soup = BeautifulSoup(r, 'html.parser')

#title = soup.find('h3', attrs = {'class':'title'}).string[:]
#backer_money = soup.find('span', attrs = {'backer_money':str(proj_id)}).string[:]
#print(backer_money)
#goal_money = soup.find('span', attrs={'class': 'goal-money'}).string[6:]
#support_num = soup.find('span', attrs={'backer_count': str(proj_id)}).string[:]

cutdown = soup.find('section', attrs = {'class':'panel-body master_work white_bg prt3'})

print(soup)