# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 10:03:08 2017

@author: zengzhixian

汽车之家文章部分爬取
"""

import re 
import requests  
from bs4 import BeautifulSoup 
import json
import math
import csv
import time
#import carcrawling


#找出文章的最大页数
def FindoutMaxPageNumber(url):
    print("---分析该车系文章的数量---")
    #该车系文章页面链接
    article_url=url+"0/0-0-1-0/"
    flag=1
    while flag==1:
        try:
            result=requests.get(article_url,timeout=5)
            flag=0
            content = BeautifulSoup(result.text, "html.parser")
        except:
            flag=1
            print('停止爬取60s')
            time.sleep(60)
    #print(content)   
    #正则匹配<a href></a>之间的内容        
    res_page = r'<a href="//www.autohome.com.cn/.*?/0/.*?/" target="_self">(.*?)</a>'
    pagenumber= re.findall(res_page,str(content), re.S|re.M)
    maxpage=1
    page=[]
    for value in pagenumber:   
        #只匹配纯数字的值
        number=re.match(r'\d+',value)
        if number:
            page.append(number.group())
    #比较最大的页码
    for i in page:
        if int(i)>int(maxpage):
            maxpage=i
    time.sleep(1)
    return maxpage

#得出每篇文章的url   
def getPageUrl(url):  
    #得到最大页码
    maxpage=int(FindoutMaxPageNumber(url))
    print("---爬取该车系文章的链接---")
    Allarticlelink=[]
    articleview=[]
    #循环输出文章的链接
    for i in range(1,maxpage+1):
        article_url = url+'0/0-0-%d-0/' % (i)
        #正则匹配文章链接
        flag=1
        while flag==1:
            try:
                result=requests.get(article_url,timeout=5)
                flag=0
                content = BeautifulSoup(result.text, "html.parser")
            except:
                flag=1
                print('停止爬取60s')
                time.sleep(60)
        res_view = '<span><i class="icon12 icon12-eye"></i>(.*?)</span>'        
        res_url =r'<h3><a href="(.*?)">(.*?)</a></h3>'
        #print(res_url) 
        link = re.findall(res_url , str(content), re.I|re.S|re.M)
        view = re.findall(res_view , str(content), re.I|re.S|re.M)#浏览量
        Allarticlelink.append(link)
        articleview.append(view)
        time.sleep(1)#间隔1s
    Allarticlelink=sum(Allarticlelink,[])#转换为一维的list
    articleview=sum(articleview,[])#转换为一维的list
    #print(Alllink)
    time.sleep(1)#间隔5s       
    return Allarticlelink,articleview
 
#获取文章评论等信息   
def getComment(url):   
    Alllink,articleview=getPageUrl(url)
    print("---爬取相应文章链接的评论等信息---")
    #content=BeautifulSoup(requests.get('http:'+Alllink[0][0]).text,"html.parser")
    #存放评论等数据
    allcomment=[]
    articledata=[]
    articledata.append(['文章标题','文章链接','发表时间','文章浏览量','文章作者','文章标签','评论数量'])
    #循环输入文章的链接
    for k in range(len(Alllink)):
        print(k+1,'/',len(Alllink))
        #正则匹配文章id
        article=[]
        res_url=r'<a class="read-all" href=".*?articleid=(.*?)" id="reply-all-btn3" rel="nofollow">.*?</a>'#文章链接
        res_time=r'<div class="article-info">.*?<span>\r\n(.*?)</span>.*?</div>'#评论时间'
        res_writer='<a class="editor-link" href=".*?" target="_blank">(.*?)</a>'#编辑
        res_tag='<a href=".*?#pvareaid=101025" target="_blank">(.*?)</a>'
        flag=1
        while flag==1:
            try:
                result=requests.get(('http:'+Alllink[k][0]),timeout=5)
                flag=0
                articleid = BeautifulSoup(result.text, "html.parser")
            except:
                flag=1
                print('停止爬取60s')
                time.sleep(60)
        #print(articleid)
        comment_url=re.findall(res_url , str(articleid), re.I|re.S|re.M)
        if not comment_url:
            continue
        article_time=re.findall(res_time , str(articleid), re.I|re.S|re.M)
        if not article_time:
            article_time.append(0)
        article_writer=re.findall(res_writer,str(articleid), re.I|re.S|re.M)
        article_tag=re.findall(res_tag,str(articleid),re.I|re.S|re.M)
        article.append(Alllink[k][1])#获取文章的标题
        print(Alllink[k][1])
        article.append(Alllink[k][0])#获取文章的链接
        article.append(article_time[0])#获取文章的发表时间
        article.append(articleview[k])#获取文章浏览量
        if len(article_writer)==0:
            article_writer.append('不详')
        article.append(article_writer[0])#获取文章作者
        if len(article_tag)==0:
            article_tag.append('无')
        article_tags=''
        for tag in article_tag:
             article_tags= article_tags+tag+';'
        article.append(article_tags)#获取文章标签
        #评论json链接
        json_url='https://reply.autohome.com.cn/api/comments/show.json?count=50&page=1&id=%d&appid=1'%(int(comment_url[0]))
        flag=1
        while flag==1:
            try:
                res=requests.get(json_url,timeout=5).content
                flag=0
            except:
                flag=1
                print('停止爬取60s')
                time.sleep(60)
        #res=requests.get(json_url).content
        #json解析
        comment=json.loads(res.decode('GBK'))
        commentcount=comment.get('commentcount')       
        article.append(commentcount)#获取评论的数量
        allcomment.append(['文章标题','文章链接','发表时间','文章浏览量','文章作者','文章标签','评论数量'])
        allcomment.append(article)
        articledata.append(article)
        #计算得到评论的页码
        commentpage=math.ceil(commentcount/50)
        allcomment.append(['评论','评论时间','评论楼层','回复楼层','评论者','评论设备','支持人数'])
        #循环获取评论
        for i in range(1,commentpage+1):       
            c_url='https://reply.autohome.com.cn/api/comments/show.json?count=50&page=%d&id=%d&appid=1'%(i,int(comment_url[0]))
            flag=1
            while flag==1:
                try:
                    res_comment=requests.get(c_url,timeout=5).content
                    flag=0
                except:
                    flag=1
                    print('停止爬取60s')
                    time.sleep(60)
            #res_comment=requests.get(c_url).content
            res_comment=json.loads(res_comment.decode('GBK'))
            lenth=len(res_comment.get('commentlist'))
            #获取commentlist json中的数据
            for j in range(0,lenth):
                #存储每条评论的数据
                comment_list=[]
                RContent=res_comment.get('commentlist')[j].get('RContent')#获取用户评论
                replydate=res_comment.get('commentlist')[j].get('replydate')#获取评论时间
                RFloor=res_comment.get('commentlist')[j].get('RFloor')#获取评论的楼层
                if 'Quote' in res_comment.get('commentlist')[j]:
                    Replayfloor=res_comment.get('commentlist')[j].get('Quote').get('RFloor')
                else:                    
                    Replayfloor=0
                RMemberName=res_comment.get('commentlist')[j].get('RMemberName')#获取评论人姓名
                SpType=res_comment.get('commentlist')[j].get('SpType')#获取评论设备
                RUp=res_comment.get('commentlist')[j].get('RUp')
                comment_list.append(RContent)
                comment_list.append(replydate)
                comment_list.append(RFloor)
                comment_list.append(Replayfloor)
                comment_list.append(RMemberName)
                comment_list.append(SpType)
                comment_list.append(RUp)
                allcomment.append(comment_list)
        time.sleep(1)
    time.sleep(1) 
    return allcomment,articledata,len(Alllink)
    
#数据保存到csv
def saveResult(Allcomment,articledata,carname): 
    date=time.strftime('%Y%m%d',time.localtime(time.time()))
    if '/' in carname:
        re_char=re.compile(r'/',re.S)
        carname= re_char.sub('',carname)
    #结果保存的路径 
    with open(r'D:\My Documents\Python Scripts\autohomecrawling\article\%s文章评论%s.csv'%(carname,date),'w',newline='') as myFile:      
        myWriter=csv.writer(myFile)       
        for i in Allcomment:   
            try:
                myWriter.writerow(i)
            except UnicodeEncodeError:
                continue           
        myFile.close()
    with open(r'D:\My Documents\Python Scripts\autohomecrawling\article\%s文章%s.csv'%(carname,date),'w',newline='') as myFile:      
        myWriter=csv.writer(myFile)       
        for i in articledata:   
            try:
                myWriter.writerow(i)
            except UnicodeEncodeError:
                continue           
        myFile.close()

            
            

#==============================================================================
# if __name__=="__main__":
#     autohome_url='https://www.autohome.com.cn'
#     cocars_list=carcrawling.Getcarsdata(autohome_url)
#     #输入汽车之家车系首页地址
#     for i in range(1,len(cocars_list)):
#         car_url='https://www.autohome.com.cn/%d/'%int(cocars_list[i][0])
#         print("---开始爬取第%d数据---",int(cocars_list[i][0]))
#         #找到该车系文章的评论
#         Allcomment=getComment(car_url)
#         print("---保存数据---")
#         #保存数据
#         saveResult(Allcomment)
#         #Allarticlelink=getPageUrl(car_url)
#         #print(len(Allarticlelink))
#         print("---success!---")
#==============================================================================


def articlecrawling(cocars_list):
    cocars_list[0].extend(['文章数量'])
    for i in range(163,len(cocars_list)):
        print(i,'/',len(cocars_list)-1)
        car_url='https://www.autohome.com.cn/%d/'%int(cocars_list[i][0])
        print("---开始爬取%s的文章数据---"%(cocars_list[i][1]))
        #找到该车系文章的评论
        Allcomment,articledata,articlenumbers=getComment(car_url)
        cocars_list[i].extend([articlenumbers])
        print("---保存数据---")
        #保存数据
        saveResult(Allcomment,articledata,cocars_list[i][1])
        #Allarticlelink=getPageUrl(car_url)
        #print(len(Allarticlelink))
        print("---success!---")
    return cocars_list


































































