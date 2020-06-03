# -*- coding: utf-8 -*-

# In[0]
import pandas as pd
import os
import re
import matplotlib.pyplot as plt
from pylab import mpl
import wordcloud
import jieba
import imageio
from PIL import Image

def getFiles(suffix, folder):
    '''得到文件列表'''
    files = os.listdir(os.getcwd()+os.sep+'%s' %(folder))  # os.getcwd() 获取当前文件的路径 
    # print(files)
    filesList = []
    for i in files:
        if suffix in i:
            filesList.append(i)
    return filesList

def genDF(suffix, folder):
    '''生成dataframe'''
    List = getFiles(suffix, folder)
    DfList = []
    for i in List:
        filepath = os.getcwd()+os.sep+folder+os.sep+i
        df = pd.read_csv(filepath)
        DfList.append(df)
        df = pd.concat(DfList)
    return df

def preProcess(df):
    '''预处理dataframe包括设置关键词和转换日期格式'''
    df.set_index('关键词', inplace = True)
    df.loc[:,'日期'] = pd.to_datetime(df.loc[:,'日期'],format='%Y-%m-%d',errors='coerce')

def mergeImg(btm, tp, path):
    '''合并图片'''
    bottom = Image.open(btm)
    top = Image.open(tp)
    # 权重越大，透明度越低
    mix = Image.blend(bottom, top, 0.1)
    # 保存叠加后的图片
    mix.save(path)

# In[1]
sumdf = genDF('sum.csv', 'mediaresult')
preProcess(sumdf)
sumdf

# In[2]
indexList = list(set(sumdf.index))
mpl.rcParams['font.sans-serif'] = ['SimHei']
List1 = ['武汉', '疫情', '口罩', '医院', '战疫', '钟南山', '肺炎']
List2 = ['熬夜', '吃饭 早饭 午饭 晚饭 夜宵', '睡觉', '起床']
List3 = ['上班', '办公室', '复工', '复产', '工作']
List4 = ['开学 返校 复学']
slist = [List1, List2, List3, List4]
for s in slist:
    df = sumdf.loc[s]
    df.set_index('日期', inplace = True)
    ax = df.plot(title='新闻关键词：'+' '.join(s)) 
    fig = ax.get_figure()
    fig.savefig(os.getcwd()+os.sep+'resultlinefig'+os.sep+'media'+' '.join(s)+'.png')

    blogdf = sumdf.loc[s,['日期', '博客数']]
    blogdf.set_index('日期', inplace = True)
    ax = blogdf.plot(title='新闻关键词：'+' '.join(s)) 
    fig = ax.get_figure()
    fig.savefig(os.getcwd()+os.sep+'resultlinefig'+os.sep+'mediablog'+' '.join(s)+'.png')


# In[3]
dtldf = genDF('detail.csv', 'mediaresult')
preProcess(dtldf)

# In[4]
List1 = ['武汉', '疫情', '口罩', '医院', '战疫', '钟南山', '肺炎']
List2 = ['熬夜', '吃饭 早饭 午饭 晚饭 夜宵', '睡觉', '起床']
List3 = ['上班', '办公室', '复工', '复产', '工作']
List4 = ['开学 返校 复学']
slist = [List1, List2, List3, List4]
sourceimg = ['口罩.png', '沙漏.png', '安全帽.png','书本.jpg']

wordIndexList = list(set(dtldf.index))
for s in slist:
# 下方注释仅用于单文件输出
# if True:
#     s = List4
    codf = dtldf.loc[s, '内容'].tolist()
    codf = [str(i) for i in codf]
    txt = ' '.join(codf)
    if '疫情' in s:
        source = os.getcwd()+os.sep+'resultww'+os.sep+sourceimg[0]
        mask = imageio.imread(source)
    elif '熬夜' in s:
        source = os.getcwd()+os.sep+'resultww'+os.sep+sourceimg[1]
        mask = imageio.imread(source)
    elif '上班' in s:
        source = os.getcwd()+os.sep+'resultww'+os.sep+sourceimg[2]
        mask = imageio.imread(source)
    else:
        source = os.getcwd()+os.sep+'resultww'+os.sep+sourceimg[3]
        mask = plt.imread(source)
    for word in ['/', '@', '#', '【', '】','全文']:
        txt = txt.replace(word, '')
        w = wordcloud.WordCloud(
        width=1000, 
        height=1000, 
        background_color='white',
        # max_words=15,
        mask = mask,
        font_path=r'C:\Windows\Fonts\SourceHanSans-Normal.otf')
    # jieba.del_word(('全文'))
    wr = " ".join(jieba.lcut(txt))
    # print (wr)
    w.generate(" ".join(jieba.lcut(txt)))
    plt.imshow(w)
    plt.axis("off")
    # plt.show()
    outpath = os.getcwd()+os.sep+'resultww'+os.sep+'media'+' '.join(s)+'.png'
    w.to_file(outpath)
    mergeImg(outpath, source, outpath)


# In[5]



# %%
