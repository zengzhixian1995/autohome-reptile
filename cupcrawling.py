# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 09:13:13 2018

@author: Administrator
"""

import re 
import requests  
from bs4 import BeautifulSoup
import time
import json
#from urllib.request import urlopen
import csv
#import carcrawling
#from fontTools.ttLib import TTFont
   
def Getcupurl(cocars_list,headers):
    print("开始爬取口碑链接...")
    #headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",  
              #"Accept": "application/json, text/javascript, */*; q=0.01"}
    #ip_list=entry.get_ip_list(ip_url, headers=headers)
    #proxies_useful=[]
    #proxies=entry.get_random_ip(ip_list)
    for i in range(76,len(cocars_list)):
        getcupurl=[]
        print(i,'/',len(cocars_list)-1)
        #proxies=entry.get_random_ip(ip_list)
        #proxies={'http': 'http://120.79.230.8:6666'}
        cup_url='https://k.autohome.com.cn/%d/?pvareaid=2099118#dataList'%int(cocars_list[i][0])
        flag=1
        while flag==1:            
            try:
                result=requests.get(cup_url,headers=headers,timeout=5)
                flag=0
                content = BeautifulSoup(result.text, "html.parser")
                re_title='<title>(.*?)</title>'
                title=re.findall(re_title,str(content), re.S|re.M)
                print(title)
                if '汽车之家' not in title[0]:
                   
                    flag=1
                    print('停止爬取60s')
                    time.sleep(60)
                    #proxies=entry.get_random_ip(ip_list)
                    #print('尝试另一个代理IP爬取')  
#                else:                   
               
            except:
                flag=1
                print('停止爬取60s')
                time.sleep(60)
                #proxies=entry.get_random_ip(ip_list)
                #proxies={'http': 'http://61.135.217.7:80'}
                #print('尝试另一个代理IP爬取')
                   
        #content1=str(content)
        re_page='<span class="page-item-info">共(.*?)页</span>'
        re_cupnumber='<span class="fn-right c999">共有(.*?)条口碑</span>'
        pagenumber=re.findall(re_page,str(content), re.S|re.M)
        cupnumber=re.findall(re_cupnumber,str(content), re.S|re.M)
        if not pagenumber:
            pagenumber.append('1')
        cupurls=[]
        time.sleep(1)
        if cupnumber[0]=='0':
            getcupurl.append(cocars_list[i][0])
        else:
            for j in range(int(pagenumber[0])):
                print('第%d页'%(j+1),'/',pagenumber[0])
                #proxies=entry.get_random_ip(ip_list)
                #proxies={'http': 'http://122.114.31.177:808'}
                cups_url='https://k.autohome.com.cn/%d/index_%d.html?pvareaid=2099118#dataList'%(int(cocars_list[i][0]),j+1)
                flag=1
                while flag==1:
                    try:
                        results=requests.get(cups_url,headers=headers,timeout=5)
                        flag=0
                        contents=BeautifulSoup(results.text, "html.parser")
                        re_title='<title>(.*?)</title>'
                        title=re.findall(re_title,str(contents), re.S|re.M)
                        print(title[0])
                        if '汽车之家' not in title[0]:
                            #response_url = urlopen(cup_url, headers=headers)
                            flag=1
                            print('停止爬取60s')
                            time.sleep(60)
                            #proxies=entry.get_random_ip(ip_list)
                            #print('尝试另一个代理IP爬取')
#                        else:

                    except:
                        flag=1
                        print('停止爬取60s')
                        time.sleep(60)
                        #proxies=entry.get_random_ip(ip_list)
                        #print('尝试另一个代理IP爬取')
                       
                #content2=str(contents)
                #print(content2)
                re_cupurls='<a class="btn btn-small fn-left" href="(.*?)" target="_blank">'
                cupurl=re.findall(re_cupurls,str(contents), re.S|re.M)
                cupurls=cupurls+cupurl
                time.sleep(1)                
            getcupurl.append([cocars_list[i][0],cupurls])
        if len(getcupurl[0])!=2:
            print(cocars_list[i][0]+'车型无口碑')
            continue
        else:            
            cupdatas,cocupcomments=Getcupdata(getcupurl,headers)
    print("口碑链接爬取结束")
    return getcupurl,cupdatas,cocupcomments
    
def Getcupdata(getcupurl,headers):
    print("开始爬取口碑数据...")
    date=time.strftime('%Y%m%d',time.localtime(time.time()))
#==============================================================================
#     wordList = ['一', '七', '三', '上', '下', '不', '中', '档', '比', '油', '泥', '灯',
#                 '九', '了', '二', '五', '低', '保', '光', '八', '公', '六', '养', '内', '冷',
#                 '副', '加', '动', '十', '电', '的', '皮', '盘', '真', '着', '路', '身', '软',
#                 '过', '近', '远', '里', '量', '长', '门', '问', '只', '右', '启', '呢', '味', 
#                 '和', '响', '四', '地', '坏', '坐', '外', '多', '大', '好', '孩', '实', '小',
#                 '少', '短', '矮', '硬', '空', '级', '耗', '雨', '音', '高', '左', '开', '当',
#                 '很', '得', '性', '自', '手', '排', '控', '无', '是', '更', '有', '机', '来']
#==============================================================================
    for i in range(len(getcupurl)):
        cupdatas=[]
        cupdatas.append(['口碑标题','口碑链接','用户','用户主页','购买车型','购车经销商','购车地点','购买时间','裸车购买价','空间','动力','操控','油耗','舒适性','外观','内饰','性价比','购车目的','口碑发表时间','使用机型','浏览量','支持量','评论量','评论ID'])
        for j in range(len(getcupurl[i][1])):
            print(j+1,'/',len(getcupurl[i][1]))
            cupdata=[]
            cupcontent_url='https:'+getcupurl[i][1][j]
            flag=1
            while flag==1:
                try:                    
                    result=requests.get(cupcontent_url,headers=headers,timeout=60)
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
            #contents=str(content)
#==============================================================================
#             re_addtext='<dd class="add-dl-text">(.*?)</dd>'
#             addtext=re.findall(re_addtext,str(content), re.S|re.M)#追加口碑
#             re_style=re.compile(r'<style type="text/css">(.*?)</style>',re.S)#去除css和js
#             re_js=re.compile(r'<script>(.*?)</script>',re.S)
#             addtext[0]=re_style.sub('',addtext[0])
#             addtext[0]=re_js.sub('',addtext[0])
#==============================================================================
            
             #爬取帖子主内容
#==============================================================================
#             re_ttf=",\r\n               url\('(.*?).ttf"
#             ttfurl= re.findall(re_ttf,str(content), re.S|re.M)
#             print(ttfurl)
#             if len(ttfurl)==0:
#                 print('meiyou')
#                 paragraphs='没有爬取到'
#             else:                   
#                 while flag==0:
#                     try:
#                         ttf = requests.get("http:" + ttfurl[0]+'.ttf', stream=True)
#                         flag=1
#                     except:
#                         flag=0
#                         print('停止爬取60s')
#                         time.sleep(60)          
#                 with open("autohome.ttf", "wb") as pdf:
#                     for chunk in ttf.iter_content(chunk_size=1024):
#                         if chunk:
#                             pdf.write(chunk)
#                 # 解析字体库font文件
#                 font = TTFont('autohome.ttf')
#                 uniList = font['cmap'].tables[0].ttFont.getGlyphOrder()
#                 utfList=[]
#                 for uni in uniList[1:]:
#                     utfList.append((r'\u'+uni[3:].lower()).encode('utf-8').decode("unicode_escape"))        
#                 # 获取发帖内容
#                 re_addtext='<dd class="add-dl-text">(.*?)</dd>'
#                 addtext=re.findall(re_addtext,str(content), re.S|re.M)#追加口碑
#                 print (addtext)
#                 paragraphs=''
#                 for text in addtext:
#                     paragraphs=paragraphs+text
#                 for k in range(len(utfList)):
#                     paragraphs = paragraphs.replace(utfList[k],wordList[k])
#                 
#                 #去除标签
#                 re_style=re.compile(r'<style type="text/css">(.*?)</style>',re.S)#去除css和js
#                 re_js=re.compile(r'<script>(.*?)</script>',re.S)
#                 re_span=re.compile(r'<[^>]+>',re.S)
#                 paragraphs=re_style.sub('',paragraphs)
#                 paragraphs=re_js.sub('',paragraphs)
#                 paragraphs=re_span.sub('',paragraphs)
#                 #print (paragraph)
#             cupdata.append(paragraphs)
#==============================================================================
            re_topic='<h3>《(.*?)》</h3>'
            topic=re.findall(re_topic,str(content), re.S|re.M)
            if not topic:
                topic.append('无')
            cupdata.append(topic[0])#标题
            cupdata.append(getcupurl[i][1][j])#口碑链接
            re_username='<div class="user-name">\n<a href="(.*?)" id="ahref_UserId" target="_blank">(.*?)</a>'
            username=re.findall(re_username,str(content), re.S|re.M)#用户名和用户链接
            #username_url='https:'+username[0][0]#用户主页链接
            if not username:
                username.append(['无','无'])
            cupdata.append(username[0][1])#用户名
            cupdata.append(username[0][0])#用户主页
            re_cartype='<dt>购买车型</dt>\n<dd>\n<a href=".*?" target="_blank">(.*?)</a><br/>\n<a href=".*?" target="_blank">(.*?)</a>'
            cattype=re.findall(re_cartype,str(content), re.S|re.M)#购买的车型
            if not cattype:
                cattype.append(['无','无'])
            cupdata.append(cattype[0][0]+';'+cattype[0][1])
            re_place='<span class="js-countryname" data-val="(.*?),(.*?)"></span>'
            placeID=re.findall(re_place,str(content), re.S|re.M)#购买地点的ID
            if placeID:
                place_url='https://k.autohome.com.cn/frontapi/GetDealerInfor?dearerandspecIdlist=%s,%s'%(placeID[0][0],placeID[0][1])
                flag=1
                while flag==1:
                    try:                    
                        re_place=requests.get(place_url,headers=headers,timeout=5).content
                        flag=0
                    except:
                        flag=1
                        print('停止爬取60s')
                        time.sleep(60)
                place=json.loads(re_place.decode('GBK'))
                if place['result']['List']:
                    cupdata.append(place['result']['List'][0]['CompanySimple'])#汽车经销商
                    cupdata.append(place['result']['List'][0]['ProvinceName']+place['result']['List'][0]['CityName']+place['result']['List'][0]['CountryName'])
                else:
                    cupdata.append('无')
                    cupdata.append('无')
            else:
                cupdata.append('无')
                cupdata.append('无')
            re_time='<dt>购买时间</dt>\n<dd .*?>(.*?)</dd>'
            purchasetime=re.findall(re_time,str(content), re.S|re.M)#购买时间
            if not purchasetime:
                purchasetime.append('无')
            cupdata.append(purchasetime[0])
            re_price='<dt>裸车购买价</dt>\n<dd class="font-arial bg-blue">\r\n(.*?)<span class="c999">'
            price=re.findall(re_price,str(content), re.S|re.M)#购买价格
            if not price:
                price.append(0)
            cupdata.append(price[0])
            re_space='<dt>空间</dt>\n.*?<span class="testfont">(.*?)</span></dd>'
            space=re.findall(re_space,str(content), re.S|re.M)#空间
            if not space:
                space.append('0')
            cupdata.append(space[0])
            re_power='<dt>动力</dt>\n.*?<span class="testfont">(.*?)</span></dd>'
            power=re.findall(re_power,str(content), re.S|re.M)#动力
            if not power:
                power.append('0')
            cupdata.append(power[0])
            re_control='<dt>操控</dt>\n.*?<span class="testfont">(.*?)</span></dd>'
            control=re.findall(re_control,str(content), re.S|re.M)#操控
            if not control:
                control.append('0')
            cupdata.append(control[0])
            re_fuel='<dt>油耗</dt>\n.*?<span class="testfont">(.*?)</span></dd>'
            fuel=re.findall(re_fuel,str(content), re.S|re.M)#油耗
            if not fuel:
                fuel.append('0')
            cupdata.append(fuel[0])
            re_comfort='<dt>舒适性</dt>\n.*?<span class="testfont">(.*?)</span></dd>'
            comfort=re.findall(re_comfort,str(content), re.S|re.M)#舒适性
            if not comfort:
                comfort.append('0')
            cupdata.append(comfort[0])
            re_exterior='<dt>外观</dt>\n.*?<span class="testfont">(.*?)</span></dd>'
            exterior=re.findall(re_exterior,str(content), re.S|re.M)#外观
            if not exterior:
                exterior.append('0')
            cupdata.append(exterior[0])
            re_interior='<dt>内饰</dt>\n.*?<span class="testfont">(.*?)</span></dd>'
            interior=re.findall(re_interior,str(content), re.S|re.M)#内饰
            if not interior:
                interior.append('0')
            cupdata.append(interior[0])
            re_value='<dt>性价比</dt>\n.*?<span class="testfont">(.*?)</span></dd>'
            value=re.findall(re_value,str(content), re.S|re.M)#性价比
            if not value:
                value.append('0')
            cupdata.append(value[0])
            re_purpose='<p class="obje">(.*?)</p>'
            purpose=re.findall(re_purpose,str(content), re.S|re.M)#购车目的
            purposes=''
            for pur in purpose:
                purposes=purposes+pur+';'
            cupdata.append(purposes)
            re_ptime='<b>\xa0(.*?)</b>'
            ptime=re.findall(re_ptime,str(content), re.S|re.M)#发表时间
            if not ptime:
                ptime.append('0')
            cupdata.append(ptime[0])
            re_model='<span>来自：(.*?)</span>'
            model=re.findall(re_model,str(content), re.S|re.M)#机型
            if not model:
                model.append('无')
            cupdata.append(model[0])
            re_browse='<span class="fn-left font-arial mr-20">有<span .*?>(.*?)</span>人看过</span>'
            browsenumber=re.findall(re_browse,str(content), re.S|re.M)#浏览量
            if not browsenumber:
                browsenumber.append('0')
            cupdata.append(browsenumber[0])
            re_support='有<label class="supportNumber" .*?>(.*?)</label>人支持该口碑'
            supportnumber=re.findall(re_support,str(content), re.S|re.M)#支持量
            if not supportnumber:
                supportnumber.append('0')
            cupdata.append(supportnumber[0])
            re_comment='<span class="font-arial CommentNumber" id="Comment_(.*?)">(.*?)</span>'
            commentnumber=re.findall(re_comment,str(content), re.S|re.M)#评论量和评论ID
            if not commentnumber:
                commentnumber.append(['0','0'])
            cupdata.append(commentnumber[0][1])
            cupdata.append(commentnumber[0][0])#评论ID
            cupdatas.append(cupdata)
            time.sleep(1)
        with open(r'D:\My Documents\Python Scripts\autohomecrawling\cup\%s口碑数据%s.csv'%(getcupurl[i][0],date),'w',newline='',encoding='gbk') as myFile:      
            myWriter=csv.writer(myFile)       
            for k in cupdatas:
                try:
                    myWriter.writerow(k)
                except UnicodeEncodeError:
                    continue
            myFile.close()
        cocupcomments=Getcupcomment(cupdatas,headers,getcupurl[i][0])
    print("口碑数据爬取结束")
    return cupdatas,cocupcomments

def Getcupcomment(cupdatas,headers,carid):
    date=time.strftime('%Y%m%d',time.localtime(time.time()))
    cupcomments=[]
    cupcomments.append(['评论内容','评论楼层','用户名','用户ID','用户性别','评论时间','使用设备','回复人ID'])
    print("开始爬取口碑评论")
    for i in range(1,len(cupdatas)):
        print(i,'/',len(cupdatas)-1)      
        cupcomments.append([cupdatas[i][0],cupdatas[i][1]])
        if int(cupdatas[i][23])==0:
                continue;
        for j in range(int(int(cupdatas[i][22])//10)+1):            
            cupcomment_url='https://reply.autohome.com.cn/ShowReply/ReplyJsonredis.ashx?count=10&page=%d&id=%d&appid=5'%(j+1,int(cupdatas[i][23]))
            flag=1
            while flag==1:          
                try:
                    result=requests.get(cupcomment_url,headers=headers,timeout=5).content
                    flag=0
                except:
                    flag=1
                    print('停止爬取60s')
                    time.sleep(60)
            cup_comment=json.loads(result.decode('GBK'))
            if cup_comment['commentlist']:             
                for k in range(len(cup_comment['commentlist'])):
                    cupcomment=[]
                    cupcomment.append(cup_comment['commentlist'][k]['RContent'])#评论内容
                    cupcomment.append(cup_comment['commentlist'][k]['RFloor'])#评论楼层
                    cupcomment.append(cup_comment['commentlist'][k]['RMemberName'])#用户名
                    cupcomment.append(cup_comment['commentlist'][k]['RMemberId'])#用户ID
                    cupcomment.append(cup_comment['commentlist'][k]['RMemberSex'])#用户性别
                    cupcomment.append(cup_comment['commentlist'][k]['replydate'])#评论时间
                    cupcomment.append(cup_comment['commentlist'][k]['SpType'])#使用设备
                    cupcomment.append(cup_comment['commentlist'][k]['RTargetMemberId'])#回复人ID
                    cupcomments.append(cupcomment)
            else:
                cupcomments.append('无评论')
        time.sleep(1)
    with open(r'D:\My Documents\Python Scripts\autohomecrawling\cup\%s口碑评论%s.csv'%(carid,date),'w',newline='') as myFile:      
        myWriter=csv.writer(myFile)       
        for i in cupcomments:   
            try:
                myWriter.writerow(i)
            except UnicodeEncodeError:
                continue        
        myFile.close()
    print("口碑评论爬取结束")
    return cupcomments




#if __name__=="__main__":
    #autohome_url='https://www.autohome.com.cn'
    #cocars_list=carcrawling.Getcarsdata(autohome_url)
    #cocars_list=Getcardata(cocars_list)
    #getcupurl=Getcupurl(cocars_list)
    #cupdatas=Getcupdata(getcupurl)
    #cocupcomments=Getcupcomment(cupdatas)

































 
    
    
    
    
    
    
