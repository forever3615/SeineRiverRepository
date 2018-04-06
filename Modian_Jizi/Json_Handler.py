#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 19:12:11 2018

@author: hanyuxu
"""

import os
import sys
import time
import json
from Modian_Info import out_to_json, main
from config import chinese_name_2

time0 = time.time()

path = os.path.dirname(sys.argv[0])
os.chdir(path)

def file_name(file_dir, keyword):
    '''
    file_dir is the path of files
    keyword is the keyword which destinated files contains
    '''
    
    L=[]   
    for root, dirs, files in os.walk(file_dir):  
        for file in files:  
            if (os.path.splitext(file)[1] == '.json') and \
            (keyword in os.path.join(file)):
                L.append(os.path.join(file))  
    return L

def read_json(json_file_name):
    '''
    take an arguement of a dict, output a .json file for this dict
    '''
    os.chdir(path + '/team_x')
    
    with open(json_file_name, 'r') as f:
        data = json.load(f)
        
    return data

'''
sort by date
'''

def sort_by_date(keyword):
    '''
    imput: 
        keyword is the chinese name of member
    output: 
        proj_summary is a dict of id, name, link, target, current and support number of the project
        personal_daily is a dict of jizi amount by date
    '''
    personal_daily = dict()
    proj_summary = list()
    
    for proj_name in file_name(path, keyword):
    
        entities = read_json(proj_name)
        proj_summary.append(entities.pop(0))
        
        for item in entities:
            pay_day = item['pay_time'][:10].replace('-','')
            if pay_day in personal_daily:
                pass
            else:
                personal_daily.update({pay_day:[]})
                personal_daily[pay_day] = 0
            personal_daily[pay_day] += item['backer_money']
            personal_daily[pay_day] = round(personal_daily[pay_day],2)
    
#    personal_daily = sorted(personal_daily.items(), key=lambda \
#                            item:item[1], reverse=True)
            
#        print(proj_summary)
    return proj_summary, personal_daily

def summary_by_date(summary_dic):
    '''
    take no arguement
    output a dict summarized daily jizi info of all members in chinese_name list
    '''
    global chinese_name_2
    
    daily_summary = dict()
    
    for item in chinese_name_2:
        proj_summary, personal_daily = sort_by_date(item)
        if len(personal_daily) == 0:
            pass
        else:
#            daily_summary.update({item:proj_summary})
            daily_summary.update({item:personal_daily})
    
        total_amount = 0
        
        for item2 in proj_summary:
            total_amount += item2['当前金额']
        
        summary_dic.update({item:{}})
        summary_dic[item].update({'总计金额': round(total_amount,2)})
        
    return daily_summary

'''
sort by modian id
'''

def sort_by_id(keyword):
    '''
    imput: 
        keyword is the chinese name of member
    output: 
        proj_summary is a dict of id, name, link, target, current and support number of the project
        personal_per_id is a dict of jizi amount by modian id
    '''
    personal_per_id = dict()
    
    for proj_name in file_name(path, keyword):
    
        entities = read_json(proj_name)
        entities.pop(0)
        
        for item in entities:
            user_id = item['user_id']
            if user_id in personal_per_id:
                pass
            else:
                personal_per_id.update({user_id: {}})
                personal_per_id[user_id].update({'nickname':item['nickname'],
                                                 'user_id':user_id,
                                                 'amount':float(0)})
            personal_per_id[user_id]['amount'] += float(item['backer_money'])
            personal_per_id[user_id]['amount'] = round(personal_per_id[user_id]['amount'],2)
    
#    personal_per_id = sorted(personal_per_id.items(), key=lambda \
#                            item:item[1], reverse=True)
    
    return personal_per_id

def summary_by_id():
    '''
    take no arguement
    output a dict summarized daily jizi info of all members in chinese_name list
    '''
    global chinese_name_2
    
    userid_summary = dict()
    
    for item in chinese_name_2:
        personal_per_id = sort_by_id(item)
        if len(personal_per_id) == 0:
            pass
        else:
            userid_summary.update({item:personal_per_id})

    return userid_summary

'''
find shared fans
'''
def find_sharing_fans(userid_summary, member_name = '冯晓菲'):
    '''
    take an arguement of member name
    return a list of her sharing fans with members in list
    '''
    
    global chinese_name_2
    
    check_list = chinese_name_2.copy()
    
    sharing_fans = dict()

    try:
        userid_summary[member_name]
    except KeyError:
        print('未获得 %s 的摩点集资信息。' % member_name)
        return
    
    check_list.remove(member_name)
    
    sharing_fans.update({member_name:{}})
    sharing_fans[member_name].update({'total_sharing_fans': 0})
    
    while True:
        
#        time0 = time.time()
        
        checking_member = check_list.pop()
        
        for item in userid_summary[member_name].keys():
            try:
                if item in userid_summary[checking_member].keys():
                    if item in sharing_fans[member_name].keys():
                        sharing_fans[member_name][item]['sharing_with'].update({checking_member:userid_summary[checking_member][item]['amount']})
                        sharing_fans[member_name][item]['num_of_sharing'] += 1
                    else:
                        sharing_fans[member_name].update({item:{}})
                        sharing_fans[member_name][item].update({'nickname': userid_summary[checking_member][item]['nickname'],
                                                                'user_id': item,
                                                                'num_of_sharing':1,
                                                                'sharing_with':{member_name:userid_summary[member_name][item]['amount']}})
                        sharing_fans[member_name][item]['sharing_with'].update({checking_member:userid_summary[checking_member][item]['amount']})
                        sharing_fans[member_name][item]['num_of_sharing'] += 1
            except KeyError:
                pass
        
#        print('已完成 %s 和 %s 的粉丝重合检查,用时 %.2f 秒。' % (member_name, checking_member, round(time.time() - time0, 2)))
        
        if len(check_list) == 0:
            break
        else:
            continue
    
    sharing_fans[member_name]['total_sharing_fans'] = len(sharing_fans[member_name]) - 1
    
    return sharing_fans

def voting_power(userid_summary):
    
    v_p = dict()
    
    for member in userid_summary.keys():
        print('开始分析 %s。' % member)
        
        v_p.update({member:{'20000~':{'0_total':0},
                            '10000~20000':{'0_total':0},
                            '5000~10000':{'0_total':0},
                            '1500~5000':{'0_total':0},
                            '1000~1500':{'0_total':0},
                            '500~1000':{'0_total':0},
                            '300~500':{'0_total':0},
                            '100~300':{'0_total':0},
                            '~100':{'0_total':0}
                            }})
        for userid in userid_summary[member]:
            if int(userid_summary[member][userid]['amount']) in range(20000,999999):
                v_p[member]['20000~']['0_total'] += 1
                v_p[member]['20000~'].update({userid_summary[member][userid]['nickname']:userid_summary[member][userid]['amount']})
            if int(userid_summary[member][userid]['amount']) in range(10000,20000):
                v_p[member]['10000~20000']['0_total'] += 1
                v_p[member]['10000~20000'].update({userid_summary[member][userid]['nickname']:userid_summary[member][userid]['amount']})
            if int(userid_summary[member][userid]['amount']) in range(5000,10000):
                v_p[member]['5000~10000']['0_total'] += 1
                v_p[member]['5000~10000'].update({userid_summary[member][userid]['nickname']:userid_summary[member][userid]['amount']})
            if int(userid_summary[member][userid]['amount']) in range(1500,5000):
                v_p[member]['1500~5000']['0_total'] += 1
                v_p[member]['1500~5000'].update({userid_summary[member][userid]['nickname']:userid_summary[member][userid]['amount']})
            if int(userid_summary[member][userid]['amount']) in range(1000,1500):
                v_p[member]['1000~1500']['0_total'] += 1
                v_p[member]['1000~1500'].update({userid_summary[member][userid]['nickname']:userid_summary[member][userid]['amount']})
            if int(userid_summary[member][userid]['amount']) in range(500,1000):
                v_p[member]['500~1000']['0_total'] += 1
                v_p[member]['500~1000'].update({userid_summary[member][userid]['nickname']:userid_summary[member][userid]['amount']})
            if int(userid_summary[member][userid]['amount']) in range(300,500):
                v_p[member]['300~500']['0_total'] += 1
#                v_p[member]['300~500'].update({userid_summary[member][userid]['nickname']:userid_summary[member][userid]['amount']})
            if int(userid_summary[member][userid]['amount']) in range(100,300):
                v_p[member]['100~300']['0_total'] += 1
#                v_p[member]['100~300'].update({userid_summary[member][userid]['nickname']:userid_summary[member][userid]['amount']})
            if int(userid_summary[member][userid]['amount']) in range(0,100):
                v_p[member]['~100']['0_total'] += 1
#                v_p[member]['~100'].update({userid_summary[member][userid]['nickname']:userid_summary[member][userid]['amount']})
        print('完成分析 %s' % member)
    return v_p
                
                
def main2():
    share = dict()
    summary_dic = dict()
    
#    suma = summary_by_id()
#    for key in suma['冯晓菲']:
#        if suma['冯晓菲'][key]['amount'] > 1000:
#            print(suma['冯晓菲'][key])
    
    by_date = summary_by_date(summary_dic)
    by_id = summary_by_id()
    
    out_to_json(path, by_date, 'Summary_by_Date')
    out_to_json(path, by_id, 'Summary_by_ID')
    
    for item in by_id.keys():
        summary_dic[item].update({'集资人数':len(by_id[item])})
        summary_dic[item].update({'人均集资':round(summary_dic[item]['总计金额']/summary_dic[item]['集资人数'],2)})
    out_to_json(path, summary_dic, 'Modian_Summary')
    
    for item in chinese_name_2:
        try:
            share.update(find_sharing_fans(by_id, item))
        except TypeError:
            print('无%s信息。'%(item))
            pass
    
    vp = voting_power(by_id)
  
    out_to_json(path, share, 'Sharing_Fans')
    out_to_json(path, vp, 'Voting_Power')
    
main()

time1 = time.time()

if __name__ == "__main__":
    main2()
    
    print('粉丝差异度查询完成！所消耗的时间为: %.2f秒'% round((time.time() - time1),2))

print('All Done~！所消耗的时间为: %.2f秒'% round((time.time() - time0),2))