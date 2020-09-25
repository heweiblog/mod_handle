#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from common.log import logger
from sqlalchemy import and_
from . import db,to_dict_list,to_no_bt_dict_list,to_have_bt_dict_list


class HandleSwitch(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	bt = db.Column(db.String(40), nullable=False)
	sbt = db.Column(db.String(40), nullable=False)
	switch = db.Column(db.String(20), nullable=False)

	def __init__(self, bt, sbt, switch):
		self.bt = bt
		self.sbt = sbt
		self.switch = switch


def get_handle_switch(data):
	try:
		s = HandleSwitch.query.filter(and_(HandleSwitch.bt==data['bt'],HandleSwitch.sbt==data['sbt'])).first()
		if s is not None:
			return {'switch': s.switch}
	except Exception as e:
		logger.warning(str(e))
	return {'switch': 'disable'}


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
		db.session.rollback()
	return False


handle_switch_methods = {
	'query': get_handle_switch,
	'add': put_handle_switch,
	'update': put_handle_switch
}

class HandleIpGroup(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	ipgroup = db.Column(db.String(80), nullable=False)
	ip = db.Column(db.String(60), nullable=False)

	def __init__(self, ipgroup, ip):
		self.ipgroup = ipgroup
		self.ip = ip


# 获取所有的handle ip list
def get_handle_ip_group(data):
	return to_dict_list(HandleIpGroup.query.all())


# 添加 handle ip list
def add_handle_ip_group(data):
	try:
		t = HandleIpGroup.query.filter(and_(HandleIpGroup.ipgroup==data['data']['ipgroup'],HandleIpGroup.ip==data['data']['ip'])).first()
		if t is None:
			t = HandleIpGroup(data['data']['ipgroup'], data['data']['ip'])
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
		db.session.rollback()
	return False


# 删除handle ip list 
def del_handle_ip_group(data):
	try:
		if 'ip' in data['data']:
			t = HandleIpGroup.query.filter(and_(HandleIpGroup.ipgroup==data['data']['ipgroup'],HandleIpGroup.ip==data['data']['ip'])).first()
			if t is not None:
				db.session.delete(t)
				db.session.commit()
		else:
			rules = HandleIpGroup.query.filter_by(ipgroup=data['data']['ipgroup']).all()
			if rules is not None:
				for i in rules:
					db.session.delete(i)
				db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
		db.session.rollback()
	return False


# 清空所有的handle ip list
def clear_handle_ip_group(data):
	try:
		rules = HandleIpGroup.query.all()
		if rules is not None:
			for i in rules:
				db.session.delete(i)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
		db.session.rollback()
	return False


handle_ip_group_methods = {
	'query': get_handle_ip_group,
	'add': add_handle_ip_group,
	'delete': del_handle_ip_group,
	'clear': clear_handle_ip_group
}


class HandleTotalThreshold(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	bt = db.Column(db.String(40), nullable=False)
	sbt = db.Column(db.String(40), nullable=False)
	meter = db.Column(db.BigInteger, nullable=False)

	def __init__(self, bt, sbt, meter):
		self.bt = bt
		self.sbt = sbt
		self.meter = meter
	def get_dict(self):
		return {'meter': self.meter}
	def to_dict(self):
		return {'source':'ms','id':0,'bt':self.bt,'sbt':self.sbt,'op':'update','data':{'meter':self.meter}}


def get_all_total_meter():
	return to_dict_list(HandleTotalThreshold.query.all())


# 获取总限速阈值
def get_total_meter(data):
	try:
		t = HandleTotalThreshold.query.filter(and_(HandleTotalThreshold.bt==data['bt'],HandleTotalThreshold.sbt==data['sbt'])).first()
		if t is not None:
			return t.get_dict()
	except Exception as e:
		logger.warning(str(e))
	return None



# 修改总限速阈值
def modify_total_meter(data):
	try:
		t = HandleTotalThreshold.query.filter(and_(HandleTotalThreshold.bt==data['bt'],HandleTotalThreshold.sbt==data['sbt'])).first()
		if t is not None:
			t.meter = data['data']['meter']
			db.session.commit()
		else:
			t = HandleTotalThreshold(data['bt'], data['sbt'], data['data']['meter'])
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
		db.session.rollback()
	return False


total_meter_methods = {
	'query': get_total_meter,
	'add': modify_total_meter,
	'update': modify_total_meter
}


class HandleIpThreshold(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	bt = db.Column(db.String(40), nullable=False)
	sbt = db.Column(db.String(40), nullable=False)
	ip = db.Column(db.String(60), nullable=False)
	meter = db.Column(db.BigInteger, nullable=False)

	def __init__(self, bt, sbt, ip, meter):
		self.bt = bt
		self.sbt = sbt
		self.ip = ip
		self.meter = meter


# 获取所有的ip限速策略
def get_ip_meter(data):
	return to_dict_list(HandleIpThreshold.query.filter(and_(HandleIpThreshold.bt==data['bt'],HandleIpThreshold.sbt==data['sbt'])).all())


# 添加/修改ip限速策略
def modify_ip_meter(data):
	try:
		t = HandleIpThreshold.query.filter(and_(HandleIpThreshold.bt==data['bt'],HandleIpThreshold.sbt==data['sbt'],HandleIpThreshold.ip==data['data']['ip'])).first()
		if t is not None:
			t.meter = data['data']['meter']
			db.session.commit()
		else:
			t = HandleIpThreshold(data['bt'], data['sbt'], data['data']['ip'], data['data']['meter'])
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
		db.session.rollback()
	return False


# 删除ip限速策略
def del_ip_meter(data):
	try:
		t = HandleIpThreshold.query.filter(and_(HandleIpThreshold.bt==data['bt'],HandleIpThreshold.sbt==data['sbt'],HandleIpThreshold.ip==data['data']['ip'])).first()
		if t is not None:
			db.session.delete(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
		db.session.rollback()
	return False


# 清空所有的ip限速策略
def clear_ip_meter(data):
	try:
		rules = HandleIpThreshold.query.filter(and_(HandleIpThreshold.bt==data['bt'],HandleIpThreshold.sbt==data['sbt'])).all()
		if rules is not None:
			for i in rules:
				db.session.delete(i)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
		db.session.rollback()
	return False


ip_meter_methods = {
	'query': get_ip_meter,
	'add': modify_ip_meter,
	'update': modify_ip_meter,
	'delete': del_ip_meter,
	'clear': clear_ip_meter
}



class HandleTagThreshold(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	bt = db.Column(db.String(40), nullable=False)
	sbt = db.Column(db.String(40), nullable=False)
	handle = db.Column(db.String(200), nullable=False)
	meter = db.Column(db.BigInteger, nullable=False)

	def __init__(self, bt, sbt, handle, meter):
		self.bt = bt
		self.sbt = sbt
		self.handle = handle
		self.meter = meter


def get_handle_tag_meter(data):
	return to_dict_list(HandleTagThreshold.query.filter(and_(HandleTagThreshold.bt==data['bt'],HandleTagThreshold.sbt==data['sbt'])).all())


def modify_handle_tag_meter(data):
	try:
		t = HandleTagThreshold.query.filter(and_(HandleTagThreshold.bt==data['bt'],HandleTagThreshold.sbt==data['sbt'],HandleTagThreshold.handle==data['data']['handle'])).first()
		if t is not None:
			t.meter = data['data']['meter']
			db.session.commit()
		else:
			t = HandleTagThreshold(data['bt'], data['sbt'], data['data']['handle'], data['data']['meter'])
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
		db.session.rollback()
	return False


def del_handle_tag_meter(data):
	try:
		t = HandleTagThreshold.query.filter(and_(HandleTagThreshold.bt==data['bt'],HandleTagThreshold.sbt==data['sbt'],HandleTagThreshold.handle==data['data']['handle'])).first()
		if t is not None:
			db.session.delete(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
		db.session.rollback()
	return False


def clear_handle_tag_meter(data):
	try:
		rules = HandleTagThreshold.query.filter(and_(HandleTagThreshold.bt==data['bt'],HandleTagThreshold.sbt==data['sbt'])).all()
		if rules is not None:
			for i in rules:
				db.session.delete(i)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
		db.session.rollback()
	return False


handle_tag_meter_methods = {
	'query': get_handle_tag_meter,
	'add': modify_handle_tag_meter,
	'update': modify_handle_tag_meter,
	'delete': del_handle_tag_meter,
	'clear': clear_handle_tag_meter
}


class HandleIpList(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	bt = db.Column(db.String(40), nullable=False)
	sbt = db.Column(db.String(40), nullable=False)
	ip = db.Column(db.String(60), nullable=False)

	def __init__(self, bt, sbt, ip):
		self.bt = bt
		self.sbt = sbt
		self.ip = ip


def get_handle_ip_list(data):
	return to_dict_list(HandleIpList.query.filter(and_(HandleIpList.bt==data['bt'],HandleIpList.sbt==data['sbt'])).all())


def add_handle_ip_list(data):
	try:
		t = HandleIpList.query.filter(and_(HandleIpList.bt==data['bt'],HandleIpList.sbt==data['sbt'],HandleIpList.ip==data['data']['ip'])).first()
		if t is None:
			t = HandleIpList(data['bt'], data['sbt'], data['data']['ip'])
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
		db.session.rollback()
	return False


def del_handle_ip_list(data):
	try:
		t = HandleIpList.query.filter(and_(HandleIpList.bt==data['bt'],HandleIpList.sbt==data['sbt'],HandleIpList.ip==data['data']['ip'])).first()
		if t is not None:
			db.session.delete(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
		db.session.rollback()
	return False


def clear_handle_ip_list(data):
	try:
		rules = HandleIpList.query.filter(and_(HandleIpList.bt==data['bt'],HandleIpList.sbt==data['sbt'])).all()
		if rules is not None:
			for i in rules:
				db.session.delete(i)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
		db.session.rollback()
	return False


handle_ip_list_methods = {
	'query': get_handle_ip_list,
	'add': add_handle_ip_list,
	'delete': del_handle_ip_list,
	'clear': clear_handle_ip_list
}


class HandleTagList(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	bt = db.Column(db.String(40), nullable=False)
	sbt = db.Column(db.String(40), nullable=False)
	handle = db.Column(db.String(200), nullable=False)

	def __init__(self, bt, sbt, handle):
		self.bt = bt
		self.sbt = sbt
		self.handle = handle


def get_handle_tag_list(data):
	return to_dict_list(HandleTagList.query.filter(and_(HandleTagList.bt==data['bt'],HandleTagList.sbt==data['sbt'])).all())


def add_handle_tag_list(data):
	try:
		t = HandleTagList.query.filter(and_(HandleTagList.bt==data['bt'],HandleTagList.sbt==data['sbt'],HandleTagList.handle==data['data']['handle'])).first()
		if t is None:
			t = HandleTagList(data['bt'], data['sbt'], data['data']['handle'])
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
		db.session.rollback()
	return False


def del_handle_tag_list(data):
	try:
		t = HandleTagList.query.filter(and_(HandleTagList.bt==data['bt'],HandleTagList.sbt==data['sbt'],HandleTagList.handle==data['data']['handle'])).first()
		if t is not None:
			db.session.delete(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
		db.session.rollback()
	return False


def clear_handle_tag_list(data):
	try:
		rules = HandleTagList.query.filter(and_(HandleTagList.bt==data['bt'],HandleTagList.sbt==data['sbt'])).all()
		if rules is not None:
			for i in rules:
				db.session.delete(i)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
		db.session.rollback()
	return False


handle_tag_list_methods = {
	'query': get_handle_tag_list,
	'add': add_handle_tag_list,
	'delete': del_handle_tag_list,
	'clear': clear_handle_tag_list
}


class HandleForwardServer(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	group = db.Column(db.String(80), nullable=False)
	proto = db.Column(db.String(20), nullable=False)
	ip = db.Column(db.String(80), nullable=False)
	port = db.Column(db.Integer, nullable=False)

	def __init__(self, group, proto, ip, port):
		self.group = group
		self.proto = proto
		self.ip = ip
		self.port = port


def get_handle_forward_server(data):
	return to_dict_list(HandleForwardServer.query.all())


def modify_handle_forward_server(data):
	try:
		t = HandleForwardServer.query.filter(and_(HandleForwardServer.group==data['data']['group'],HandleForwardServer.proto==data['data']['proto'],\
		HandleForwardServer.ip==data['data']['ip'],HandleForwardServer.port==data['data']['port'])).first()
		if t is None:
			t = HandleForwardServer(data['data']['group'], data['data']['proto'], data['data']['ip'], data['data']['port'])
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
		db.session.rollback()
	return False


def del_handle_forward_server(data):
	try:
		t = HandleForwardServer.query.filter(and_(HandleForwardServer.group==data['data']['group'],HandleForwardServer.proto==data['data']['proto'],\
		HandleForwardServer.ip==data['data']['ip'],HandleForwardServer.port==data['data']['port'])).first()
		if t is not None:
			db.session.delete(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
		db.session.rollback()
	return False


def clear_handle_forward_server(data):
	try:
		rules = HandleForwardServer.query.all()
		if rules is not None:
			for i in rules:
				db.session.delete(i)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
		db.session.rollback()
	return False


handle_forward_server_methods = {
	'query': get_handle_forward_server,
	'add': modify_handle_forward_server,
	'update': modify_handle_forward_server,
	'delete': del_handle_forward_server,
	'clear': clear_handle_forward_server
}



class HandleProto(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	proto = db.Column(db.String(20), nullable=False)
	action = db.Column(db.String(20), nullable=False)
	port = db.Column(db.Integer, nullable=False)
	ipv4 = db.Column(db.String(400), nullable=False)
	ipv6 = db.Column(db.String(800), nullable=False)

	def __init__(self, proto, action, port, ipv4, ipv6):
		self.proto = proto
		self.action = action
		self.port = port
		self.ipv4 = ipv4
		self.ipv6 = ipv6
	
	def get_dict(self):
		return {'proto':self.proto,'action':self.action,'port':self.port,'ipv4':json.loads(self.ipv4),'ipv6':json.loads(self.ipv6)}
	def to_dict(self):
		return {'source':'ms','id':0,'service':'handle','bt':'businessproto','sbt':'rules','op':'add','data':self.get_dict()}


def get_all_handle_proto():
	try:
		rules = HandleProto.query.all()
		if rules is not None:
			l = []
			for i in rules:
				l.append(i.to_dict())
			return l
	except Exception as e:
		logger.warning(str(e))
	return []



def get_handle_proto(data):
	try:
		rules = HandleProto.query.all()
		if rules is not None:
			l = []
			for i in rules:
				l.append(i.get_dict())
			if len(l) > 0:
				return l
	except Exception as e:
		logger.warning(str(e))
	return None


def modify_handle_proto(data):
	try:
		ipv4 = json.dumps(data['data']['ipv4'])
		ipv6 = json.dumps(data['data']['ipv6'])
		t = HandleProto.query.filter(and_(HandleProto.proto==data['data']['proto'],HandleProto.ipv4==ipv4,HandleProto.ipv6==ipv6,HandleProto.port==data['data']['port'])).first()
		if t is not None:
			t.action = data['data']['action']
			db.session.commit()
		else:
			t = HandleProto(data['data']['proto'], data['data']['action'], data['data']['port'], ipv4, ipv6)
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
		db.session.rollback()
	return False


def del_handle_proto(data):
	try:
		ipv4 = json.dumps(data['data']['ipv4'])
		ipv6 = json.dumps(data['data']['ipv6'])
		t = HandleProto.query.filter(and_(HandleProto.proto==data['data']['proto'],HandleProto.ipv4==ipv4,HandleProto.ipv6==ipv6,HandleProto.port==data['data']['port'])).first()
		if t is not None:
			db.session.delete(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
		db.session.rollback()
	return False


def clear_handle_proto(data):
	try:
		rules = HandleProto.query.all()
		if rules is not None:
			for i in rules:
				db.session.delete(i)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
		db.session.rollback()
	return False


handle_proto_methods = {
	'query': get_handle_proto,
	'add': modify_handle_proto,
	'update': modify_handle_proto,
	'delete': del_handle_proto,
	'clear': clear_handle_proto
}


class HandleCa(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	ca_cert = db.Column(db.String(2100), nullable=False)
	rsa_key = db.Column(db.String(2100), nullable=False)

	def __init__(self, ca_cert, rsa_key):
		self.ca_cert = ca_cert
		self.rsa_key = rsa_key


def get_handle_ca(data):
	return to_dict_list(HandleCa.query.all())


def add_handle_ca(data):
	try:
		t = HandleCa.query.filter(and_(HandleCa.ca_cert==data['data']['ca_cert'],HandleCa.rsa_key==data['data']['rsa_key'])).first()
		if t is None:
			t = HandleCa(data['data']['ca_cert'], data['data']['rsa_key'])
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
		db.session.rollback()
	return False


def del_handle_ca(data):
	try:
		t = HandleCa.query.filter(and_(HandleCa.ca_cert==data['data']['ca_cert'],HandleCa.rsa_key==data['data']['rsa_key'])).first()
		if t is not None:
			db.session.delete(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
		db.session.rollback()
	return False


def clear_handle_ca(data):
	try:
		rules = HandleCa.query.all()
		if rules is not None:
			for i in rules:
				db.session.delete(i)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
		db.session.rollback()
	return False


handle_ca_methods = {
	'query': get_handle_ca,
	'add': add_handle_ca,
	'delete': del_handle_ca,
	'clear': clear_handle_ca
}


class HandleXforce(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	handle = db.Column(db.String(200), nullable=False)
	rcode = db.Column(db.Integer, nullable=False)
	ttl = db.Column(db.BigInteger, nullable=False)
	timestamp = db.Column(db.BigInteger, nullable=False)
	values = db.Column(db.Text, nullable=False)

	def __init__(self, handle, rcode, ttl, timestamp, values):
		self.handle = handle
		self.rcode = rcode
		self.ttl = ttl
		self.timestamp = timestamp
		self.values = values

	def get_dict(self):
		return {'handle':self.handle,'rcode':self.rcode,'ttl':self.ttl,'timestamp':self.timestamp,'values':json.loads(self.values)}
	def to_dict(self):
		return {'source':'ms','id':0,'service':'handle','bt':'xforce','sbt':'rules','op':'add','data':self.get_dict()}


def get_all_handle_xforce():
	try:
		rules = HandleXforce.query.all()
		l = []
		for i in rules:
			l.append(i.to_dict())
		return l
	except Exception as e:
		logger.warning(str(e))
	return []



def get_handle_xforce(data):
	try:
		rules = HandleXforce.query.all()
		l = []
		for i in rules:
			l.append(i.get_dict())
		if len(l) > 0:
			return l
	except Exception as e:
		logger.warning(str(e))
	return None

		
def modify_handle_xforce(data):
	try:
		t = HandleXforce.query.filter_by(handle=data['data']['handle']).first()
		if t is not None:
			t.rcode = data['data']['rcode']
			t.ttl = data['data']['ttl']
			t.timestamp = data['data']['timestamp']
			t.values = json.dumps(data['data']['values'])
			db.session.commit()
		else:
			t = HandleXforce(data['data']['handle'], data['data']['rcode'], data['data']['ttl'], data['data']['timestamp'], json.dumps(data['data']['values']))
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
		db.session.rollback()
	return False


def del_handle_xforce(data):
	try:
		t = HandleXforce.query.filter_by(handle=data['data']['handle']).first()
		if t is not None:
			db.session.delete(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
		db.session.rollback()
	return False


def clear_handle_xforce(data):
	try:
		rules = HandleXforce.query.all()
		if rules is not None:
			for i in rules:
				db.session.delete(i)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
		db.session.rollback()
	return False


handle_xforce_methods = {
	'query': get_handle_xforce,
	'add': modify_handle_xforce,
	'update': modify_handle_xforce,
	'delete': del_handle_xforce,
	'clear': clear_handle_xforce
}


class HandleString(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	bt = db.Column(db.String(40), nullable=False)
	sbt = db.Column(db.String(40), nullable=False)
	string = db.Column(db.String(40), nullable=False)

	def __init__(self, bt, sbt, string):
		self.bt = bt
		self.sbt = sbt
		self.string = string
	def get_qtype(self):
		return {'qtype': self.string}
	def get_algo(self):
		return {'lb-algo': self.string}
	def to_dict(self):
		if self.sbt == 'blackqtype':
			return {'source':'ms','service':'handle','id':0,'bt':self.bt,'sbt':self.sbt,'op':'update','data':{'qtype':self.string}}
		elif self.sbt == 'algorithm':
			return {'source':'ms','service':'handle','id':0,'bt':self.bt,'sbt':self.sbt,'op':'update','data':{'lb-algo':self.string}}


def get_all_handle_string():
	try:
		rules = HandleString.query.all()
		l = []
		for i in rules:
			l.append(i.to_dict())
		return l
	except Exception as e:
		logger.warning(str(e))
	return []


def get_handle_string(data):
	try:
		rules = HandleString.query.filter(and_(HandleString.bt==data['bt'],HandleString.sbt==data['sbt'])).all()
		if rules is not None:
			l = []
			for i in rules:
				if data['sbt'] == 'blackqtype':
					l.append(i.get_qtype())
				elif data['sbt'] == 'algorithm':
					l.append(i.get_algo())
			if len(l) > 0:
				return l
	except Exception as e:
		logger.warning(str(e))
	return None


def get_handle_str(data):
	if data['sbt'] == 'blackqtype':
		return data['data']['qtype']
	elif data['sbt'] == 'algorithm':
		return data['data']['lb-algo']
	return ''


def modify_handle_string(data):
	try:
		data_str = get_handle_str(data)
		t = HandleString.query.filter(and_(HandleString.bt==data['bt'],HandleString.sbt==data['sbt'],HandleString.string==data_str)).first()
		if t is None:
			t = HandleString(data['bt'], data['sbt'], data_str)
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
		db.session.rollback()
	return False


def modify_loadbalance_string(data):
	try:
		data_str = get_handle_str(data)
		t = HandleString.query.filter(and_(HandleString.bt==data['bt'],HandleString.sbt==data['sbt'])).first()
		if t is None:
			t = HandleString(data['bt'], data['sbt'], data_str)
			db.session.add(t)
			db.session.commit()
		else:
			t.string = data_str
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
		db.session.rollback()
	return False


def delete_handle_string(data):
	try:
		t = HandleString.query.filter(and_(HandleString.bt==data['bt'],HandleString.sbt==data['sbt'],HandleString.string==get_handle_str(data))).first()
		if t is not None:
			db.session.delete(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
		db.session.rollback()
	return False


def clear_handle_string(data):
	try:
		rules = HandleString.query.filter(and_(HandleString.bt==data['bt'],HandleString.sbt==data['sbt'])).all()
		if rules is not None and len(rules) > 0:
			for i in rules:
				db.session.delete(i)
			db.session.commit()
		return True		
	except Exception as e:
		logger.warning(str(e))
		db.session.rollback()
	return None


loadbalance_methods = {
	'query': get_handle_string,
	'add': modify_loadbalance_string,
	'update': modify_loadbalance_string,
	'delete': delete_handle_string,
	'clear': clear_handle_string
}

handle_string_methods = {
	'query': get_handle_string,
	'add': modify_handle_string,
	'delete': delete_handle_string,
	'clear': clear_handle_string
}


class HandleDigit(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	bt = db.Column(db.String(40), nullable=False)
	sbt = db.Column(db.String(40), nullable=False)
	digit = db.Column(db.BigInteger, nullable=False)

	def __init__(self, bt, sbt, digit):
		self.bt = bt
		self.sbt = sbt
		self.digit = digit
	def get_responsecode(self):
		return {'responsecode': self.digit}
	def to_dict(self):
		if self.sbt == 'responserules':
			return {'source':'ms','id':0,'bt':self.bt,'sbt':self.sbt,'op':'update','data':{'responsecode':self.digit}}


def get_all_total_digit():
	try:
		rules = HandleDigit.query.all()
		l = []
		for i in rules:
			l.append(i.to_dict())
		return l
	except Exception as e:
		logger.warning(str(e))
	return []


def get_total_digit(data):
	try:
		rules = HandleDigit.query.filter(and_(HandleDigit.bt==data['bt'],HandleDigit.sbt==data['sbt'])).all()
		if rules is not None:
			l = []
			for i in rules:
				if data['sbt'] == 'responserules':
					l.append(i.get_responsecode())
			if len(l) > 0:
				return l
	except Exception as e:
		logger.warning(str(e))
	return None


def get_handle_num(data):
	if data['sbt'] == 'responserules':
		return data['data']['responsecode']
	return -1


def modify_total_digit(data):
	try:
		num = get_handle_num(data)
		t = HandleDigit.query.filter(and_(HandleDigit.bt==data['bt'],HandleDigit.sbt==data['sbt'],HandleDigit.digit==num)).first()
		if t is None:
			t = HandleDigit(data['bt'], data['sbt'], num)
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
		db.session.rollback()
	return False


def delete_total_digit(data):
	try:
		num = get_handle_num(data)
		t = HandleDigit.query.filter(and_(HandleDigit.bt==data['bt'],HandleDigit.sbt==data['sbt'],HandleDigit.digit==num)).first()
		if t is not None:
			db.session.delete(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
		db.session.rollback()
	return False


def clear_total_digit(data):
	try:
		rules = HandleDigit.query.filter(and_(HandleDigit.bt==data['bt'],HandleDigit.sbt==data['sbt'])).all()
		if rules is not None and len(rules) > 0:
			for i in rules:
				db.session.delete(i)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
		db.session.rollback()
	return False


selfcheck_response_methods = {
	'query': get_total_digit,
	'add': modify_total_digit,
	'update': modify_total_digit,
	'delete': delete_total_digit,
	'clear': clear_total_digit
}


class HandleStub(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	handle = db.Column(db.String(300), nullable=False)
	ttl = db.Column(db.Integer, nullable=False)
	index = db.Column(db.Integer, nullable=False)
	type = db.Column(db.String(40), nullable=False)
	data = db.Column(db.Text, nullable=False)

	def __init__(self, handle, ttl, index, type, data):
		self.handle = handle
		self.ttl = ttl
		self.index = index
		self.type = type
		self.data = data


def get_handle_stub(data):
	return to_dict_list(HandleStub.query().all())

		
def modify_handle_stub(data):
	try:
		t = HandleStub.query.filter(and_(HandleStub.handle==data['data']['handle'],HandleStub.index==data['data']['index'],HandleStub.type==data['data']['type'])).first()
		if t is not None:
			t.ttl = data['data']['ttl']
			t.data = json.dumps(data['data']['data'])
			db.session.commit()
		else:
			t = HandleStub(data['data']['handle'], data['data']['ttl'], data['data']['index'], data['data']['type'], json.dumps(data['data']['data']))
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
		db.session.rollback()
	return False


def del_handle_stub(data):
	try:
		t = HandleStub.query.filter(and_(HandleStub.handle==data['data']['handle'],HandleStub.index==data['data']['index'],HandleStub.type==data['data']['type'])).first()
		if t is not None:
			db.session.delete(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
		db.session.rollback()
	return False


def clear_handle_stub(data):
	try:
		rules = HandleStub.query.all()
		if rules is not None:
			for i in rules:
				db.session.delete(i)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
		db.session.rollback()
	return False


handle_stub_methods = {
	'query': get_handle_stub,
	'add': modify_handle_stub,
	'update': modify_handle_stub,
	'delete': del_handle_stub,
	'clear': clear_handle_stub
}


class HandleHealth(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	switch = db.Column(db.String(20), nullable=False)
	cycle = db.Column(db.Integer, nullable=False)

	def __init__(self, switch, cycle):
		self.switch = switch
		self.cycle = cycle


def get_handle_health(data):
	try:
		s = HandleHealth.query.get(1)
		if s is not None:
			return {'switch': s.switch,'cycle':s.cycle}
	except Exception as e:
		logger.warning(str(e))
	return {'switch': 'disable','cycle':1800}


def put_handle_health(data):
	try:
		s = HandleHealth.query.get(1)
		if s is not None:
			s.switch = data['data']['switch']
			s.cycle = data['data']['cycle']
			db.session.commit()
		else:
			s = HandleHealth(data['data']['switch'],data['data']['cycle'])
			db.session.add(s)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
		db.session.rollback()


handle_health_methods = {
	'query': get_handle_health,
	'add': put_handle_health,
	'update': put_handle_health,
}



def get_all_handle():
	return to_have_bt_dict_list(HandleSwitch.query.all(),'handle') + to_have_bt_dict_list(HandleIpList.query.all(),'handle') + to_have_bt_dict_list(HandleTagList.query.all(),'handle') + \
	to_have_bt_dict_list(HandleTotalThreshold.query.all(),'handle') + to_have_bt_dict_list(HandleIpThreshold.query.all(),'handle') + \
	to_have_bt_dict_list(HandleTagThreshold.query.all(),'handle') + to_no_bt_dict_list('useripwhitelist','rules',HandleIpGroup.query.all(),'handle') + \
	to_no_bt_dict_list('backend','forwardserver',HandleForwardServer.query.all(),'handle') + to_no_bt_dict_list('certificate','rules',HandleCa.query.all(),'handle') + \
	to_have_bt_dict_list(HandleString.query.all(),'handle') + to_have_bt_dict_list(HandleDigit.query.all(),'handle') +  get_all_handle_xforce() + \
	to_no_bt_dict_list('stub','rules',HandleStub.query.all(),'handle') + get_all_handle_proto()
	


def get_all_proxy_handle():
	no_switch = {'trusted','useripwhitelist','ipthreshold','srcipaccesscontrol'}
	return [i for i in to_have_bt_dict_list(HandleSwitch.query.all(),'handle') if i['bt'] not in no_switch] + to_have_bt_dict_list(HandleTotalThreshold.query.all(),'handle') + \
	to_have_bt_dict_list(HandleTagList.query.all(),'handle') + to_no_bt_dict_list('backend','forwardserver',HandleForwardServer.query.all(),'handle') + \
	to_have_bt_dict_list(HandleTagThreshold.query.all(),'handle') + to_no_bt_dict_list('certificate','rules',HandleCa.query.all(),'handle') + \
	[i for i in get_all_handle_string() if i['bt'] != 'loadbalance'] + to_have_bt_dict_list(HandleDigit.query.all(),'handle') +  get_all_handle_xforce() + get_all_handle_proto()


def get_all_xforward_handle():
	return [i for i in to_have_bt_dict_list(HandleSwitch.query.all(),'handle') if i['bt'] == 'selfcheck'] + \
	to_no_bt_dict_list('backend','forwardserver',HandleForwardServer.query.all(),'handle') + [i for i in get_all_handle_string() if i['bt'] == 'selfcheck'] + \
	to_have_bt_dict_list(HandleDigit.query.all(),'handle') +  get_all_handle_xforce() + get_all_handle_proto()


def get_all_recursion_handle():
	return to_no_bt_dict_list('healthdetect','config',HandleHealth.query.all(),'handle') + [i for i in get_all_handle_string() if i['bt'] == 'loadbalance'] + \
	[i for i in to_have_bt_dict_list(HandleSwitch.query.all(),'handle') if i['bt'] == 'trusted'] + to_no_bt_dict_list('stub','rules',HandleStub.query.all(),'handle')





