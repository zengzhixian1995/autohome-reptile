# -*- coding: utf-8 -*-
"""
Created on Tue Mar  6 20:02:28 2018

@author: Administrator
"""

from bs4 import BeautifulSoup
import requests
import random
import carcrawling
import cupcrawling
import articlecrawling
import bbscrawling
import csv
import time
def get_ip_list(url, headers):
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        if '天' in tds[8].text:
            ip_list.append(tds[5].text.lower()+'://'+tds[1].text + ':' + tds[2].text)
    return ip_list

def get_random_ip(ip_list):
    proxy_list = []
    for ip in ip_list:
        proxy_list.append( ip)
    proxy_ip = random.choice(proxy_list)
    proxies = {proxy_ip.split(":")[0]: proxy_ip}
    return proxies

if __name__ == '__main__':
    date=time.strftime('%Y%m%d',time.localtime(time.time()))
    time_start=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print('开始时间:',time_start)
    #ip_url = 'http://www.xicidaili.com/nn/'#代理ip地址
    autohome_url="https://www.autohome.com.cn"#汽车之家首页
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",  
              "Accept": "application/json, text/javascript, */*; q=0.01"}
    cocarlists=csv.reader(open('D:\\My Documents\\Python Scripts\\autohomecrawling\\车型数据20180316.csv',encoding='gbk'))
    cocars_list=list(cocarlists)
    #ip_list = get_ip_list(ip_url, headers=headers)
    #ip_list =['101.37.79.1:2']  
    #cocarlist=carcrawling.Getcarsdata(autohome_url)#爬取车型数据
    #cocarlists=carcrawling.Getcardata(cocarlist)#爬取车型主页数据
    #cocarlists=articlecrawling.articlecrawling(cocarlists)#爬取车型文章数据
    #getcupurl,cupdatas,cocupcomments=cupcrawling.Getcupurl(cocars_list,headers)#爬取口碑数据内容
    #cupdatas,cocupcomments=cupcrawling.Getcupdata(getcupurl,headers)#爬取口碑数据
    #cupdatas=csv.reader(open('D:\\My Documents\\Python Scripts\\autohomecrawling\\cup\\4253口碑数据20180321.csv',encoding='gbk'))
    #cupdatas=list(cupdatas)
    #cocupcomments=cupcrawling.Getcupcomment(cupdatas,headers,'4253')#爬取口碑评论
    bbscodata,bbsdatas,cocars_list=bbscrawling.bbscrawling(cocars_list,headers)#爬取论坛数据
    #bbsdatas=bbscrawling.bbsdatacrawling(bbscodata,headers)#爬取帖子数据
#==============================================================================
#     with open(r'D:\My Documents\Python Scripts\autohomecrawling\车型数据%s.csv'%date,'w',newline='') as myFile:      
#         myWriter=csv.writer(myFile)       
#         for i in cocars_list:   
#             try:
#                 myWriter.writerow(i)
#             except UnicodeEncodeError:
#                 continue           
#         myFile.close()
#==============================================================================
    time_end=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print('结束时间:',time_end)
    
    
    
    
    
    
    

