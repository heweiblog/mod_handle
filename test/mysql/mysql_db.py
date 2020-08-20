#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime
import MySQLdb

# 打开数据库连接
db = MySQLdb.connect("192.168.5.41", "root", "123456", "test", charset='utf8' )

# 使用cursor()方法获取操作游标 
cursor = db.cursor()

# 如果数据表已经存在使用 execute() 方法删除表。
cursor.execute("drop table if exists employee")

# 创建数据表sql语句
sql = """create table employee (
		first_name  char(20) not null,
		last_name  char(20),
		age int,  
		sex char(20),
		income float )"""

cursor.execute(sql)

l = []
for i in range(20000):
	a = (str(i+1),str(i+1),i+1,str(i+1),i+1)
	l.append(a)

# sql 插入语句
sql = """insert into employee(first_name,
		last_name, age, sex, income)
		values (%s, %s, %s, %s, %s)"""
		#values ('mac', 'mohan', 20, 'm', 2000)
try:
	# 执行sql语句
	# cursor.execute(sql)
	begin = datetime.now()
	cursor.executemany(sql,l)
	# 提交到数据库执行
	db.commit()
	end = datetime.now()
	print(end-begin)
except:
	# rollback in case there is any error
	db.rollback()

# 关闭数据库连接
db.close()

