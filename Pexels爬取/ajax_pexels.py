#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from bs4 import BeautifulSoup
import requests
headers={
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}
urls=['https://www.pexels.com/search/beautiful%20girl/?page={}'.format(i) for i in range(1,10)]
list=[]
for url in urls:
    wb_data=requests.get(url,headers=headers)
    soup=BeautifulSoup(wb_data.text,'lxml')
    imgs=soup.select('body > div.page-wrap > div.l-container > div.photos > div > div > article > a.js-photo-link.photo-item__link > img')
    print(imgs)
    for img in imgs:
        photo=img.get('src')
        list.append(photo)
    path='C:\chapter3\demo\pic\\'
    for item in list:
        data=requests.get(item,headers=headers)
        fp=open(path+item.split('?')[0][-10:],'wb')
        fp.write(data.content)
        fp.close()


# In[ ]:




