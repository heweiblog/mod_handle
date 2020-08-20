#!/usr/bin/python
# -*- coding: utf-8 -*-

import pymysql,json
from configparser import ConfigParser
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

class CrmParser(ConfigParser):
	def as_dict(self):
		d = dict(self._sections)
		for k in d:
			d[k] = dict(d[k])
		return d

config = CrmParser()
config.read('/etc/hcrm.ini')

crm_cfg = config.as_dict()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(crm_cfg['db']['user'],crm_cfg['db']['passwd'],crm_cfg['db']['host'],crm_cfg['db']['port'],crm_cfg['db']['database'])
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class Switch(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	bt = db.Column(db.String(40), nullable=False)
	sbt = db.Column(db.String(40), nullable=False)
	switch = db.Column(db.String(20), nullable=False)

	def __init__(self, bt, sbt, switch):
		self.bt = bt
		self.sbt = sbt
		self.switch = switch

# 批量初始化开关策略
def batch_init_switch():
	try:
		tabs = []
		db_switch = {}
		with open('/var/hcrm/switch.json', 'r') as f:
			db_switch = json.load(f)
		for bt in db_switch:
			for sbt in db_switch[bt]:
				t = {'bt':bt,'sbt':sbt,'switch':db_switch[bt][sbt]}
				tabs.append(t)
		if len(tabs) > 0:
			db.session.execute(Switch.__table__.insert(),tabs)
			db.session.commit()
		return True
	except Exception as e:
		print(str(e))
	return False


class HandleSwitch(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	bt = db.Column(db.String(40), nullable=False)
	sbt = db.Column(db.String(40), nullable=False)
	switch = db.Column(db.String(20), nullable=False)

	def __init__(self, bt, sbt, switch):
		self.bt = bt
		self.sbt = sbt
		self.switch = switch

def batch_init_handle_switch():
	try:
		tabs = []
		db_switch = {}
		with open('/var/hcrm/handle_switch.json', 'r') as f:
			db_switch = json.load(f)
		for bt in db_switch:
			for sbt in db_switch[bt]:
				t = {'bt':bt,'sbt':sbt,'switch':db_switch[bt][sbt]}
				tabs.append(t)
		if len(tabs) > 0:
			db.session.execute(HandleSwitch.__table__.insert(),tabs)
			db.session.commit()
		return True
	except Exception as e:
		print(str(e))
	return False


class TotalThreshold(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	bt = db.Column(db.String(40), nullable=False)
	sbt = db.Column(db.String(40), nullable=False)
	threshold = db.Column(db.BigInteger, nullable=False)

	def __init__(self, bt, sbt, threshold):
		self.bt = bt
		self.sbt = sbt
		self.threshold = threshold

# 批量初始化限速策略
def batch_init_threshold():
	try:
		tabs = []
		db_threshold = {}
		with open('/var/hcrm/threshold.json', 'r') as f:
			db_threshold = json.load(f)
		for bt in db_threshold:
			for sbt in db_threshold[bt]:
				t = {'bt':bt,'sbt':sbt,'threshold':db_threshold[bt][sbt]}
				tabs.append(t)
		if len(tabs) > 0:
			db.session.execute(TotalThreshold.__table__.insert(),tabs)
			db.session.commit()
		return True
	except Exception as e:
		print(str(e))
	return False

def create_db():
	try:
		con = pymysql.connect(host=crm_cfg['db']['host'],port=int(crm_cfg['db']['port']), user=crm_cfg['db']['user'],passwd=crm_cfg['db']['passwd'], charset='utf8')
		cur = con.cursor()
		cur.execute('drop database if exists `{}`;'.format(crm_cfg['db']['database']))
		cur.execute('create database {} character set utf8;'.format(crm_cfg['db']['database']))
		cur.close()
		con.close()
		print('create database {} success;'.format(crm_cfg['db']['database']))
	except Exception as e:
		print(str(e))

try:
	create_db()
	db.create_all()
	batch_init_switch()
	batch_init_handle_switch()
	batch_init_threshold()
	print('hcrm db init success!!!')
except Exception as e:
	print(str(e))



