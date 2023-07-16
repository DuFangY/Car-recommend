# -*- coding: UTF-8 -*-
# @Time : 2021-03-16 1:15
# @File : spider_carInfo.py
# @Sofrware : PyCharm
# @Author : Du Fangyuan
import pymysql
import requests
import re

def re_web(url):
    first_url = url  #汽车之家url
    response = requests.get(first_url)   #模拟浏览器请求服务器获取html信息
    html = response.text    #页面、文档取出来可直接用text
    return html

def energy_car():
    conn = pymysql.connect(host="127.0.0.1", user="root", password="root", port=3306, database="home_car",
                           charset="utf8")
    # 使用cursor()方法获取游标
    cursor = conn.cursor()

    html = re_web("https://ev.autohome.com.cn/#pvareaid=3311257")
    chose_url = re.findall(r'div class="hotcar-content"(.+?)<div id="hotcar-7"', html, re.S)
    # print(chose_url)
    car_url = re.findall(r'<a href="(.*?)">',chose_url[0])
    count =  0
    for url in  car_url:
        car_url[count] = "http:"+ url
        count = count +1
    name = re.findall(r'<p class="text">(.*?)</p>',chose_url[0])
    print(car_url)
    print(name)
    img_url=[]
    price= []
    score =[]
    for url in car_url:
        html = re_web(url)
        img_url.append("http:"+re.findall(r'type="image/webp" srcset="(.+?) 380w', html, re.S)[0])
        price.append(re.findall(r'class="emphasis">(.+?)<em>',html)[0]+"万元")
        sc = re.findall(r'款口碑(.*?)分</span>',html)
        if(sc):
            score.append(sc[0])
        else:
            score.append("0.00")
    # print(price)
    # print(score)
    # print(img_url)
    count = -1
    for key in name:
        count = count + 1
        sql = 'INSERT INTO app01_car(name,type ,car_url,price,score,img_url) VALUES (%s,%s,%s,%s,%s,%s)'
        args = (name[count],"新能源",car_url[count],price[count],score[count],img_url[count])
        try:
            print("爬取存储中......")
            # 执行sql语句
            cursor.execute(sql, args)
            # 提交到数据库执行
            conn.commit()
        except  Exception as e:
            print(str(e))
            conn.rollback()
    conn.close()

energy_car()