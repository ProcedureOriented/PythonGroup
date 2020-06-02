# In[1]
with open('uidlist.txt','r', encoding='utf-8')as f:
    uidlist=f.readlines()
lisst=[]
lis=[]
for uid in uidlist:
    if uid in lis:#防止单个uid被重复统计
        continue
    lis.append(uid)
    try:#为防止uid列表对应的文件不存在，使用try
        with open(uid.replace('\n','')+'.txt','r') as f2:
            #print (uid)
            for i in f2.readlines():#用一个列表存储所有读入的数据，以备后续统一写入
                lisst.append(i)
            lisst.append('\n')
            lisst.append('-1')#每个博主的记录结尾处额外写一行-1，帮助主程序分离名称
            lisst.append('\n')
    except:
        pass
b=0#b用来统计读取的行数，
with open('data.txt','a') as f3:
    for i in lisst:
        f3.write(i)
        b+=1
    f3.write('\n')
    f3.write('0')#总表结尾处添加单独的一行0，作为结束的标志
print(b)

# %%
