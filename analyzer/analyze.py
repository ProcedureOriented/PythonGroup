import codecs
import re
import os
import csv
import matplotlib.pyplot as plt
import numpy as np
from snownlp import SnowNLP
from snownlp import sentiment
from snownlp.sentiment import Sentiment

def getFiles(folder):
    '''从文件夹得到文件列表'''
    files = os.listdir(os.getcwd()+os.sep+'%s' %(folder))  # os.getcwd() 获取当前文件的路径 
    print(files)
    filesList = []
    for i in files:
        if (re.match('.*.txt', i)):
            filesList.append(i)
    return filesList

def writecomment(comment, source):
    filepath = './stmresult/%s.csv' %(source)
    if not os.path.exists(filepath):
        with open (filepath, 'w', encoding='utf_8_sig', newline='') as summary:
            csv.writer(summary).writerow(['内容', '评分'])    #不存在则创建文件并写表头
    else:
        with open (filepath, 'a+', encoding='utf_8_sig', newline='') as summary:
            csv.writer(summary).writerow(comment)    #创建关键词日期记录

def snowanalysis(cmtlist, filename):
    sentimentslist = []
    for comment in cmtlist:
        print(comment)
        s = SnowNLP(comment)
        score = s.sentiments

        print(score)
        sentimentslist.append(score)

        writecomment([comment, score], filename)
    plt.hist(sentimentslist, bins=np.arange(0, 1, 0.01))
    plt.show()

        # 对分值进行归一化（尝试修正模型的偏移）
        # score = score*0.5/0.7244678128321579
        # score = (score - score.min()) / (score.max() - score.min())

comments = []

with open('result1.txt', mode='r', encoding='utf_8_sig') as f:
    rows = f.readlines()
    for row in rows:
        if '内容：' in row:
            text = re.sub(r'(?:回复)?(?://)?@[\w\u2E80-\u9FFF]+:?|\[\w+\]', ',', row)
            r='[’！？：；【】，《》!"#$%&\'()（）“”…*+,-./:;<=>?@[\\]^_`{|}~]+'
            text = re.sub(r, '', text)
            text = text.lstrip('内容：')
            comments.append(text.strip('\n'))

snowanalysis(comments, 'result1')