#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 00:43:03 2018

@author: hanyuxu
"""

import xlrd
import os
import sys

path = os.path.dirname(sys.argv[0])
os.chdir(path)

def read_excel():
    data=xlrd.open_workbook('/Users/hanyuxu/Documents/GitHub/SeineRiverRepository/Member_List/owhat.xlsx')
    print('已读取owhat信息。')
    table = data.sheet_by_name(u'Summary')
    htt = round(table.cell(1,1).value,2)
    lyt = round(table.cell(2,1).value,2)
    return htt, lyt