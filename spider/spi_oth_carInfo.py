# -*- coding: UTF-8 -*-
# @Time : 2021-03-16 12:55
# @File : 0.py
# @Sofrware : PyCharm
# @Author : Du Fangyuan
from __future__ import division
import pymysql
import requests
import re


def re_web(url):
    first_url = url  # 汽车之家url
    response = requests.get(first_url)  # 模拟浏览器请求服务器获取html信息
    html = response.text  # 页面、文档取出来可直接用text
    return html


def other_car(url, conn, cursor, type_name, count, t_name):
    """
    除新能源车型外的第一次页面信息爬取
    :param url:
    :param conn:
    :param cursor:
    :param type_name:
    :param count:
    :param t_name:
    :return:
    """
    html = re_web(url)
    second_url = re.findall(r'<h4><a href="(.*?)口碑', html, re.S)  # 截取部分有用html
    car_url = []
    car_name = []
    car_price = []
    sql = 'INSERT INTO app01_car(name,type ,car_url,price,score) VALUES (%s,%s,%s,%s)'
    for key in second_url:
        c_a = re.search(r'(.*?)"', key)
        c_a = "http:" + c_a.group().replace('"', "")
        car_url.append(c_a)  # 获取车辆url
        name = re.search(r'">(.+?)<', key)
        name = name.group().replace("<", "")
        name = name.replace('">', "")
        car_name.append(name)  # 获取车辆名称
        """
        获取车辆价格
        """
        price = re.search(r'指导价(.*?)报价', key).group()
        if (re.search("指导价：暂无", price)):
            price = "暂无指导价"
            car_price.append(price)
        else:
            price = re.search(r'">(.*?)<', price).group()
            price = price.replace(">", "")
            price = price.replace("<", "")
            car_price.append(price)
        args = (name, type_name, c_a, price)
        storge_mysql(sql, args, count, t_name) #数据库存储


def storge_mysql(sql, args, count, number):
    """
    数据库存储信息
    :param sql:
    :param args:
    :param count:
    :param number:
    :return:
    """
    try:
        print("爬取存储中......", end="")
        # 执行sql语句
        #     args = ("在售款",car_score,img_Url)
        cursor.execute(sql, args)

        # 提交到数据库执行
        conn.commit()
        print("已完成", "%.2f%%" % (count / number * 100))  # 输出爬取完成百分数
    except  Exception as e:
        print(str(e))
        print("已完成", "%.2f%%" % (count / number * 100))
        conn.rollback()


def img_sco_info(conn, cursor, url, count, c_url):
    """
    除新能源车型外的二次页面信息爬取
    :param conn:
    :param cursor:
    :param url:
    :param count:
    :param c_url:
    :return:
    """
    html = re_web(url)
    """
    判断此车有没有停售
    """
    # sale_inf = re.search('<h2>停售款</h2',html).group()
    if (re.search('<h2>停售款</h2', html) is None):  # 元组不为空，此车未停售
        if (re.search(r'款口碑(.*?)分', html)):
            car_score = re.search(r'款口碑(.*?)分', html).group()
            car_score = car_score.replace("款口碑", '')
            car_score = car_score.replace("分", '')
        else:
            car_score = 0
        img_Url = re.search(r'type="image/webp" srcset=(.*?),', html).group()
        img_Url = img_Url.replace('type="image/webp" srcset=', '')
        img_Url = img_Url.replace(",", '')
        img_Url = "https:" + img_Url
        sql = 'update app01_car set sales_inf = %s  where car_url = %s '
        args = ("在售款", url)
        storge_mysql(sql, args, count, c_url)
        sql = 'update app01_car set score = %s  where car_url = %s '
        args = (car_score, url)
        storge_mysql(sql, args, count, c_url)
        sql = 'update app01_car set img_url = %s  where car_url = %s '
        args = (img_Url, url)
        storge_mysql(sql, args, count, c_url)
    else:  # 此车停售
        sql = 'update app01_car set sales_inf = %s  where car_url = %s '
        args = ("停售款", url)
        storge_mysql(sql, args, count, c_url)


if __name__ == '__main__':
    conn = pymysql.connect(host="127.0.0.1", user="root", password="root", port=3306, database="home_car",
                           charset="utf8")  # 连接数据库
    # 使用cursor()方法获取游标
    cursor = conn.cursor()
    t_url = cursor.execute("select url from app01_cartype where nid>=3")  # 获得数据个数,获得车辆类型url
    type_url = []  # 车辆类型url
    type_name = []  # 车辆类型名称
    for i in range(t_url):
        """
        读取数据库车辆类型url
        """
        data_url = cursor.fetchone()  # 形成元组
        data_url = ''.join((data_url))  # 取掉元组括号
        type_url.append(data_url)
    t_name = cursor.execute("select type_car from app01_cartype where nid>=3")  # 获得数据个数,获得各类车辆Type 名称信息
    count = 0  # 计算爬取进度变量初始化
    for i in range(t_name):
        """
        读取数据库相应车辆类型名称
        """
        count = count + 1
        data_url = cursor.fetchone()  # 形成元组
        data_url = ''.join((data_url))  # 取掉元组括号
        type_name.append(data_url)
        """
        爬取车辆类型初始页面
        """
        other_car(i, conn, cursor, data_url, count, t_name)
    change_url = []
    c_url = cursor.execute("select car_url from app01_car where nid >=163")  # 第一次爬取页面无评分，图片地址信息，现在第二次跨页面爬取

    for i in range(c_url):
        """
        读取数据库相应车辆信息页面url
        """
        data_url = cursor.fetchone()  # 形成元组
        data_url = ''.join('%s' % a for a in data_url)  # 转化为str类型,取掉元组括号
        change_url.append(data_url)

    num = 0  # 计算爬取进度变量初始化

    for i in range(c_url):
        """
        进一步爬取相应页面的车辆信息
        """
        num = num + 1
        img_sco_info(conn, cursor, change_url[i], num, c_url)
    cursor.close()
    conn.close()
