#!/usr/bin/env python
# coding: utf-8

# In[101]:


#coding:utf-8
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import pyecharts
plt.rcParams['font.sans-serif']=['SimHei']
get_ipython().magic('matplotlib inline')

def get_url(city='guangzhou'):
    for time in range(201801,201813):
        url='http://lishi.tianqi.com/{}/{}.html'.format(city,time)
        yield url
def get_datas(urls=get_url()):
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
        cookie={"cityPy":"sanming; cityPy_expire=1551775148; UM_distinctid=16928f54c6d0-08753ecf8a3d56-5d4e211f-1fa400-16928f54c6e445; CNZZDATA1275796416=308465049-1551166484-null%7C1551172369; Hm_lvt_ab6a683aa97a52202eab5b3a9042a8d2=1551170359,1551172902; Hm_lpvt_ab6a683aa97a52202eab5b3a9042a8d2=1551172902"}
        for url in urls:
            wb_data=requests.get(url,headers=headers,cookies=cookie)
            #print(wb_data)
            soup=BeautifulSoup(wb_data.content,'html.parser')
            #print(soup)
            date=soup.select('#tool_site > div.tqtongji2 > ul > li:nth-of-type(1) > a')
            #tool_site > div.tqtongji2 > ul:nth-child(2) > li:nth-child(1)
            #print(date)
            max_temp=soup.select('#tool_site > div.tqtongji2 > ul > li:nth-of-type(2)')
            #print(max_temp)
            min_temp=soup.select('#tool_site > div.tqtongji2 > ul > li:nth-of-type(3)')
            weather=soup.select('#tool_site > div.tqtongji2 > ul > li:nth-of-type(4)')
            wind_direction=soup.select('#tool_site > div.tqtongji2 > ul > li:nth-of-type(5)')
            date=[x.text for x in date]
            max_temp=[x.text for x in max_temp[1:]]
            min_temp=[x.text for x in min_temp[1:]]
            weather=[x.text for x in weather[1:]]
            wind_direction=[x.text for x in wind_direction[1:]]
            yield pd.DataFrame([date,max_temp,min_temp,weather,wind_direction]).T
get_datas()
def get_result():
    result=pd.DataFrame()
    for data in get_datas():
        result=result.append(data)
    return result

result=get_result()
print('空数据有：',result.isnull().any().sum())
result.columns=['日期','最高温度','最低温度','天气状况','风向']
result.head(10)

result['日期']=pd.to_datetime(result['日期'])
result['最高温度']=pd.to_numeric(result['最高温度'])
result['最低温度']=pd.to_numeric(result['最低温度'])
result['平均温度']=(result['最高温度']+result['最低温度'])/2

#result.info()

sns.distplot(result['平均温度'])


# In[102]:


sns.countplot(result['天气状况'])


# In[110]:


result['是否降水']=result['天气状况'].apply(lambda x :'未降水' if x in ['晴','多云','阴','雾','浮尘','霾','扬沙'] else '降水')
rain=result.groupby([result['日期'].apply(lambda x : x.month),'是否降水'])['是否降水'].count()

month=[str(i)+'月份' for i in range(1,13)]
is_rain=[rain[i]['降水'] if '降水' in rain[i].index else 0 for i in range(1,13)]
no_rain=[rain[i]['未降水'] if '未降水' in rain[i].index else 0 for i in range(1,13)]
line=pyecharts.Line('各月降水天数统计')

line.add(
    '降水天数',
    month,
    is_rain,
    is_fill=True,
    area_opacity=0.7,
    is_stack=True)

line.add('未降水天数',
         month,no_rain,
         is_fill=True,
         area_opacity=0.7,
         is_stack=True)

line.render('rain.html')

result.groupby(result['日期'].apply(lambda x : x.month)).mean().plot(kind='line')

directions=['北风','西北风','西风','西南风','南风','东南风','东风','东北风']
schema=[]
v=[]
days=result['风向'].value_counts()
for d in directions:
    schema.append((d,100))
    v.append(days[d])
v=[v]
radar=pyecharts.Radar()
radar.config(schema)
radar.add('风向统计',v,is_axisline_show=True)
radar.render('wind.html')

plt.show()


# In[ ]:




