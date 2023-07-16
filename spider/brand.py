# -*- coding: UTF-8 -*-
# @Time : 2021-04-08 17:49
# @File : brand.py
# @Sofrware : PyCharm
# @Author : Du Fangyuan
import pymysql
import re
import requests
"""
存储更新的信息
"""
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
        print("信息更新中......", end="")
        # 执行sql语句
        cursor.execute(sql, args)

        # 提交到数据库执行
        conn.commit()
        print("已完成", "%.2f%%" % (count / number * 100))  # 输出爬取完成百分数
    except  Exception as e:
        print(str(e))
        print("已完成", "%.2f%%" % (count / number * 100))
        conn.rollback()
def update_inf(conn, cursor,num,url,brand_count):
    response = requests.get(url)   #模拟浏览器请求服务器获取html信息
    html = response.text    #页面、文档取出来可直接用text
    first_spi = re.findall(r'<a href="/">首页</a>(.*?)</div>',html,re.S)[0]
    car_brand = re.findall(r'.html">(.*?)</a>',first_spi,re.S)[0]
    sql = 'update app01_car set brand = %s  where car_url = %s '
    args = (car_brand,url)
    storge_mysql(sql, args, num, brand_count)

if __name__ == '__main__':
    conn = pymysql.connect(host="127.0.0.1", user="root", password="root", port=3306, database="home_car",
                           charset="utf8")  # 连接数据库
    # 使用cursor()方法获取游标
    cursor = conn.cursor()
    """
    将在售款车辆口碑 以及 指导价格更新
    """
    brand_count = cursor.execute("select car_url from app01_car where sales_inf='在售款'")  # 获得数据个数,获得车辆类型url
    print('需要添加品牌的车辆的个数->'+str(brand_count))   #待更新的信息个数
    car_url = []     #需要检验是否更新车辆品牌的车辆类型
    for i in range(brand_count):
        data_url = cursor.fetchone()  # 形成元组
        data_url = ''.join('%s' % a for a in data_url)  # 取掉元组括号
        car_url.append(data_url)
    num = 0    #更新进度显示
    for url in car_url:
        num = num +1
        update_inf(conn, cursor,num,url,brand_count)
