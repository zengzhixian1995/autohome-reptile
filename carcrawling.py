# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 17:15:55 2018

@author: lenovo
"""

import re 
import requests  
from bs4 import BeautifulSoup 
import json
import time
import csv

def Getcarsdata(autohome_url):
    #从汽车之家首页中获取车型数据
    #autohome_url="https://www.autohome.com.cn"#汽车之家首页
    print('开始爬取汽车之家首页的汽车数据...')
    flag=1
    while flag==1:
        try:
            content = BeautifulSoup(requests.get(autohome_url,timeout=5).text, "html.parser")#用get方法获取页面并解析文档
            flag=0
        except:
            flag=1
            print('停止爬取60s')
            time.sleep(60)
    #content = BeautifulSoup(requests.get(autohome_url).text, "html.parser")#用get方法获取页面并解析文档
    re_match=r'<div data-gcjid=.*? data-index=.*?>\n<a href="/(.*?)/#pvareaid=.*?">(.*?)</a>\n</div>'#汽车车系正则匹配式
    re_match1=r'<div data-gcjid=.*? data-index=.*?><a href="/(.*?)/#pvareaid=.*?">(.*?)</a></div>'#汽车车系正则匹配式
    re_match2=r'<dl class="hotcar-list">\n<dt><a .*?>(.*?)</a></dt>'
    car_type=re.findall(re_match2,str(content), re.S|re.M)#汽车类型
    car_name=re.findall(re_match,str(content), re.S|re.M)#汽车车系
    car_name1=re.findall(re_match1,str(content), re.S|re.M)#汽车车系
    car_url="https://www.autohome.com.cn/ashx/AjaxIndexHotCar.ashx"#车型数据
    flag=1
    time.sleep(1)
    while flag==1:
        try:
            res=requests.get(car_url,timeout=5).content#车型数据页面
            flag=0
        except:
            flag=1
            print('停止爬取60s')
            time.sleep(60)
    #res=requests.get(car_url).content#车型数据页面
    car_list=json.loads(res.decode('GBK'))#车型数据列表
    hotcar_url="https://api.mall.autohome.com.cn/gethomead/120100?_appid=cms"#特卖车标签链接
    flag=1
    time.sleep(1)
    while flag==1:
        try:
            res_hotcar=requests.get(hotcar_url,timeout=5).content#特卖车页面
            flag=0
        except:
            flag=1
            print('停止爬取60s')
            time.sleep(60)
    #res_hotcar=requests.get(hotcar_url).content#特卖车页面
    #res_hotcar=str(res_hotcar.decode('utf-8'))
    hostcar_list=json.loads(res_hotcar.decode('utf-8'))#特卖车列表
    hotcar_id=[]
    for i in range(len(hostcar_list['result']['list'])):#获取特卖车的ID
        hotcar_id.append(hostcar_list['result']['list'][i]['seriesId'])
    cocars_list=[]#总车系列表
    car_idname={}#汽车id与名称的词典
    cocars_list.append(['汽车ID','车名','车型','是否有特卖标签','在汽车之家首页的位置'])
    for i in range(len(car_name)-1):#提取首页第一列车的数据
        cars_list=[]
        cars_list.append(car_name[i][0])#汽车id
        cars_list.append(car_name[i][1])#汽车名称
        car_idname[car_name[i][0]]=car_name[i][1]
        cars_list.append(car_type[0])#汽车类型
        if int(car_name[i][0]) in hotcar_id:#是否有特卖标签
            cars_list.append(1)
        else:
            cars_list.append(0)
        cars_list.append(i+1)#首页出现的位置
        cocars_list.append(cars_list)
    for i in range(len(car_name1)-1):#提取首页二、三列车的数据
        cars_list=[]
        cars_list.append(car_name1[i][0])
        cars_list.append(car_name1[i][1])
        car_idname[car_name1[i][0]]=car_name1[i][1]
        if i < 24:
            cars_list.append(car_type[1])
        else:
            cars_list.append(car_type[2])
        if int(car_name1[i][0]) in hotcar_id:
            cars_list.append(1)
        else:
            cars_list.append(0)
        if i < 24:
            cars_list.append(i+1)
        else:
            cars_list.append(i-23)
        cocars_list.append(cars_list)
    for i in range(len(car_list)):#提取其他车系的数据
        for j in range(len(car_list[i]['SeriesList'])):
            cars_list=[]
            cars_list.append(car_list[i]['SeriesList'][j]['Id'])
            cars_list.append(car_list[i]['SeriesList'][j]['Name'])
            car_idname[car_list[i]['SeriesList'][j]['Id']]=car_list[i]['SeriesList'][j]['Name']
            cars_list.append(car_list[i]['Name'])
            if car_list[i]['SeriesList'][j]['Id'] in hotcar_id:
                cars_list.append(1)
            else:
                cars_list.append(0)
            cars_list.append(j+1)
            cocars_list.append(cars_list)
    time.sleep(5)
    print('汽车之家首页的汽车数据爬取结束')
    return cocars_list

        
def Getcardata(cocars_list):
    print("开始爬取车系首页数据...")
    cocars_list[0].extend(['关注排名','用户评分','口碑数量','图片数量','视频数量','新车百车故障数'])
    #proxies=entry.get_random_ip(ip_list)#随机获取代理ip
    for i in range(1,len(cocars_list)):
        print(i,'/',len(cocars_list)-1)      
        car_url='https://www.autohome.com.cn/%d/#pvareaid=103177'%int(cocars_list[i][0])#车系首页
        #flag=1#代理ip标志
        #while flag==1:
        flag=1
        while flag==1:
            try:
                result=requests.get(car_url,timeout=5)
                flag=0
            except:
                flag=1
                print('停止爬取60s')
                time.sleep(60)
        #result=requests.get(car_url)
        #flag=0
        #proxies=entry.get_random_ip(ip_list)#随机获取代理ip
        #print('尝试另一个代理IP爬取')
        content = BeautifulSoup(result.text, "html.parser")
        re_rank='<div class="subnav-title-rank">.*?<span class="red">\xa0(.*?)</span></div>'
        rank=re.findall(re_rank,str(content), re.S|re.M)#关注排名
        re_score='<a class="font-score" href=.*?>(.*?)</a>'
        score=re.findall(re_score,str(content),re.S|re.M)#用户评分
        re_count='<span class="count"><a href=.*?>(.*?)条口碑</a></span>'
        cupcount=re.findall(re_count,str(content),re.S|re.M)#口碑数量
        re_image='<span>实拍图片(.*?)张</span>'
        imagecount=re.findall(re_image,str(content),re.S|re.M)#图片数量
        re_movie='<span>视频(.*?)个</span>'
        moviecount=re.findall(re_movie,str(content),re.S|re.M)#视频数量
        re_fault='<a class="fn-left font-fault" href=".*?">(.*?)</a>'
        faultcount=re.findall(re_fault,str(content),re.S|re.M)#新车百车故障数
        if len(rank)==0:
            rank.append('暂无')
        if len(score)==0:
            score.append('暂无')
        if len(cupcount)==0:
            cupcount.append('暂无')
        if len(imagecount)==0:
            imagecount.append('暂无')
        if len(moviecount)==0:
            moviecount.append('暂无')
        if len(faultcount)==0:
            faultcount.append('暂无')
        cocars_list[i].extend([rank[0],score[0],cupcount[0],imagecount[0],moviecount[0],faultcount[0]])
        time.sleep(1)    
#==============================================================================
#     with open(r'D:\My Documents\Python Scripts\autohomecrawling\cocars_list.csv','w',newline='') as myFile:      
#         myWriter=csv.writer(myFile)       
#         for i in cocars_list:   
#             try:
#                 myWriter.writerow(i)
#             except UnicodeEncodeError:
#                 continue         
#         myFile.close()
#     time.sleep(5)
#==============================================================================
    print("车系首页数据爬取结束")    
    return cocars_list    
        
        









