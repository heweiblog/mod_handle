#!/usr/bin/python
# -*- coding: utf-8 -*-

''''' 
�������ַ�������mysql.connector��mysql��д������,����������mysqldb��pymysql�ͻ��˿��д������Ӧ�ú�mysql.connectorһ�� 
��������д��ʱ,���ڼ��������紫��Ĵ�������ٶȼӿ� 
��������,���д������ύ����,��д���ٶ�Ҳ����������,�������ڵ��ε�insert,���ݿ��ڲ�Ҳ�Ὺ�������Ա�֤һ��д��������� 
�����������,��������ִ�ж��д�����,��ô�ͱ�����ÿһ��д�붼��������,���Ҳ���ʡʱ�� 
�Ӳ���Ч������,���������д����ٶȴ��������д���3��,����ͨд���50�� 
����  ��ͨд��   manyд��  �����manyд�� 
1��  26.7s  1.7s    0.5s 
10��  266s   19s    5s 
100�� 2553s   165s    49s 
  
��autocommit����Ϊtrue,ִ��insertʱ��ֱ��д�����ݿ�,������execute ��������ʱ,Ĭ�Ͽ�������,���������commit,��������ʵ���ϼ��������ٶ� 
���⻹��Ҫע�����mysql�����ݿ�洢���������MyISAM,��ô�ǲ�֧�������,InnoDB ��֧������ 
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
    print u"{func}����ÿ{count}��������д���ʱ{sec}��".format(func = fn.func_name,count=args[0],sec=seconds) 
  return _wrapper 
  
#��ͨд�� 
@time_me
def ordinary_insert(count): 
  sql = "insert into stu(name,age,class)values('test mysql insert',30,8)"
  for i in range(count): 
    cur.execute(sql) 
  
  
  
#���� 
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
  #������Ԫ���������Խ��Խ�� 
  for i in range(loop): 
    cur.executemany(sql, stus) 
  
#��������� 
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
  #������Ԫ���������Խ��Խ�� 
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
    print u'��������'
