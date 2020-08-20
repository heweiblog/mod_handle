#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from common.log import logger
from sqlalchemy import and_
from . import db,to_dict_list


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
	try:
		rules = HandleTotalThreshold.query.all()
		l = []
		for i in rules:
			l.append(i.to_dict())
		return l
	except Exception as e:
		logger.warning(str(e))
	return []


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
	handle = db.Column(db.String(300), nullable=False)
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
	handle = db.Column(db.String(300), nullable=False)

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
		t = HandleForwardServer.query.filter_by(group=data['data']['group']).first()
		if t is not None:
			t.ip = data['data']['ip']
			t.port = data['data']['port']
			t.proto = data['data']['proto']
			db.session.commit()
		else:
			t = HandleForwardServer(data['data']['group'], data['data']['proto'], data['data']['ip'], data['data']['port'])
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


def del_handle_forward_server(data):
	try:
		t = HandleForwardServer.query.filter_by(group=data['data']['group']).first()
		if t is not None:
			db.session.delete(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
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
	ipv4 = db.Column(db.String(80), nullable=False)
	ipv6 = db.Column(db.String(80), nullable=False)

	def __init__(self, proto, action, port, ipv4, ipv6):
		self.proto = proto
		self.action = action
		self.port = port
		self.ipv4 = ipv4
		self.ipv6 = ipv6


def get_handle_proto(data):
	return to_dict_list(HandleProto.query.all())


def modify_handle_proto(data):
	try:
		t = HandleProto.query.filter_by(action=data['data']['proto']).first()
		if t is not None:
			t.ipv4 = data['data']['ipv4']
			t.ipv6 = data['data']['ipv6']
			t.port = data['data']['port']
			t.proto = data['data']['action']
			db.session.commit()
		else:
			t = HandleProto(data['data']['proto'], data['data']['action'], data['data']['port'], data['data']['ipv4'], data['data']['ipv6'])
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


def del_handle_proto(data):
	try:
		t = HandleProto.query.filter_by(action=data['data']['proto']).first()
		if t is not None:
			db.session.delete(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
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
	ca_cert = db.Column(db.String(4000), nullable=False)
	rsa_key = db.Column(db.String(4000), nullable=False)

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
	return False


handle_ca_methods = {
	'query': get_handle_ca,
	'add': add_handle_ca,
	'delete': del_handle_ca,
	'clear': clear_handle_ca
}


class HandleXforce(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	handle = db.Column(db.String(300), nullable=False)
	ttl = db.Column(db.Integer, nullable=False)
	index = db.Column(db.Integer, nullable=False)
	type = db.Column(db.String(40), nullable=False)
	data = db.Column(db.String(400), nullable=False)

	def __init__(self, handle, ttl, index, type, data):
		self.handle = handle
		self.ttl = ttl
		self.index = index
		self.type = type
		self.data = data
	
	def get_dict(self):
		return {'handle':self.handle, 'ttl':self.ttl, 'index':self.index, 'type':self.type, 'data':json.loads(self.data)}


def get_handle_xforce(data):
	try:
		rules = HandleXforce.query.all()
		l = []
		if rules is not None:
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
			t.ttl = data['data']['ttl']
			t.index = data['data']['index']
			t.type = data['data']['type']
			t.data = json.dumps(data['data']['data'])
			db.session.commit()
		else:
			t = HandleXforce(data['data']['handle'], data['data']['ttl'], data['data']['index'], data['data']['type'], json.dumps(data['data']['data']))
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


def del_handle_xforce(data):
	try:
		#t = HandleXforce.query.filter(and_(HandleXforce.handle==data['data']['handle'],HandleXforce.index==data['data']['index'],HandleXforce.type==data['data']['type'])).first()
		t = HandleXforce.query.filter_by(handle=data['data']['handle']).first()
		if t is not None:
			db.session.delete(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
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
	return False


handle_xforce_methods = {
	'query': get_handle_xforce,
	'add': modify_handle_xforce,
	'update': modify_handle_xforce,
	'delete': del_handle_xforce,
	'clear': clear_handle_xforce
}


