#!/usr/bin/python
# -*- coding: utf-8 -*-

from common.log import logger
from . import db


class RegisterList(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	module = db.Column(db.String(40), nullable=False)
	conf_url = db.Column(db.String(200), nullable=False)
	task_url = db.Column(db.String(200), nullable=False)
	ip = db.Column(db.String(60), nullable=False)
	port = db.Column(db.Integer, nullable=False)

	def __init__(self, module, conf_url, task_url, ip, port):
		self.module = module
		self.conf_url = conf_url
		self.task_url = task_url
		self.ip = ip
		self.port = port


def get_all_register():
	try:
		s = RegisterList.query.all()
		if s is not None and len(s) > 0:
			d = {}
			for i in s:
				d[i.module] = {'conf_url': i.conf_url, 'task_url': i.task_url, 'ip': i.ip, 'port': i.port}
			return d
	except Exception as e:
		logger.warning(str(e))
	return None


def put_register(md,data):
	try:
		s = RegisterList.query.filter_by(module=md).first()
		if s is not None:
			s.conf_url = data['conf_url']
			s.task_url = data['task_url']
			s.ip = data['ip']
			s.port = data['port']
			db.session.commit()
		else:
			s = RegisterList(md,data['conf_url'],data['task_url'],data['ip'],data['port'])
			db.session.add(s)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
		db.session.rollback()
	return False


def del_register(md):
	try:
		s = RegisterList.query.filter_by(module=md).first()
		if s is not None:
			db.session.delete(s)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
		db.session.rollback()
	return False



