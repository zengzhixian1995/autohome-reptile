# -*- coding: utf-8 -*-
"""
Created on Fri Mar  2 16:05:03 2018

@author: Administrator
"""

import re 
import requests  
from bs4 import BeautifulSoup
import time
import csv
from fontTools.ttLib import TTFont

def bbscrawling(cocars_list,headers):    
    print('开始爬取论坛数据')
    for i in range(1,len(cocars_list)):
        print(i,'/',len(cocars_list)-1)
        bbscodata=[]        
        carbbs_url='https://club.autohome.com.cn/bbs/forum-c-%d-1.html?orderby=dateline&qaType=-1#pvareaid=101061'%int(cocars_list[i][0])
        flag=1
        while flag==1:
            try:
                result=requests.get(carbbs_url,headers=headers,timeout=5)
                flag=0
                contents=BeautifulSoup(result.text, "html.parser")
                re_title='<title>(.*?)</title>'
                title=re.findall(re_title,str(contents), re.S|re.M)
                print(title[0])
                if '汽车之家' not in title[0]:
                    flag=1
                    print('停止爬取60s')
                    time.sleep(60)
            except:
                flag=1
                print('停止爬取60s')
                time.sleep(60)       
        content = BeautifulSoup(result.text, "html.parser")
        re_bbscount='<span>本坛帖子：(.*?)</span>'
        bbscount=re.findall(re_bbscount,str(content), re.S|re.M)#帖子总数
        re_pagenumber='<span class="fr">共(.*?)页</span>'
        pagenumber=re.findall(re_pagenumber,str(content),re.S|re.M)#帖子页数
        bbscodata.append([bbscount[0],pagenumber[0]])
        cocars_list[i].extend(bbscount[0])
        bbscodata.append(['帖子主题','帖子链接','发帖人','发帖人主页','最后回复人','回复人主页','发帖时间','最后回复时间','帖子内容','点击量','回复量'])        
        for j in range(int(pagenumber[0])):
            print(j+1,'/共',pagenumber[0],'页')
            bbs_pageurl='https://club.autohome.com.cn/bbs/forum-c-%d-%d.html?orderby=dateline&qaType=-1#pvareaid=101061'%(int(cocars_list[i][0]),j+1)
            flag=1
            #print(bbs_pageurl)
            while flag==1:
                try:
                    result=requests.get(bbs_pageurl,headers=headers,timeout=5)
                    flag=0
                    contents=BeautifulSoup(result.text, "html.parser")
                    re_title='<title>(.*?)</title>'
                    title=re.findall(re_title,str(contents), re.S|re.M)
                    #print(title[0])
                    if '汽车之家' not in title[0]:
                        flag=1
                        print('停止爬取60s')
                        time.sleep(60)
                except:
                    flag=1
                    print('停止爬取60s')
                    time.sleep(60) 
            content = BeautifulSoup(result.text, "html.parser")
            re_bbstopic='<a class="a_topic" href="(.*?)" target="_blank">\s\n(.*?)</a>'
            bbstopic=re.findall(re_bbstopic,str(content),re.S|re.M)#帖子主题
            re_bbsusername='<a class="linkblack" href="(.*?)" target="_blank">(.*?)</a>'
            bbsusername=re.findall(re_bbsusername,str(content),re.S|re.M)#帖子作者主页与用户名
            re_date='<span class="tdate">(.*?)</span>'
            date=re.findall(re_date,str(content),re.S|re.M)#发帖时间
            re_time='<span class="ttime">(.*?)</span>'
            ttime=re.findall(re_time,str(content),re.S|re.M)#最后回复时间
            for k in range(len(bbstopic)):
                bbsdata=[]
                bbsdata.append(bbstopic[k][1])#帖子主题
                bbsdata.append(bbstopic[k][0])#帖子链接
                bbsdata.append(bbsusername[2*k][1])#发帖人
                bbsdata.append(bbsusername[2*k][0])#发帖人主页
                bbsdata.append(bbsusername[2*k+1][1])#最后回复人
                bbsdata.append(bbsusername[2*k+1][0])#最后回复人主页
                bbsdata.append(date[k])#发帖时间
                bbsdata.append(ttime[k])#最后回复时间
                bbscodata.append(bbsdata)
            time.sleep(1)
        
        bbsdatas=bbsdatacrawling(bbscodata,headers,cocars_list[i][1])
        time.sleep(1)
    time.sleep(1)

    print('论坛数据爬取完成')
    return bbscodata,bbsdatas,cocars_list


def bbsdatacrawling(bbscodata,headers,carname):    
    print('开始爬取帖子数据')
    wordList = ['一', '七', '三', '上', '下', '不', '九', '了', '二', '五', '低', '八',
                '六', '十', '的', '着', '近', '远', '长', '右', '呢', '和', '四', '地', '坏',
                '多', '大', '好', '小', '少', '短', '矮', '高', '左', '很', '得', '是', '更']
    bbsdatas=[]
    bbsdatas.append(['评论','评论人','评论人主页','评论人注册日期','来自地区','发表时间','帖子数量','回复量','精华帖数','关注车型','使用设备','所在楼层','回复楼层'])
    for i in range(2,len(bbscodata)):
        print(i-1,'/',len(bbscodata)-2)
        bbsdatas.append([bbscodata[i][0],bbscodata[i][1]])
        bbs_url='https://club.autohome.com.cn'+bbscodata[i][1]
        flag=1
        while flag==1:
            try:
                result=requests.get(bbs_url,headers=headers,timeout=5)
                flag=0
                content = BeautifulSoup(result.text, "html.parser")
                re_title='<title>(.*?)</title>'
                title=re.findall(re_title,str(content), re.S|re.M)
                print(title[0])
                if '帖子被删除' in title[0]:
                    flag=2
                    break
                if '汽车之家' not in title[0]:
                    flag=1
                    print('停止爬取60s')
                    time.sleep(60)               
            except:
                flag=1
                print('停止爬取60s')
                time.sleep(60)
        if flag==2:
            continue
        #contents=str(content)
        #爬取帖子主内容
        re_ttf=",url\('(.*?).ttf"
        ttfurl= re.findall(re_ttf,str(content), re.S|re.M)
        if len(ttfurl)==0:
            #print('meiyou')
            paragraphs='没有爬取到'
        else:                   
            while flag==0:
                try:
                    ttf = requests.get("http:" + ttfurl[0]+'.ttf', stream=True)
                    flag=1
                except:
                    flag=0
                    print('停止爬取60s')
                    time.sleep(60)          
            with open("autohome.ttf", "wb") as pdf:
                for chunk in ttf.iter_content(chunk_size=1024):
                    if chunk:
                        pdf.write(chunk)
            # 解析字体库font文件
            font = TTFont('autohome.ttf')
            uniList = font['cmap'].tables[0].ttFont.getGlyphOrder()
            utfList=[]
            for uni in uniList[1:]:
                utfList.append((r'\u'+uni[3:].lower()).encode('utf-8').decode("unicode_escape"))        
            # 获取发帖内容
            res_paragraph='<div class="tz-paragraph">(.*?)</div>'
            paragraph= re.findall(res_paragraph,str(content), re.S|re.M)
            paragraphs=''
            for text in paragraph:
                paragraphs=paragraphs+text
            for k in range(len(utfList)):
                paragraphs = paragraphs.replace(utfList[k],wordList[k])
            #print (paragraph)
            #去除标签
            re_span=re.compile(r'<[^>]+>',re.S)
            paragraphs=re_span.sub('',paragraphs)
        re_pagenumber='<span class="fs" title=".*?"> / (.*?) 页' 
        pagenumber=re.findall(re_pagenumber,str(content), re.S|re.M)#总页数
        re_view='<font id="x-views">(.*?)</font>'
        view=re.findall(re_view,str(content), re.S|re.M)#浏览量
        re_reply='<font id="x-replys">(.*?)</font>'
        reply=re.findall(re_reply,str(content), re.S|re.M)#回复量
        bbscodata[i].extend([paragraphs])#帖子内容
        bbscodata[i].extend(view)#点击量
        bbscodata[i].extend(reply)#回复量
        re_number=re.compile(r'1.html',re.S)
        for j in range(int(pagenumber[0])):
            print(j+1,'/帖子',pagenumber[0],'页')
            bbs_urls=re_number.sub(str(j+1)+'.html',bbs_url)
            flag=1
            while flag==1:
                try:
                    result=requests.get(bbs_urls,headers=headers,timeout=5)
                    flag=0
                    content = BeautifulSoup(result.text, "html.parser")
                    re_title='<title>(.*?)</title>'
                    title=re.findall(re_title,str(content), re.S|re.M)
                    print(title[0])
                    if '汽车之家' not in title[0]:
                        flag=1
                        print('停止爬取60s')
                        time.sleep(60)
                except:
                    flag=1
                    print('停止爬取60s')
                    time.sleep(60)
            re_usernameblock='<ul class="maxw">(.*?)</ul>'
            re_leftlist='<ul class="leftlist">(.*?)</ul>'
            re_conright='<div class="conright fl">(.*?)</div>\n<!--end conright-->'
            
            usernameblock=re.findall(re_usernameblock,str(content), re.S|re.M)
            leftlist=re.findall(re_leftlist,str(content), re.S|re.M)
            conright=re.findall(re_conright,str(content), re.S|re.M)
            #bbsdatas.append(conright)
            re_username='<a .*? href="(.*?)" .*? xname="uname">(.*?)</a>'
            re_jinghua='精华：(.*?)帖'
            re_bbsnumber='<li>帖子：<a class="c01439a" href=".*?" target="_blank" title="查看">(.*?)帖</a><span>.*?</span><a class="c01439a" href=".*?" target="_blank" title="查看">(.*?)回</a></li>'
            re_logintime='<li>注册：(.*?)</li>'
            re_place='<li>来自：<a class="c01439a" href=".*?" target="_blank" title="查看该地区论坛">(.*?)</a></li>'
            re_focus='<li>关注：<a class="c01439a" href=".*?" target="_blank" title=".*?">(.*?)</a></li>'
            re_date='<span>发表于 </span><span xname="date">(.*?)</span>'
            re_device='<button class="rightbutlz" data-type="_copy" href="#" name="_clipboard" rel=".*?" style="box-sizing: content-box;color: #3b5998;" title="复制本楼链接到剪贴板">.*?</button>\n</div>\n<span>发表于 </span><span xname="date">.*?</span><span>.*?<a href=".*?" target="_blank">(.*?)</a></span>'            
            re_floor='<button .*?>(.*?)</button>'
            re_reply='发表在 <a .*?>(.*?)</a></p>'
            re_flag=re.compile(r'<[^>]+>',re.S)
            try:
                if j==0:                
                    for k in range(1,len(usernameblock)):
                        bbsdata=[]                                    
                        username=re.findall(re_username,usernameblock[k], re.S|re.M)#用户名
                        if len(username)==0:
                            username.append(['NULL','NULL'])                    
                        jinghua=re.findall(re_jinghua,leftlist[k], re.S|re.M)#精华贴数量
                        if len(jinghua)==0:
                            jinghua.append('NULL')
                        jinghua[0]=re_flag.sub('',jinghua[0])                    
                        bbsnumber=re.findall(re_bbsnumber,leftlist[k], re.S|re.M)#贴子数量和回复量
                        if len(bbsnumber)==0:
                            bbsnumber.append(['NULL','NULL'])                    
                        logintime=re.findall(re_logintime,leftlist[k], re.S|re.M)
                        if len(logintime)==0:
                            logintime.append('NULL')                    
                        place=re.findall(re_place,leftlist[k], re.S|re.M)
                        if len(place)==0:
                            place.append('NULL')                     
                        focus=re.findall(re_focus,leftlist[k], re.S|re.M)                   
                        date=re.findall(re_date,conright[k-1], re.S|re.M)
                        if len(date)==0:
                            date.append('NULL')
                        device=re.findall(re_device,conright[k-1], re.S|re.M)
                        if len(device)==0:
                            device.append('NULL')
                        if 'yy_reply_cont' in conright[k-1]:
                            re_comment='<div class="yy_reply_cont">(.*?)</div>'                    
                            comment=re.findall(re_comment,conright[k-1], re.S|re.M)
                        else:
                            re_comment='<div class="w740">(.*?)</div>\n</div>'                    
                            comment=re.findall(re_comment,conright[k-1], re.S|re.M)
                        floor=re.findall(re_floor,conright[k-1], re.S|re.M)
                        reply=re.findall(re_reply,conright[k-1], re.S|re.M)
                        if not comment:
                            comment.append('无')
                        comment[0]=re_flag.sub('',comment[0])
                        comment[0]=comment[0].strip()
                        bbsdata.append(comment[0])#评论内容
                        bbsdata.append(username[0][1])#回帖人
                        bbsdata.append(username[0][0])#回帖人主页
                        bbsdata.append(logintime[0])#注册时间
                        bbsdata.append(place[0])#来自地区
                        bbsdata.append(date[0])#发表时间
                        bbsdata.append(bbsnumber[0][0])#帖子数量
                        bbsdata.append(bbsnumber[0][1])#回复量
                        bbsdata.append(jinghua[0])#精华贴数
                        if not focus:
                            focus.append('无')
                        bbsdata.append(focus[0])#关注车型
                        if not device:
                            device.append('无')
                        bbsdata.append(device[0])#使用设备
                        if not floor:
                            floor.append('无')
                        bbsdata.append(floor[0])
                        if not reply:
                            reply.append('无')
                        bbsdata.append(reply[0])
                        bbsdatas.append(bbsdata)
                else:
                    for k in range(len(usernameblock)):
                        bbsdata=[]                                    
                        username=re.findall(re_username,usernameblock[k], re.S|re.M)#用户名
                        if len(username)==0:
                            username.append(['NULL','NULL'])                    
                        jinghua=re.findall(re_jinghua,leftlist[k], re.S|re.M)#精华贴数量
                        if len(jinghua)==0:
                            jinghua.append('NULL')
                        jinghua[0]=re_flag.sub('',jinghua[0])                    
                        bbsnumber=re.findall(re_bbsnumber,leftlist[k], re.S|re.M)#贴子数量和回复量
                        if len(bbsnumber)==0:
                            bbsnumber.append(['NULL','NULL'])                     
                        logintime=re.findall(re_logintime,leftlist[k], re.S|re.M)
                        if len(logintime)==0:
                            logintime.append('NULL')                    
                        place=re.findall(re_place,leftlist[k], re.S|re.M)
                        if len(place)==0:
                            place.append('NULL')                     
                        focus=re.findall(re_focus,leftlist[k], re.S|re.M)                    
                        date=re.findall(re_date,conright[k], re.S|re.M)
                        if len(date)==0:
                            date.append('NULL')
                        device=re.findall(re_device,conright[k], re.S|re.M)
                        if len(device)==0:
                            device.append('NULL')
                        if 'yy_reply_cont' in conright[k]:
                            re_comment='<div class="yy_reply_cont">(.*?)</div>'                    
                            comment=re.findall(re_comment,conright[k], re.S|re.M)
                        else:
                            re_comment='<div class="w740">(.*?)</div>\n</div>'                    
                            comment=re.findall(re_comment,conright[k], re.S|re.M)                    
                        floor=re.findall(re_floor,conright[k], re.S|re.M)
                        reply=re.findall(re_reply,conright[k], re.S|re.M)
                        if not comment:
                            comment.append('无')
                        comment[0]=re_flag.sub('',comment[0])
                        comment[0]=comment[0].strip()
                        bbsdata.append(comment[0])#评论内容
                        bbsdata.append(username[0][1])#回帖人
                        bbsdata.append(username[0][0])#回帖人主页
                        bbsdata.append(logintime[0])#注册时间
                        bbsdata.append(place[0])#来自地区
                        bbsdata.append(date[0])#发表时间
                        bbsdata.append(bbsnumber[0][0])#帖子数量
                        bbsdata.append(bbsnumber[0][1])#回复量
                        bbsdata.append(jinghua[0])#精华贴数
                        if not focus:
                            focus.append('无')
                        bbsdata.append(focus[0])#关注车型
                        if not device:
                            device.append('无')
                        bbsdata.append(device[0])#使用设备
                        
                        bbsdata.append(floor[0])#楼层
                        if not reply:
                            reply.append('无')
                        bbsdata.append(reply[0])#回复楼层
                        bbsdatas.append(bbsdata)
            except:
                print('此贴爬取出错')
                break
        time.sleep(1)
    date=time.strftime('%Y%m%d',time.localtime(time.time()))
    if '/' in carname:
        re_char=re.compile(r'/',re.S)
        carname= re_char.sub('',carname)
    with open(r'D:\My Documents\Python Scripts\autohomecrawling\bbs\%s论坛数据%s.csv'%(carname,date),'w',newline='',encoding='gbk') as myFile:      
        myWriter=csv.writer(myFile)       
        for ii in bbscodata:   
            try:
                myWriter.writerow(ii)
            except UnicodeEncodeError:
                continue        
        myFile.close()
    with open(r'D:\My Documents\Python Scripts\autohomecrawling\bbs\%s帖子数据%s.csv'%(carname,date),'w',newline='',encoding='gbk') as myFile:      
        myWriter=csv.writer(myFile)       
        for jj in bbsdatas:   
            try:
                myWriter.writerow(jj)
            except UnicodeEncodeError:
                continue        
        myFile.close()
    print('帖子数据爬取完成')
    return bbsdatas


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    