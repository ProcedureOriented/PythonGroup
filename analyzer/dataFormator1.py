# -*- coding: utf-8 -*-

import re
import os
import csv

def getFiles(folder):
    '''从文件夹得到文件列表'''
    files = os.listdir(os.getcwd()+os.sep+'%s' %(folder))  # os.getcwd() 获取当前文件的路径 
    print(files)
    filesList = []
    for i in files:
        if (re.match('.*.txt', i)):
            filesList.append(i)
    return filesList

def genDate(str,year = 2020):
    '''根据短日期m-d返回长日期yyyy-mm-dd'''
    md = re.split('-',str)
    for i in range(2):
        md[i] = md[i].rjust(2, '0')
    md.insert(0, '%s' %year)
    return '-'.join(md)

def getDetail(str1, totalflag=0):
    '''提取点赞评论转发数字返回列表, totalflag:0，单条微博；1，日微博统计'''
    if totalflag:
        rlt = re.findall(r'博客数：(\d+)，点赞数：(\d+)，评论数：(\d+)，转发数：(\d+)\n', str1)
        return list(rlt[0])
    rlt = re.findall(r'点赞数：(\d+)，评论数：(\d+)，转发数：(\d+)\n', str1)
    return list(rlt[0])

def writeData(ls, keyword, summaryflag=0):
    '''写入数据'''
    if summaryflag:
        filepath = './result/%s-sum.csv' %(keyword)
        if not os.path.exists(filepath):
            with open (filepath, 'w', encoding='utf_8_sig', newline='') as summary:
                csv.writer(summary).writerow(['关键词','日期','博客数','点赞数','评论数','转发数'])    #不存在则创建文件并写表头
        else:
            with open (filepath, 'a+', encoding='utf_8_sig', newline='') as summary:
                csv.writer(summary).writerow(ls)    #创建关键词日期记录
    else:
        filepath = './result/%s-detail.csv' %(keyword)
        if not os.path.exists(filepath):
            with open (filepath, 'w',encoding='utf_8_sig', newline='') as detail:
                csv.writer(detail).writerow(['关键词','博主','内容','日期','点赞数','评论数','转发数'])    #不存在则创建文件并写表头
        else:
            with open (filepath, 'a+', encoding='utf_8_sig', newline='') as detail:
                csv.writer(detail).writerow(ls)    #创建微博记录
        
if __name__=='__main__':
    filename = input('Filename(xxx.txt):')
    with open('./%s' %(filename), 'r', encoding='utf_8_sig') as f:
        line = f.readline()
        while line:     #当line不为EOF
            if line[:3] == '关键词':
                keyword = re.search(r'关键词: ([\s\S]*)\n', line).group(1)
                line = f.readline()
            if line[:2] == '日期':
                date = genDate(re.search(r'日期：([\s\S]*)\n', line).group(1))    #转换标准日期形式
                line = f.readline()
            if line[:2] == '内容':
                content = re.search(r'内容：([\s\S]*)\n', line).group(1)      #得到内容
                line = f.readline()

                blogger = re.search(r'博主：([\s\S]*)\n', line).group(1)      #得到博主
                line = f.readline()

                line = line.lstrip()    #去除开头空格
                detail = getDetail(line)    #得到赞评转数

                result=[keyword, blogger, content, date]+detail    #生成数据记录
                writeData(result, keyword)  #写入
                line = f.readline()
            if line[:2] == '本日':
                detail = getDetail(line, 1)
                result = [keyword,date]+detail
                writeData(result, keyword, 1)
                line = f.readline()
            if line in ['\n','\r\n']:    #如果是空行
                line = f.readline()
