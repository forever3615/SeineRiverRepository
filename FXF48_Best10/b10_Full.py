#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 18:05:16 2018

@author: hanyuxu
"""

import requests
import urllib3
import os
import sys
import time

time0 = time.time()

path = os.path.dirname(sys.argv[0])
os.chdir(path)

js = requests.get('https://raw.githubusercontent.com/fxf48/fxf48.github.io/master/js/unlock.txt')
js_text = js.text.replace('When we are to you', 'WhenWeAreToYou').replace('Ice Queen', 'IceQueen').replace('girl crush', 'GrilCrush').replace('  ', ' ')

for i in range(1,63):
    if i < 10:
        key = '\n0' + str(i) + '\t'
    else:
        key = '\n' + str(i) + '\t'
    js_text = js_text.replace(key, ' ')
js_list = js_text.replace('01', '').replace('\t', '').split(' ')

song_dict = dict()

ident = 0

for key in range(0, len(js_list) - 2 , 3):
    ident += 1
    if ident < 10:
        str_id = '0' + str(ident)
    else:
        str_id = str(ident)

    name = js_list[key]
    artist = js_list[key+1]
    url = js_list[key+2]

    song_dict.update({str_id + '.' + name:{'id': str_id,
                                           'name': name,
                                           'artist': artist,
                                           'url': url}})

def download_song(file_name):    
    http = urllib3.PoolManager()
    response = http.request('GET', song_dict[key]['url'])
    try:
        os.chdir(path + '/FXF48_B10/Final_ver')
    except FileNotFoundError:
        os.makedirs(path + '/FXF48_B10/Final_ver')
        os.chdir(path + '/FXF48_B10/Final_ver')
    with open(file_name, 'wb') as f:
        f.write(response.data)
    response.release_conn()
    print('已输出 %s ~!' % file_name)

for key in song_dict:
    file_name = '%s_%s.flac' % (key, song_dict[key]['artist'])

    os.chdir(path + '/FXF48_B10/Final_ver')
    try:
        open(file_name)
    except FileNotFoundError:
        print(file_name)
        download_song(file_name)
