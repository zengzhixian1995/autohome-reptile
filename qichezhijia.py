# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 10:03:08 2017

@author: zengzhixian

汽车之家文章评论爬取
"""
import re 
import requests  
from bs4 import BeautifulSoup 
import json
import math
import csv

#找出文章的最大页数
def FindoutMaxPageNumber(url):
    print("---分析该车系文章的数量---")
    #该车系文章页面链接
    article_url=url+"0/0-0-1-0/"
    content = BeautifulSoup(requests.get(article_url).text, "html.parser")
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
    return maxpage

#得出每篇文章的url   
def getPageUrl(url):  
    #得到最大页码
    maxpage=int(FindoutMaxPageNumber(url))
    print("---爬取该车系文章的链接---")
    Allarticlelink=[]
    #循环输出文章的链接
    for i in range(1,maxpage+1):
        article_url = url+'0/0-0-%d-0/' % (i)
        #正则匹配文章链接
        content = BeautifulSoup(requests.get(article_url).text, "html.parser")
        #res_url = r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')"         
        res_url =r'<h3><a href="(.*?)">(.*?)</a></h3>'
        #print(res_url) 
        link = re.findall(res_url , str(content), re.I|re.S|re.M)
        Allarticlelink.append(link)
   
    Allarticlelink=sum(Allarticlelink,[])#转换为一维的list
    #print(Alllink)       
    return Allarticlelink
 
#获取文章评论等信息   
def getComment(url):   
    Alllink=getPageUrl(url)
    print("---爬取相应文章链接的评论等信息---")
    #content=BeautifulSoup(requests.get('http:'+Alllink[0][0]).text,"html.parser")
    #存放评论等数据
    allcomment=[]
    #循环输入文章的链接
    for k in range(0,len(Alllink)):
        #正则匹配文章id
        article=[]
        res_url=r'<a class="read-all" href=".*?articleid=(.*?)" id="reply-all-btn3" rel="nofollow">.*?</a>'
        res_time=r'<div class="article-info">.*?<span>\r\n(.*?)</span>.*?</div>'
        articleid=BeautifulSoup(requests.get('http:'+Alllink[k][0]).text, "html.parser")
        comment_url=re.findall(res_url , str(articleid), re.I|re.S|re.M)
        article_time=re.findall(res_time , str(articleid), re.I|re.S|re.M)
        article.append(Alllink[k][1])#获取文章的标题
        article.append(Alllink[k][0])#获取文章的链接
        article.append(article_time[0])#获取文章的发表时间
        #评论json链接
        json_url='https://reply.autohome.com.cn/api/comments/show.json?count=50&page=1&id=%d&appid=1'%(int(comment_url[0]))
        res=requests.get(json_url).content
        #json解析
        comment=json.loads(res.decode('GBK'))
        commentcount=comment.get('commentcount')       
        article.append(commentcount)#获取评论的数量
        allcomment.append(['文章标题','文章链接','发表时间','评论数量'])
        allcomment.append(article)
        #计算得到评论的页码
        commentpage=math.ceil(commentcount/50)
        allcomment.append(['评论','评论时间','评论楼层','回复楼层','评论者','评论设备'])
        #循环获取评论
        for i in range(1,commentpage+1):       
            c_url='https://reply.autohome.com.cn/api/comments/show.json?count=50&page=%d&id=%d&appid=1'%(i,int(comment_url[0]))
            #print(c_url)
            res_comment=requests.get(c_url).content
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
                comment_list.append(RContent)
                comment_list.append(replydate)
                comment_list.append(RFloor)
                comment_list.append(Replayfloor)
                comment_list.append(RMemberName)
                comment_list.append(SpType)
                allcomment.append(comment_list)
    return allcomment
    
#数据保存到csv
def saveResult(result): 
    #结果保存的路径 
    with open(r'C:\Users\Administrator\Desktop\result.csv','w',newline='') as myFile:      
        myWriter=csv.writer(myFile)
        #myWriter.writerow(['评论','评论时间','评论楼层']) 
        for i in result:    
            myWriter.writerow(i)

    
#输入汽车之家车系首页地址
car_url='http://www.autohome.com.cn/3586/'
print("---开始爬取数据---")
#找到该车系文章的评论
Allcomment=getComment(car_url)
print("---保存数据---")
#保存数据
saveResult(Allcomment)
#Allarticlelink=getPageUrl(car_url)
#print(len(Allarticlelink))
print("---success!---")








































































