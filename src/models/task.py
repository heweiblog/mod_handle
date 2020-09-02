#!/usr/bin/python
# -*- coding: utf-8 -*-

import time,json
from common.log import logger
from . import db
from sqlalchemy import and_

class TaskList(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	rcode = db.Column(db.Integer, nullable=False)
	type = db.Column(db.String(40), nullable=False)
	status = db.Column(db.String(40), nullable=False)
	start = db.Column(db.String(40), nullable=False)
	end = db.Column(db.String(40), nullable=False)
	description = db.Column(db.String(400), nullable=False)
	data = db.Column(db.Text, nullable=False)
	result = db.Column(db.Text, nullable=False)

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
		return {'description': self.description, 'rcode':self.rcode, 'taskid':self.id, 'tasktype':self.type,\
		'status': self.status, 'starttime':self.start, 'endtime':self.end, 'result': json.loads(self.result)}


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
			t.result = json.dumps(data['result'])
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


