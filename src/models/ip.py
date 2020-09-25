#!/usr/bin/python
# -*- coding: utf-8 -*-

from common.log import logger
from sqlalchemy import and_
from . import db,to_dict_list,to_no_bt_dict_list,to_have_bt_dict_list


class IpList(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	bt = db.Column(db.String(40), nullable=False)
	sbt = db.Column(db.String(40), nullable=False)
	ip = db.Column(db.String(60), nullable=False)

	def __init__(self, bt, sbt, ip):
		self.bt = bt
		self.sbt = sbt
		self.ip = ip


# 获取ip列表
def get_ip_list(data):
	return to_dict_list(IpList.query.filter(and_(IpList.bt==data['bt'],IpList.sbt==data['sbt'])).all())


def ip_list_exist(data):
	try:
		t = IpList.query.filter(and_(IpList.bt==data['bt'],IpList.sbt==data['sbt'],IpList.ip==data['data']['ip'])).first()
		if t is not None:
			return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 添加ip列表
def add_ip_list(data):
	try:
		t = IpList.query.filter(and_(IpList.bt==data['bt'],IpList.sbt==data['sbt'],IpList.ip==data['data']['ip'])).first()
		if t is None:
			t = IpList(data['bt'], data['sbt'], data['data']['ip'])
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 添加 accesscontrolanswerip ip列表
def update_ip_list(data):
	try:
		t = IpList.query.filter(and_(IpList.bt==data['bt'],IpList.sbt==data['sbt'])).first()
		if t is None:
			t = IpList(data['bt'], data['sbt'], data['data']['ip'])
			db.session.add(t)
			db.session.commit()
		else:
			t.ip = data['data']['ip']
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False



# 删除ip列表
def del_ip_list(data):
	try:
		t = IpList.query.filter(and_(IpList.bt==data['bt'],IpList.sbt==data['sbt'],IpList.ip==data['data']['ip'])).first()
		if t is not None:
			db.session.delete(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 清空ip列表
def clear_ip_list(data):
	try:
		rules = IpList.query.filter(and_(IpList.bt==data['bt'],IpList.sbt==data['sbt'])).all()
		if rules is not None:
			for i in rules:
				db.session.delete(i)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


access_ip_methods = {
	'query': get_ip_list,
	'update': update_ip_list,
	'delete': del_ip_list,
}


ip_list_methods = {
	'query': get_ip_list,
	'add': add_ip_list,
	'update': add_ip_list,
	'delete': del_ip_list,
	'clear': clear_ip_list
}


def get_rootcopy_ip_list(data):
	try:
		rules = IpList.query.filter(and_(IpList.bt==data['bt'],IpList.sbt==data['sbt'])).all()
		if rules is not None and len(rules) > 0:
			l = []
			for i in rules:
				l.append(i.ip)
			return l
	except Exception as e:
		logger.warning(str(e))
	return None


def add_rootcopy_ip_list(data):
	try:
		for i in data['data']['ip']:
			t = IpList.query.filter(and_(IpList.bt==data['bt'],IpList.sbt==data['sbt'],IpList.ip==i)).first()
			if t is None:
				t = IpList(data['bt'], data['sbt'], i)
				db.session.add(t)
				db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False
	

def delete_rootcopy_ip_list(data):
	try:
		for i in data['data']['ip']:
			t = IpList.query.filter(and_(IpList.bt==data['bt'],IpList.sbt==data['sbt'],IpList.ip==i)).first()
			if t is not None:
				db.session.delete(t)
		db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


rootcopy_methods = {
	'query': get_rootcopy_ip_list,
	'add': add_rootcopy_ip_list,
	'delete': delete_rootcopy_ip_list,
	'clear': clear_ip_list
}

class SrcIpAccessControl(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	ip = db.Column(db.String(60), nullable=False)
	action = db.Column(db.String(20), nullable=False)

	def __init__(self, ip, action):
		self.ip = ip
		self.action = action


# 获取所有源ip访问控制列表
def get_src_ip_control(data):
	return to_dict_list(SrcIpAccessControl.query.all())


def src_ip_control_exist(data):
	try:
		t = SrcIpAccessControl.query.filter_by(ip=data['data']['ip']).first()
		if t is not None:
			return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 添加/修改源ip访问控制列表
def modify_src_ip_control(data):
	try:
		t = SrcIpAccessControl.query.filter_by(ip=data['data']['ip']).first()
		if t is not None:
			t.action = data['data']['action']
			db.session.commit()
		else:
			t = SrcIpAccessControl(data['data']['ip'], data['data']['action'])
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 从源ip访问控制列表删除元素
def del_src_ip_control(data):
	try:
		t = SrcIpAccessControl.query.filter_by(ip=data['data']['ip']).first()
		if t is not None:
			db.session.delete(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 清空源ip访问控制列表
def clear_src_ip_control(data):
	try:
		rules = SrcIpAccessControl.query.all()
		if rules is not None:
			for i in rules:
				db.session.delete(i)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


src_ip_access_control_methods = {
	'query': get_src_ip_control,
	'add': modify_src_ip_control,
	'update': modify_src_ip_control,
	'delete': del_src_ip_control,
	'clear': clear_src_ip_control
}


class IpQtypeAccessControl(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	qtype = db.Column(db.String(20), nullable=False)
	ip = db.Column(db.String(60), nullable=False)
	action = db.Column(db.String(20), nullable=False)

	def __init__(self, qtype, ip, action):
		self.qtype = qtype
		self.ip = ip
		self.action = action


# 获取所有ip qtype访问控制列表
def get_ip_qtype_access_control(data):
	return to_dict_list(IpQtypeAccessControl.query.all())


def ip_qtype_access_control_exist(data):
	try:
		t = IpQtypeAccessControl.query.filter(and_(IpQtypeAccessControl.qtype==data['data']['qtype'],IpQtypeAccessControl.ip==data['data']['ip'])).first()
		if t is not None:
			return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 添加/修改ip qtype访问控制列表
def modify_ip_qtype_access_control(data):
	try:
		t = IpQtypeAccessControl.query.filter(and_(IpQtypeAccessControl.qtype==data['data']['qtype'],IpQtypeAccessControl.ip==data['data']['ip'])).first()
		if t is not None:
			t.action = data['data']['action']
			db.session.commit()
		else:
			t = IpQtypeAccessControl(data['data']['qtype'], data['data']['ip'], data['data']['action'])
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 从ip qtype访问控制列表删除元素
def del_ip_qtype_access_control(data):
	try:
		t = IpQtypeAccessControl.query.filter(and_(IpQtypeAccessControl.qtype==data['data']['qtype'],IpQtypeAccessControl.ip==data['data']['ip'])).first()
		if t is not None:
			db.session.delete(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 清空域名访问控制列表
def clear_ip_qtype_access_control(data):
	try:
		rules = IpQtypeAccessControl.query.all()
		if rules is not None:
			for i in rules:
				db.session.delete(i)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


ip_qtype_access_control_methods = {
	'query': get_ip_qtype_access_control,
	'add': modify_ip_qtype_access_control,
	'update': modify_ip_qtype_access_control,
	'delete': del_ip_qtype_access_control,
	'clear': clear_ip_qtype_access_control
}


class GrayDomainRedirectIp(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	ip = db.Column(db.String(60), nullable=False)
	weight = db.Column(db.Integer, nullable=False)

	def __init__(self, ip, weight):
		self.ip = ip
		self.weight = weight


# 获取所有的灰色域名访问控制重定向IP
def get_ip_weight(data):
	return to_dict_list(GrayDomainRedirectIp.query.all())


def ip_weight_exist(data):
	try:
		t = GrayDomainRedirectIp.query.filter_by(ip=data['data']['ip']).first()
		if t is not None:
			return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 添加/修改灰色域名访问控制重定向IP
def modify_ip_weight(data):
	try:
		t = GrayDomainRedirectIp.query.filter_by(ip=data['data']['ip']).first()
		if t is not None:
			t.weight = data['data']['weight']
			db.session.commit()
		else:
			t = GrayDomainRedirectIp(data['data']['ip'], data['data']['weight'])
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 删除灰色域名访问控制重定向IP
def del_ip_weight(data):
	try:
		t = GrayDomainRedirectIp.query.filter_by(ip=data['data']['ip']).first()
		if t is not None:
			db.session.delete(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 清空所有的灰色域名访问控制重定向IP
def clear_ip_weight(data):
	try:
		rules = GrayDomainRedirectIp.query.all()
		if rules is not None:
			for i in rules:
				db.session.delete(i)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


ip_weight_methods = {
	'query': get_ip_weight,
	'add': modify_ip_weight,
	'update': modify_ip_weight,
	'delete': del_ip_weight,
	'clear': clear_ip_weight
}


def get_all_ip():
	return to_have_bt_dict_list(IpList.query.all()) + to_no_bt_dict_list('srcipaccesscontrol','rules',SrcIpAccessControl.query.all()) + \
	to_no_bt_dict_list('ipqtypeaccesscontrol','rules',IpQtypeAccessControl.query.all()) + to_no_bt_dict_list('graydomainaccesscontrol','redirectip',GrayDomainRedirectIp.query.all())



