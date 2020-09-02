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

def get_all_proto():
	return to_no_bt_dict_list('dts','dnsqtype',Qtype.query.all()) + to_no_bt_dict_list('dts','gtldomain',Tld.query.all())


