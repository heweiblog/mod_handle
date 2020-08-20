#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from sqlalchemy import and_
from . import db,to_dict_list,to_have_bt_dict_list
from common.log import logger

class Switch(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	bt = db.Column(db.String(40), nullable=False)
	sbt = db.Column(db.String(40), nullable=False)
	switch = db.Column(db.String(20), nullable=False)

	def __init__(self, bt, sbt, switch):
		self.bt = bt
		self.sbt = sbt
		self.switch = switch


# 获取开关
def get_switch(data):
	try:
		s = Switch.query.filter(and_(Switch.bt==data['bt'],Switch.sbt==data['sbt'])).first()
		if s is not None:
			return {'switch': s.switch}
	except Exception as e:
		logger.warning(str(e))
	return {'switch': 'disable'}


# 修改开关
def put_switch(data):
	try:
		s = Switch.query.filter(and_(Switch.bt==data['bt'],Switch.sbt==data['sbt'])).first()
		if s is not None:
			s.switch = data['data']['switch']
			db.session.commit()
		else:
			s = Switch(data['bt'],data['sbt'],data['data']['switch'])
			db.session.add(s)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


switch_methods = {
	'query': get_switch,
	'add': put_switch,
	'update': put_switch
}


class HandleSwitch(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	bt = db.Column(db.String(40), nullable=False)
	sbt = db.Column(db.String(40), nullable=False)
	switch = db.Column(db.String(20), nullable=False)

	def __init__(self, bt, sbt, switch):
		self.bt = bt
		self.sbt = sbt
		self.switch = switch


# 获取开关
def get_handle_switch(data):
	try:
		s = HandleSwitch.query.filter(and_(HandleSwitch.bt==data['bt'],HandleSwitch.sbt==data['sbt'])).first()
		if s is not None:
			return {'switch': s.switch}
	except Exception as e:
		logger.warning(str(e))
	return {'switch': 'disable'}


# 修改开关
def put_handle_switch(data):
	try:
		s = HandleSwitch.query.filter(and_(HandleSwitch.bt==data['bt'],HandleSwitch.sbt==data['sbt'])).first()
		if s is not None:
			s.switch = data['data']['switch']
			db.session.commit()
		else:
			s = HandleSwitch(data['bt'],data['sbt'],data['data']['switch'])
			db.session.add(s)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


handle_switch_methods = {
	'query': get_handle_switch,
	'update': put_handle_switch
}


class ViewSwitch(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	bt = db.Column(db.String(40), nullable=False)
	sbt = db.Column(db.String(40), nullable=False)
	view = db.Column(db.String(80), nullable=False)
	switch = db.Column(db.String(20), nullable=False)

	def __init__(self, bt, sbt, view, switch):
		self.bt = bt
		self.sbt = sbt
		self.view = view
		self.switch = switch


# 获取view switch
def get_view_switch(data):
	return to_dict_list(ViewSwitch.query.filter(and_(ViewSwitch.bt==data['bt'],ViewSwitch.sbt==data['sbt'])).all())


# 添加/修改view switch
def modify_view_switch(data):
	try:
		t = ViewSwitch.query.filter(and_(ViewSwitch.bt==data['bt'],ViewSwitch.sbt==data['sbt'],ViewSwitch.view==data['data']['view'])).first()
		if t is not None:
			t.switch = data['data']['switch']
			db.session.commit()
		else:
			t = ViewSwitch(data['bt'], data['sbt'], data['data']['view'], data['data']['switch'])
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


view_switch_methods = {
	'query': get_view_switch,
	'update': modify_view_switch,
}


def get_all_fpga_switch():
	s_list = to_have_bt_dict_list(Switch.query.all())
	for i in s_list:
		if i['bt'] == 'importdnameprotect':
			s_list.remove(i)
	no_list = ['rrfilter','forward','edns','stub','dns64']
	v_list = to_have_bt_dict_list(ViewSwitch.query.all())
	for i in v_list:
		if i['bt'] in no_list: 
			v_list.remove(i)
	return s_list + v_list


def get_all_switch():
	return to_have_bt_dict_list(Switch.query.all()) + to_have_bt_dict_list(ViewSwitch.query.all())

