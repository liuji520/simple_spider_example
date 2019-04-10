#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[76]:


#小猪网广州租房信息爬取
#新版加入了图片滑动验证，待解决。

#导入相应的库
from bs4 import BeautifulSoup
import requests
import time

#加入请求头
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
cookies={'Cookie': 'abtest_ABTest4SearchDate=b; TY_SESSION_ID=24f8b403-d1e9-421b-a44f-f5ef29250517; _uab_collina=155488326523131800675034; gr_user_id=65d84921-c427-4894-b80c-55bceef7571f; grwng_uid=6b521ad4-8dcf-43fc-b35e-cd1cdf250a9b; xzuuid=043e0d18; openAccountLogin=100178070201%7C%7Ca144e51542919338b3b1980558635011%7C%7Cweixinopen%7C%7Chttp%3A%2F%2Fthirdwx.qlogo.cn%2Fmmopen%2Fvi_32%2FajNVdqHZLLAxcfLibZ9gO2drSnf4I7oILUo2fcSPXothJPL7SsMqZN8XfVb0JyicYhLLVTJaoJQpq4FspeiaL5sFA%2F132; xz_guid_4se=a7989055-34ff-4cdd-ac9b-efdda6152167; rule_math=ufbeuctvww8; xzucode4im=fbe56b417cc3e7698b06206b2a55e3e5; xzSessId4H5=876949a97b972498490b97428dd1fa06; newcheckcode=4453726f9e43b57911859d4cec43dfa0; xzuinfo=%7B%22user_id%22%3A100178070201%2C%22user_name%22%3A%2218688514754%22%2C%22user_key%22%3A%22fb4ded3f43%22%2C%22user_nickName%22%3A%22%5Cu5218%5Cu5b63dw%22%7D; xzucode=0d0bee7c9f73fdcf8761bce17509447b; xztoken=WyIyNTA1MDQxMDEwdTAzZSIseyJ1c2VyaWQiOjEwMDE3ODA3MDIwMSwiZXhwaXJlIjowLCJjIjoid2ViIn0sIjc5MDVmNTI0ZTQ2ZjUwNTcwNDY5N2ZmZDdiNmJlMzVmIl0%3D; 59a81cc7d8c04307ba183d331c373ef6_gr_last_sent_sid_with_cs1=b2b5e90b-aee4-47b4-a678-c01bd5959639; 59a81cc7d8c04307ba183d331c373ef6_gr_last_sent_cs1=100178070201; 59a81cc7d8c04307ba183d331c373ef6_gr_cs1=100178070201; 59a81cc7d8c04307ba183d331c373ef6_gr_session_id=b2b5e90b-aee4-47b4-a678-c01bd5959639; 59a81cc7d8c04307ba183d331c373ef6_gr_session_id_b2b5e90b-aee4-47b4-a678-c01bd5959639=true'}
#定义判断用户性别的函数
def judgment_sex(class_name):
    if class_name==['member_icol']:
        return '女'
    else:
        return '男'

#定义获取详细页URL的函数

def get_links(url):
    wb_data=requests.get(url,headers=headers,cookies=cookies)
    soup=BeautifulSoup(wb_data.text,'lxml')
    links=soup.select('#page_list > ul > li > a')
    #print(links)
    for link in links:
        href=link.get("href")
        #print(href)
        get_info(href)

#定义获取网页信息的函数


def get_info(url):
    wb_data=requests.get(url,headers=headers)
    soup=BeautifulSoup(wb_data.text,'lxml')
    #print(soup)
    titles=soup.select('div.wrap.clearfix.con_bg > div.con_l > div.pho_info > h4 > em')
    #print(titles)
    addresses=soup.select('div.wrap.clearfix.con_bg > div.con_l > div.pho_info > p > span')
    #print(addresses)
    prices=soup.select('#pricePart > div.day_l > span')
    #print(prices)
    imgs=soup.select('#floatRightBox > div.js_box.clearfix > div.member_pic > a > img')
    #print(imgs)
    names=soup.select('#floatRightBox > div.js_box.clearfix > div.w_240 > h6 > a')
    #print(names)
    sexs=soup.select('#floatRightBox > div.js_box.clearfix > div.member_pic > div')
    #print(sexs)
    for  title,address,price,img,name,sex in zip(titles,addresses,prices,imgs,names,sexs):
        data={
            'title':title.get_text(),
            'address':address.get_text().strip(),
            'price':price.get_text(),
            'img':img.get('src'),
            'name':name.get_text(),
            'sex':judgment_sex(sex.get('class'))
        }
        print(data)

#主程序入口

if  __name__=='__main__':
    urls=['http://gz.xiaozhu.com/search-duanzufang-p{}-0/'.format(str(i)) for i in range(1,14)]
    for single_url in urls:
        get_links(single_url)
        time.sleep(10)


# In[ ]:




