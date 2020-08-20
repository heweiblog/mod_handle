#!/usr/bin/python
# -*- coding:utf-8 -*-
import time
from pymysql import *

# 装饰器，计算插入50000条数据需要的时间
def timer(func):
    def decor(*args):
        start_time = time.time()
        func(*args)
        end_time = time.time()
        d_time = end_time - start_time
        print("the running time is : ", d_time)

    return decor

@timer
def add_test_users():
    
    usersvalues = []
    for num in range(1, 50000):
        usersvalues.append(('需要插入的字段对应的value'))  # 注意要用两个括号扩起来

    conn = connect(host='192.168.5.41', port='3306', user='root', password='123456', database='test', charset='utf8')
    cs = conn.cursor()  # 获取光标
    # 注意这里使用的是executemany而不是execute，下边有对executemany的详细说明
    cs.executemany('insert into 'num'(字段名) values(%s,%s,%s,%s)', usersvalues)

    conn.commit()
    cs.close()
    conn.close()
    print('OK')

add_test_users()
