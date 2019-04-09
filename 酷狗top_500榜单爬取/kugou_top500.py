#!/usr/bin/env python
# coding: utf-8

# In[45]:


#酷狗音乐榜单top500爬取

#导入相应的库
import requests
from bs4 import BeautifulSoup
import time

#加入请求头
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

#定义获取信息的函数
def get_info(url):
    wb_data=requests.get(url,headers=headers)
    soup=BeautifulSoup(wb_data.text,'lxml')
    ranks=soup.select('div.pc_temp_songlist > ul > li > span.pc_temp_num')
    #print(ranks)
    titles=soup.select('div.pc_temp_songlist > ul > li > a')
    #print(titles)
    times=soup.select('div.pc_temp_songlist > ul > li > span.pc_temp_tips_r > span')
    #print(times)
    for rank,title,time in zip(ranks,titles,times):
        #分割字符串、去空格，获取干净的数据
        data={
            'rank':rank.get_text().strip(),
            'title':title.get_text().split('-')[0],
            'time':time.get_text().strip()
        }
        
        print(data)
        
#主程序
if __name__=='__main__':
    #构造url
    urls=['https://www.kugou.com/yy/rank/home/{}-8888.html'.format(str(i)) for i in range(1,24)]
    for url in urls:
        get_info(url)
    time.sleep(1)


# In[ ]:




