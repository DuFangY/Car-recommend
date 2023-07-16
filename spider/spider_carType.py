# -*- coding: UTF-8 -*-
# @Time : 2021-03-15 16:25
# @File : splider.py
# @Sofrware : PyCharm
# @Author : Du Fangyuan
import pymysql
import requests
import re


def find_label_url():
    """
    车辆大类型爬取
    :return:
    """
    """dowload html"""
    first_url = "https://www.autohome.com.cn/xian/"  # 汽车之家url
    response = requests.get(first_url)  # 模拟浏览器请求服务器获取html信息
    html = response.text  # 页面、文档取出来可直接用text
    # 因为是匹配任意字符 文本中又有很多回车换行，必须加re.S
    chose_url = re.findall(r'<li class="type(.+?)</li>', html, re.S)  # 懒惰匹配
    """删除多余匹配项"""
    length = len(chose_url)  # 列表长度
    type = re.findall(r'<li class="type(.+?)</a>', html, re.S)  # 懒惰匹配
    # 提取需要的数据
    # 正则表达式：“.*？” 代表匹配接下来的字符 给其加括号代表只接收中间的字符
    # 返回的是列表 因为只有一个元素字符串 [0]是索引 将文字拿出
    # global chose_url
    type_car = []
    url_car = []
    for i in range(length):
        new_url = re.findall(r'">(.*?)" ', chose_url[i], re.S)[0]  # 正则匹配相应url
        new_url = new_url.strip()
        new_url = new_url.replace('<a href="', '')
        new_url = 'https:' + new_url  # 生成相应url
        if (i == 7 or i == 8):  # SUV 和 MPV大类可进一步再区分
            car_type = re.findall(r'<em>(.*?)</em>', type[i], re.S)[0]  # 正则匹配相应车辆类别

            # print(car_type,new_url)
            type_car.append(car_type)
            url_car.append(new_url)
            # url_branch = re.findall(r'<dd>(.+?)</dd>', chose_url[i], re.S)  # SUV MPV更细分类url信息
            # length_branch = len(url_branch)  # 细分个数监测
            # for j in range(length_branch):  # 对每个分类进行url、种类解析
            #     new_url_branch = re.findall(r'href="(.*?)">', url_branch[j], re.S)[0]  # 正则匹配相应细分分支url
            #     car_branch_type = re.findall(r'">(.*?)</a>', url_branch[j], re.S)[0]  # 正则匹配相应细化分支车辆类别
            #
            #     type_car.append(car_branch_type)
            #     url_car.append('https:' + new_url_branch)

        else:  # 其他没有更细划分的车类
            car_type = re.findall(r'<span class="type-name">(.*?)</span>', type[i], re.S)[0]  # 正则匹配相应车辆类别

            type_car.append(car_type)
            url_car.append(new_url)
    return dict(zip(type_car, url_car))


def insert_Typemysql(data_dict):
    # 打开数据库连接
    conn = pymysql.connect(host="127.0.0.1", user="root", password="root", port=3306, database="home_car",
                           charset="utf8")
    # 使用cursor()方法获取游标
    cursor = conn.cursor()
    for key in data_dict:
        print(key, data_dict[key])
        sql = 'INSERT INTO app01_cartype(type_car,url) VALUES (%s,%s)'
        args = (key, data_dict[key])

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


def main():
    data_dict = find_label_url()
    insert_Typemysql(data_dict)  # 车辆类型数据存储中


if __name__ == '__main__':
    main()
