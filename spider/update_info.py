# -*- coding: UTF-8 -*-
# @Time : 2021-04-07 13:17
# @File : update_info.py
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
def update_inf(conn, cursor,num,url,update_count):
    response = requests.get(url)   #模拟浏览器请求服务器获取html信息
    html = response.text    #页面、文档取出来可直接用text
    score = re.findall(r'款口碑(.*?)分</span>',html)   #爬取的最新评分信息
    if not score:  #在售款汽车若无相关口碑评分信息，则口碑评分mysql存入为0.00
        score = 0.00
    sql = 'select score from app01_car where car_url= %s '
    cursor.execute(sql, url)
    sto_score = cursor.fetchone()
    sto_score = ''.join('%s' % a for a in sto_score)   #数据库中的旧评分信息
    if sto_score != score:   #与数据库中评分不一样，需要更新
        sql = 'update app01_car set score = %s  where car_url = %s '
        args = (score,url)
        storge_mysql(sql, args, num, update_count)
    else:
        pass

if __name__ == '__main__':
    conn = pymysql.connect(host="127.0.0.1", user="root", password="root", port=3306, database="home_car",
                           charset="utf8")  # 连接数据库
    # 使用cursor()方法获取游标
    cursor = conn.cursor()
    """
    将在售款车辆口碑 以及 指导价格更新
    """
    update_count = cursor.execute("select car_url from app01_car where sales_inf='在售款'")  # 获得数据个数,获得车辆类型url
    print('需要修改信息的个数->'+str(update_count))   #待更新的信息个数
    car_url = []     #需要检验是否更新的车辆类型
    for i in range(update_count):
        data_url = cursor.fetchone()  # 形成元组
        data_url = ''.join('%s' % a for a in data_url)  # 取掉元组括号
        car_url.append(data_url)
    num = 0    #更新进度显示
    for url in car_url:
        num = num +1
        update_inf(conn, cursor,num,url,update_count)
