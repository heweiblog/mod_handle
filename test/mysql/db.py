#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)

'''配置数据库'''
app.config['SECRET_KEY'] = 'dns'#一个字符串，密码。也可以是其他如加密过的

#在此登录的是root用户，要填上密码如123456，MySQL默认端口是3306。并填上创建的数据库名如youcaihua
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@192.168.5.41/test'

#设置下方这行code后，在每次请求结束后会自动提交数据库中的变动
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


db = SQLAlchemy(app)#实例化数据库对象，它提供访问Flask-SQLAlchemy的所有功能

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True)
	email = db.Column(db.String(120), unique=True)

	def __init__(self, username, email):
		self.username = username
		self.email = email

	def __repr__(self):
		return '<User %r>' % self.username

if __name__ == '__main__':
	db.drop_all()
	db.create_all()

	#user_list = []
	for i in range(20):
		me = User(str(i), str(i)+'@example.com')
		#user_list.append(User(str(i), str(i)+'@example.com'))
		db.session.add(me)
	#db.session.add_all(user_list)
	begin = datetime.now()
	print(begin)
	db.session.commit()
	end = datetime.now()
	print(end)
	print(end-begin)
	
	'''
	peter = User.query.filter_by(username='peter').first()
	print(peter,peter.username,peter.email)
	
	db.session.delete(peter)
	db.session.commit()
	
	m = User(peter.username, 'ww.he@yamu.com')
	db.session.add(m)
	db.session.commit()

	peter = User.query.filter_by(username='peter').first()
	print(type(peter),peter,peter.username,peter.email)
	'''
