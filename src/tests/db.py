#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = 'dns'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@192.168.5.41/test'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

class Switch(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	switch_id = db.Column(db.String(20), unique=True)
	status = db.Column(db.Boolean(0), unique=True)

	def __init__(self, switch_id, status):
		self.switch_id = switch_id
		self.status = status
	def get_dict(self):
		return {'switch_id':self.switch_id,'status':self.status}

'''
class Switch(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	#version = db.Column(db.Integer, primary_key=True)
	#version = db.Column(db.Integer, unique=True)
	switch_id = db.Column(db.String(20), unique=True)
	status = db.Column(db.Boolean(0), unique=True)

	#def __init__(self, id, switch_id, status):
	def __init__(self, switch_id, status):
		#self.version = version
		#self.id = id
		self.switch_id = switch_id
		self.status = status
'''

#db.drop_all(bind=['switch'])
#db.create_all(bind=['tmpconf'])
db.drop_all()
db.create_all()
s = Switch('iptables',True)
db.session.add(s)
db.session.commit()

