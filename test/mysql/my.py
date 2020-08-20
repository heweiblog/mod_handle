#!/usr/bin/python
# -*- coding: utf-8 -*-

''''' 
采用三种方法测试mysql.connector对mysql的写入性能,其他的例如mysqldb和pymysql客户端库的写入性能应该和mysql.connector一致 
采用批量写入时,由于减少了网络传输的次数因而速度加快 
开启事务,多次写入后再提交事务,其写入速度也会显著提升,这是由于单次的insert,数据库内部也会开启事务以保证一次写入的完整性 
如果开启事务,在事务内执行多次写入操作,那么就避免了每一次写入都开启事务,因而也会节省时间 
从测试效果来看,事务加批量写入的速度大概是批量写入的3倍,是普通写入的50倍 
数量  普通写入   many写入  事务加many写入 
1万  26.7s  1.7s    0.5s 
10万  266s   19s    5s 
100万 2553s   165s    49s 
  
将autocommit设置为true,执行insert时会直接写入数据库,否则在execute 插入命令时,默认开启事物,必须在最后commit,这样操作实际上减慢插入速度 
此外还需要注意的是mysql的数据库存储引擎如果是MyISAM,那么是不支持事务的,InnoDB 则支持事务 
'''
import time 
import sys 
import mysql.connector 
reload(sys) 
sys.setdefaultencoding('utf-8') 
  
config = { 
    'host': '127.0.0.1', 
    'port': 3306, 
    'database': 'testsql', 
    'user': 'root', 
    'password': 'sheng', 
    'charset': 'utf8', 
    'use_unicode': True, 
    'get_warnings': True, 
    'autocommit':True
  } 
  
conn = mysql.connector.connect(**config) 
cur = conn.cursor() 
  
def time_me(fn): 
  def _wrapper(*args, **kwargs): 
    start = time.time() 
    fn(*args, **kwargs) 
    seconds = time.time() - start 
    print u"{func}函数每{count}条数数据写入耗时{sec}秒".format(func = fn.func_name,count=args[0],sec=seconds) 
  return _wrapper 
  
#普通写入 
@time_me
def ordinary_insert(count): 
  sql = "insert into stu(name,age,class)values('test mysql insert',30,8)"
  for i in range(count): 
    cur.execute(sql) 
  
  
  
#批量 
@time_me
def many_insert(count): 
  sql = "insert into stu(name,age,class)values(%s,%s,%s)"
  
  loop = count/20
  stus = (('test mysql insert', 30, 30), ('test mysql insert', 30, 31), ('test mysql insert', 30, 32), ('test mysql insert', 30, 32) 
         ,('test mysql insert', 30, 32), ('test mysql insert', 30, 32), ('test mysql insert', 30, 32), ('test mysql insert', 30, 32), 
         ('test mysql insert', 30, 32), ('test mysql insert', 30, 32) 
        ,('test mysql insert', 30, 30), ('test mysql insert', 30, 31), ('test mysql insert', 30, 32), ('test mysql insert', 30, 32) 
         ,('test mysql insert', 30, 32), ('test mysql insert', 30, 32), ('test mysql insert', 30, 32), ('test mysql insert', 30, 32), 
         ('test mysql insert', 30, 32), ('test mysql insert', 30, 32)) 
  #并不是元组里的数据越多越好 
  for i in range(loop): 
    cur.executemany(sql, stus) 
  
#事务加批量 
@time_me
def transaction_insert(count): 
  sql = "insert into stu(name,age,class)values(%s,%s,%s)"
  insert_lst = [] 
  loop = count/20
  
  stus = (('test mysql insert', 30, 30), ('test mysql insert', 30, 31), ('test mysql insert', 30, 32), ('test mysql insert', 30, 32) 
         ,('test mysql insert', 30, 32), ('test mysql insert', 30, 32), ('test mysql insert', 30, 32), ('test mysql insert', 30, 32), 
         ('test mysql insert', 30, 32), ('test mysql insert', 30, 32) 
        ,('test mysql insert', 30, 30), ('test mysql insert', 30, 31), ('test mysql insert', 30, 32), ('test mysql insert', 30, 32) 
         ,('test mysql insert', 30, 32), ('test mysql insert', 30, 32), ('test mysql insert', 30, 32), ('test mysql insert', 30, 32), 
         ('test mysql insert', 30, 32), ('test mysql insert', 30, 32)) 
  #并不是元组里的数据越多越好 
  for i in range(loop): 
    insert_lst.append((sql,stus)) 
    if len(insert_lst) == 20: 
      conn.start_transaction() 
      for item in insert_lst: 
        cur.executemany(item[0], item[1]) 
      conn.commit() 
      print '0k'
      insert_lst = [] 
  
  if len(insert_lst) > 0: 
    conn.start_transaction() 
    for item in insert_lst: 
      cur.executemany(item[0], item[1]) 
    conn.commit() 
  
def test_insert(count): 
  ordinary_insert(count) 
  many_insert(count) 
  transaction_insert(count) 
  
if __name__ == '__main__': 
  if len(sys.argv) == 2: 
    loop = int(sys.argv[1]) 
    test_insert(loop) 
  else: 
    print u'参数错误'
