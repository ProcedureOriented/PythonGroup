# In[0]
import pandas as pd
import os
import random
import matplotlib.pyplot as plt
import numpy as np

def getFiles(suffix, folder):
    files = os.listdir(os.getcwd()+os.sep+'%s' %(folder))  # os.getcwd() 获取当前文件的路径 
    # print(files)
    filesList = []
    for i in files:
        if suffix in i:
            filesList.append(i)
    return filesList

def genDF(suffix, folder):
    List = getFiles(suffix, folder)
    DfList = []
    for i in List:
        filepath = os.getcwd()+os.sep+folder+os.sep+i
        df = pd.read_csv(filepath)
        df['tag'] = i[:-4]
        DfList.append(df)
    df = pd.concat(DfList)
    return df

def randomCheck(dataframe, times):
    indexList = list(set(dataframe.index))
    for index in indexList:
        splitdf = dataframe.loc[index].reset_index(drop = True)
        length = splitdf.shape[0]

        for i in range(times):
            rdmList=[]
            while len(rdmList) < 5:
                rdmList.append(random.randint(1,length))

            print('Random index list%i of %s is: ' %(i+1, index), end='')
            print(rdmList)
            print(splitdf.ix[rdmList, ['评分','内容']])
        print('\n')


# In[1]
# 抽样检查
df = genDF('.csv', 'stmresult')
df.set_index('tag', inplace = True)

randomCheck(df, 5)

# In[2]
# 绘制数量直方图
picpath = os.getcwd()+os.sep+'stmresultpic'+os.sep

from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']

indexList = list(set(df.index))
gplist = []
for index in indexList:
    gp = df.loc[index, '评分'].tolist()
    print(index)
    plt.hist(gp, density=0, bins=np.arange(0, 1.05, 0.05), color='steelblue')
    plt.xlabel(index+'情绪评分')   
    plt.ylabel('数量')
    plt.savefig(picpath+'bar %s.png' %(index))
    plt.show()

    gplist.append(gp)#为绘制箱型图做准备

# In[2]
# 绘制箱型图
plt.close()
plt.boxplot(gplist)
plt.title(','.join(indexList))
plt.savefig(picpath+'box.png')
plt.show()

# In[3]
# 绘制密度分度叠加图
plt.close()
plt.figure(figsize=(10,6))
p1 = plt.hist(gplist[0], density=True, color='steelblue', alpha =0.5)
p2 = plt.hist(gplist[1], density=True, color='red', alpha = 0.5)
p3 = plt.hist(gplist[2], density=True, color='green', alpha = 0.5)
plt.title('三组关键词的密度分布图')
plt.xlabel('情绪评分')
plt.ylabel('密度 (%)')
plt.legend([indexList[0], indexList[1], indexList[2]], title='Results')
plt.savefig(picpath+'density.png')
plt.show()

# %%