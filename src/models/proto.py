#!/usr/bin/python
# -*- coding: utf-8 -*-

import time,json
from common.log import logger
from . import db,to_dict_list,to_no_bt_dict_list
from sqlalchemy import and_


class Qtype(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	qtype = db.Column(db.String(40), nullable=False)

	def __init__(self, qtype):
		self.qtype = qtype


# 获取qtype
def get_qtype(data):
	return to_dict_list(Qtype.query.all())


# 添加qtype
def add_qtype(data):
	try:
		p = Qtype.query.filter_by(qtype=data['data']['qtype']).first()
		if p is None:
			p = Qtype(qtype=data['data']['qtype'])
			db.session.add(p)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 删除qtype
def del_qtype(data):
	try:
		p = Qtype.query.filter_by(qtype=data['data']['qtype']).first()
		if p is not None:
			db.session.delete(p)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 清空qtype
def clear_qtype(data):
	try:
		qtype = Qtype.query.all()
		for p in qtype:
			db.session.delete(p)
		db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


qtype_methods = {
	'query': get_qtype,
	'add': add_qtype,
	'delete': del_qtype,
	'clear': clear_qtype
}


class Tld(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	gtld = db.Column(db.String(80), nullable=False)

	def __init__(self, gtld):
		self.gtld = gtld


# 获取tld
def get_tld(data):
	return to_dict_list(Tld.query.all())


# 添加tld
def add_tld(data):
	try:
		p = Tld.query.filter_by(gtld=data['data']['gtld']).first()
		if p is None:
			p = Tld(gtld=data['data']['gtld'])
			db.session.add(p)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 删除tld
def del_tld(data):
	try:
		p = Tld.query.filter_by(gtld=data['data']['gtld']).first()
		if p is not None:
			db.session.delete(p)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 清空tld
def clear_tld(data):
	try:
		gtld = Tld.query.all()
		for p in gtld:
			db.session.delete(p)
		db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


tld_methods = {
	'query': get_tld,
	'add': add_tld,
	'delete': del_tld,
	'clear': clear_tld
}


class TaskList(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	rcode = db.Column(db.Integer, nullable=False)
	type = db.Column(db.String(40), nullable=False)
	status = db.Column(db.String(60), nullable=False)
	start = db.Column(db.String(40), nullable=False)
	end = db.Column(db.String(40), nullable=False)
	description = db.Column(db.String(300), nullable=False)
	data = db.Column(db.String(400), nullable=False)
	result = db.Column(db.String(400), nullable=False)
	#data = db.Column(db.PickleType, nullable=False)

	def __init__(self, type, data):
		self.rcode = 0
		self.type = type
		self.status = 'Executing'
		self.start = time.strftime('%Y-%m-%d %H:%M:%S')
		self.end = ''
		self.description = 'Executing'
		self.data = data
		self.result = ''

	def get_dict(self):
		return {'description': self.description, 'rcode':self.rcode, 'taskID':self.id, 'taskType':self.type, 'status': self.status, 'startTime':self.start,'endTime':self.end, 'result': self.result}


def get_task_list(task_id):
	try:
		rules = TaskList.query.get(task_id)
		if rules is not None:
			return rules.get_dict()
	except Exception as e:
		logger.warning(str(e))
	return None


def add_task_list(data):
	try:
		data_str = json.dumps(data['data'])
		t = TaskList.query.filter(and_(TaskList.type==data['tasktype'],TaskList.data==data_str)).first()
		if t is not None:
			return t.id
		else:
			t = TaskList(data['tasktype'], data_str)
			db.session.add(t)
			db.session.commit()
			t = TaskList.query.filter(and_(TaskList.type==data['tasktype'],TaskList.data==data_str)).first()
			if t is not None:
				return t.id
	except Exception as e:
		logger.warning(str(e))
	return 0


def update_task_list(task_id,data):
	try:
		t = TaskList.query.get(task_id)
		if t is not None:
			t.rcode = data['rcode']
			t.description = data['description']
			t.status = data['status']
			t.end = time.strftime('%Y-%m-%d %H:%M:%S') 
			db.session.commit()
			return True
	except Exception as e:
		logger.warning(str(e))
	return False


def del_task_list(task_id):
	try:
		t = TaskList.query.get(task_id)
		if t is not None:
			db.session.delete(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


def clear_task_list(data):
	try:
		rules = TaskList.query.all()
		if rules is not None:
			for i in rules:
				db.session.delete(i)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


task_list_methods = {
	'query': get_task_list,
	'add': add_task_list,
	'update': update_task_list,
	'delete': del_task_list,
	'clear': clear_task_list
}


def get_all_proto():
	return to_no_bt_dict_list('dts','dnsqtype',Qtype.query.all()) + to_no_bt_dict_list('dts','gtldomain',Tld.query.all())


