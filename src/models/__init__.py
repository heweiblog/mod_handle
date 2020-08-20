#!/usr/bin/python
# -*- coding: utf-8 -*-

import pymysql
from common.log import logger
from common.conf import crm_cfg
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def to_dict(ob):
	try:
		d = {c.name: getattr(ob, c.name) for c in ob.__table__.columns}
		del d['id']
		return d
	except Exception as e:
		logger.warning(str(e))
	return None


def to_dict_list(rules):
	try:
		l = []
		for i in rules:
			d = {c.name: getattr(i, c.name) for c in i.__table__.columns}
			if 'bt' in d:
				del d['bt']
			if 'sbt' in d:
				del d['sbt']
			del d['id']
			l.append(d)
		if len(l) > 0:
			return l
	except Exception as e:
		logger.warning(str(e))
	return None


def to_have_bt_dict_list(rules):
	try:
		l = []
		for i in rules:
			data = {c.name: getattr(i, c.name) for c in i.__table__.columns}
			bt = data['bt']
			sbt = data['sbt']
			del data['id']
			del data['bt']
			del data['sbt']
			content = {'source':'ms','id':0,'bt':bt,'sbt':sbt,'op':'add','data':data}
			l.append(content)
		return l
	except Exception as e:
		logger.warning(str(e))
	return []


def to_no_bt_dict_list(bt,sbt,rules):
	try:
		l = []
		for i in rules:
			data = {c.name: getattr(i, c.name) for c in i.__table__.columns}
			del data['id']
			content = {'source':'ms','id':0,'bt':bt,'sbt':sbt,'op':'add','data':data}
			l.append(content)
		return l
	except Exception as e:
		logger.warning(str(e))
	return []



