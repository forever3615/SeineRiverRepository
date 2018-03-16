#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 11:53:19 2018

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

js = requests.get('https://raw.githubusercontent.com/fxf48/fxf48.github.io/master/js/b10list.js')

js_list = js.text.replace(' ','').replace("'", '').replace('"','').replace(',','').split('\n')

song_dict = dict()

ident = 0

for key in range(0, len(js_list)):
    if 'name' in js_list[key]:
        ident += 1
        if ident < 10:
            str_id = '0' + str(ident)
        else:
            str_id = str(ident)

        name = js_list[key].replace('name:','')
        if 'url' in js_list[key+1].replace('artist:',''):
            artist = '匿名 试听版'
            url = js_list[key+1].replace('url:','')
        else:
            artist =  js_list[key+1].replace('artist:','')
            url = js_list[key+2].replace('url:','')
        song_dict.update({str_id + '.' + name:{'id': str_id,
                                               'name': name,
                                               'artist': artist,
                                               'url': url}})

for key in song_dict:
    file_name = '%s_%s.flac' % (key, song_dict[key]['artist'].replace(' ','_').replace('完整版','_完整版'))
    http = urllib3.PoolManager()
    response = http.request('GET', song_dict[key]['url'])
    try:
        os.chdir(path + '/FXF48_B10')
    except FileNotFoundError:
        os.makedirs(path + '/FXF48_B10')
        os.chdir(path + '/FXF48_B10')
    with open(file_name, 'wb') as f:
        f.write(response.data)
    response.release_conn()
    print('已输出 %s ~!' % file_name)

print('全部完成，用时 %.2f秒~' % round(time.time()-time0,2))
