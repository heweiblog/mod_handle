#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import and_
from common.log import logger
from . import db,to_dict_list,to_no_bt_dict_list,to_have_bt_dict_list

class CreditDname(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	dname = db.Column(db.String(300), nullable=False)

	def __init__(self, dname):
		self.dname = dname


# 获取授信域名
def get_credit_dname(data):
	return to_dict_list(CreditDname.query.all())


# 添加授信域名
def add_credit_dname(data):
	try:
		p = CreditDname.query.filter_by(dname=data['data']['dname']).first()
		if p is None:
			p = CreditDname(dname=data['data']['dname'])
			db.session.add(p)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 删除授信域名
def del_credit_dname(data):
	try:
		p = CreditDname.query.filter_by(dname=data['data']['dname']).first()
		if p is not None:
			db.session.delete(p)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 清空授信域名
def clear_credit_dname(data):
	try:
		dname = CreditDname.query.all()
		for p in dname:
			db.session.delete(p)
		db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


credit_dname_methods = {
	'query': get_credit_dname,
	'add': add_credit_dname,
	'delete': del_credit_dname,
	'clear': clear_credit_dname
}


class DomainAccessControl(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	domain = db.Column(db.String(300), nullable=False)
	action = db.Column(db.String(20), nullable=False)

	def __init__(self, domain, action):
		self.domain = domain
		self.action = action


# 获取所有域名访问控制列表
def get_domain_access_control(data):
	return to_dict_list(DomainAccessControl.query.all())


# 添加/修改域名访问控制列表
def modify_domain_access_control(data):
	try:
		t = DomainAccessControl.query.filter_by(domain=data['data']['domain']).first()
		if t is not None:
			t.action = data['data']['action']
			db.session.commit()
		else:
			t = DomainAccessControl(data['data']['domain'], data['data']['action'])
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 从域名访问控制列表删除元素
def del_domain_access_control(data):
	try:
		t = DomainAccessControl.query.filter_by(domain=data['data']['domain']).first()
		if t is not None:
			db.session.delete(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 清空域名访问控制列表
def clear_domain_access_control(data):
	try:
		rules = DomainAccessControl.query.all()
		if rules is not None:
			for i in rules:
				db.session.delete(i)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


domain_access_control_methods = {
	'query': get_domain_access_control,
	'add': modify_domain_access_control,
	'update': modify_domain_access_control,
	'delete': del_domain_access_control,
	'clear': clear_domain_access_control
}


class IpDomainAccessControl(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	ip = db.Column(db.String(60), nullable=False)
	domain = db.Column(db.String(300), nullable=False)
	action = db.Column(db.String(20), nullable=False)

	def __init__(self, ip, domain, action):
		self.ip = ip
		self.domain = domain
		self.action = action


# 获取所有ip域名访问控制列表
def get_ip_domain_access_control(data):
	return to_dict_list(IpDomainAccessControl.query.all())


# 添加/修改ip域名访问控制列表
def modify_ip_domain_access_control(data):
	try:
		t = IpDomainAccessControl.query.filter(and_(IpDomainAccessControl.ip==data['data']['ip'],IpDomainAccessControl.domain==data['data']['domain'])).first()
		if t is not None:
			t.action = data['data']['action']
			db.session.commit()
		else:
			t = IpDomainAccessControl(data['data']['ip'], data['data']['domain'], data['data']['action'])
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 从ip域名访问控制列表删除元素
def del_ip_domain_access_control(data):
	try:
		t = IpDomainAccessControl.query.filter(and_(IpDomainAccessControl.ip==data['data']['ip'],IpDomainAccessControl.domain==data['data']['domain'])).first()
		if t is not None:
			db.session.delete(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 清空ip域名访问控制列表
def clear_ip_domain_access_control(data):
	try:
		rules = IpDomainAccessControl.query.all()
		if rules is not None:
			for i in rules:
				db.session.delete(i)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


ip_domain_access_control_methods = {
	'query': get_ip_domain_access_control,
	'add': modify_ip_domain_access_control,
	'update': modify_ip_domain_access_control,
	'delete': del_ip_domain_access_control,
	'clear': clear_ip_domain_access_control
}


class DomainQtypeAccessControl(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	qtype = db.Column(db.String(20), nullable=False)
	domain = db.Column(db.String(300), nullable=False)
	action = db.Column(db.String(20), nullable=False)

	def __init__(self, qtype, domain, action):
		self.qtype = qtype
		self.domain = domain
		self.action = action


# 获取所有qtype域名访问控制列表
def get_domain_qtype_access_control(data):
	return to_dict_list(DomainQtypeAccessControl.query.all())


# 添加/修改qtype域名访问控制列表
def modify_domain_qtype_access_control(data):
	try:
		t = DomainQtypeAccessControl.query.filter(and_(DomainQtypeAccessControl.qtype==data['data']['qtype'],DomainQtypeAccessControl.domain==data['data']['domain'])).first()
		if t is not None:
			t.action = data['data']['action']
			db.session.commit()
		else:
			t = DomainQtypeAccessControl(data['data']['qtype'], data['data']['domain'], data['data']['action'])
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 从域名访问控制列表删除元素
def del_domain_qtype_access_control(data):
	try:
		t = DomainQtypeAccessControl.query.filter(and_(DomainQtypeAccessControl.qtype==data['data']['qtype'],DomainQtypeAccessControl.domain==data['data']['domain'])).first()
		if t is not None:
			db.session.delete(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 清空域名访问控制列表
def clear_domain_qtype_access_control(data):
	try:
		rules = DomainQtypeAccessControl.query.all()
		if rules is not None:
			for i in rules:
				db.session.delete(i)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


domain_qtype_access_control_methods = {
	'query': get_domain_qtype_access_control,
	'add': modify_domain_qtype_access_control,
	'update': modify_domain_qtype_access_control,
	'delete': del_domain_qtype_access_control,
	'clear': clear_domain_qtype_access_control
}


class QtypeAccessControl(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	qtype = db.Column(db.String(20), nullable=False)
	action = db.Column(db.String(20), nullable=False)

	def __init__(self, qtype, action):
		self.qtype = qtype
		self.action = action


# 获取所有请求类型访问控制列表
def get_qtype_access_control(data):
	return to_dict_list(QtypeAccessControl.query.all())


# 添加/修改请求类型访问控制列表
def modify_qtype_access_control(data):
	try:
		t = QtypeAccessControl.query.filter_by(qtype=data['data']['qtype']).first()
		if t is not None:
			t.action = data['data']['action']
			db.session.commit()
		else:
			t = QtypeAccessControl(data['data']['qtype'], data['data']['action'])
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 从请求类型访问控制列表删除元素
def del_qtype_access_control(data):
	try:
		t = QtypeAccessControl.query.filter_by(qtype=data['data']['qtype']).first()
		if t is not None:
			db.session.delete(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 清空请求类型访问控制列表
def clear_qtype_access_control(data):
	try:
		rules = QtypeAccessControl.query.all()
		if rules is not None:
			for i in rules:
				db.session.delete(i)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


qtype_access_control_methods = {
	'query': get_qtype_access_control,
	'add': modify_qtype_access_control,
	'update': modify_qtype_access_control,
	'delete': del_qtype_access_control,
	'clear': clear_qtype_access_control
}


class GrayDomainAccessControl(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	domain = db.Column(db.String(300), nullable=False)
	action = db.Column(db.String(20), nullable=False)

	def __init__(self, domain, action):
		self.domain = domain
		self.action = action


# 获取所有灰色域名访问控制列表
def get_gray_domain_access_control(data):
	return to_dict_list(GrayDomainAccessControl.query.all())


# 添加/修改灰色域名访问控制列表
def modify_gray_domain_access_control(data):
	try:
		t = GrayDomainAccessControl.query.filter_by(domain=data['data']['domain']).first()
		if t is not None:
			t.action = data['data']['action']
			db.session.commit()
		else:
			t = GrayDomainAccessControl(data['data']['domain'], data['data']['action'])
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 从灰色域名访问控制列表删除元素
def del_gray_domain_access_control(data):
	try:
		t = GrayDomainAccessControl.query.filter_by(domain=data['data']['domain']).first()
		if t is not None:
			db.session.delete(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 清空灰色域名访问控制列表
def clear_gray_domain_access_control(data):
	try:
		rules = GrayDomainAccessControl.query.all()
		if rules is not None:
			for i in rules:
				db.session.delete(i)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


gray_domain_access_control_methods = {
	'query': get_gray_domain_access_control,
	'add': modify_gray_domain_access_control,
	'update': modify_gray_domain_access_control,
	'delete': del_gray_domain_access_control,
	'clear': clear_gray_domain_access_control
}


class ImportDnameProtect(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	qtype = db.Column(db.String(20), nullable=False)
	domain = db.Column(db.String(300), nullable=False)
	action = db.Column(db.String(20), nullable=False)
	answer = db.Column(db.String(300), nullable=False)
	backup = db.Column(db.String(300))

	def __init__(self, qtype, domain, action, answer, backup):
		self.qtype = qtype
		self.domain = domain
		self.action = action
		self.answer = answer
		self.backup = backup


# 获取所有重点域名保障列表
def get_import_dname(data):
	return to_dict_list(ImportDnameProtect.query.all())


# 添加/修改重点域名保障
def modify_import_dname(data):
	try:
		t = ImportDnameProtect.query.filter(and_(ImportDnameProtect.qtype==data['data']['qtype'],ImportDnameProtect.domain==data['data']['domain'])).first()
		if t is not None:
			t.answer = data['data']['answer']
			t.backup = data['data']['backup']
			t.action = data['data']['action']
			db.session.commit()
		else:
			t = ImportDnameProtect(data['data']['qtype'], data['data']['domain'], data['data']['action'], data['data']['answer'], data['data']['backup'])
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 从重点域名保障列表删除元素
def del_import_dname(data):
	try:
		t = ImportDnameProtect.query.filter(and_(ImportDnameProtect.qtype==data['data']['qtype'],ImportDnameProtect.domain==data['data']['domain'])).first()
		if t is not None:
			db.session.delete(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 清空重点域名保障列表
def clear_import_dname(data):
	try:
		rules = ImportDnameProtect.query.all()
		if rules is not None:
			for i in rules:
				db.session.delete(i)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


import_dname_methods = {
	'query': get_import_dname,
	'add': modify_import_dname,
	'update': modify_import_dname,
	'delete': del_import_dname,
	'clear': clear_import_dname
}


class DomainList(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	bt = db.Column(db.String(40), nullable=False)
	sbt = db.Column(db.String(40), nullable=False)
	domain = db.Column(db.String(300), nullable=False)

	def __init__(self, bt, sbt, domain):
		self.bt = bt
		self.sbt = sbt
		self.domain = domain


# 获取域名列表
def get_domain_list(data):
	return to_dict_list(DomainList.query.filter(and_(DomainList.bt==data['bt'],DomainList.sbt==data['sbt'])).all())


# 添加域名列表
def add_domain_list(data):
	try:
		t = DomainList.query.filter(and_(DomainList.bt==data['bt'],DomainList.sbt==data['sbt'],DomainList.domain==data['data']['domain'])).first()
		if t is None:
			t = DomainList(data['bt'], data['sbt'], data['data']['domain'])
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 删除域名列表
def del_domain_list(data):
	try:
		t = DomainList.query.filter(and_(DomainList.bt==data['bt'],DomainList.sbt==data['sbt'],DomainList.domain==data['data']['domain'])).first()
		if t is not None:
			db.session.delete(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 清空域名列表
def clear_domain_list(data):
	try:
		rules = DomainList.query.filter(and_(DomainList.bt==data['bt'],DomainList.sbt==data['sbt'])).all()
		if rules is not None:
			for i in rules:
				db.session.delete(i)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


domain_list_methods = {
	'query': get_domain_list,
	'add': add_domain_list,
	'delete': del_domain_list,
	'clear': clear_domain_list
}

def get_all_fpga_domain():
	return to_have_bt_dict_list(DomainList.query.all()) + to_no_bt_dict_list('creditdname','dnamelist',CreditDname.query.all()) + \
	to_no_bt_dict_list('domainaccesscontrol','rules',DomainAccessControl.query.all()) + to_no_bt_dict_list('ipdomainaccesscontrol','rules',IpDomainAccessControl.query.all()) + \
	to_no_bt_dict_list('domainqtypeaccesscontrol','rules',DomainQtypeAccessControl.query.all()) + to_no_bt_dict_list('qtypeaccesscontrol','rules',QtypeAccessControl.query.all()) + \
	to_no_bt_dict_list('graydomainaccesscontrol','rules',GrayDomainAccessControl.query.all())


def get_all_domain():
	return to_have_bt_dict_list(DomainList.query.all()) + to_no_bt_dict_list('creditdname','dnamelist',CreditDname.query.all()) + \
	to_no_bt_dict_list('domainaccesscontrol','rules',DomainAccessControl.query.all()) + to_no_bt_dict_list('ipdomainaccesscontrol','rules',IpDomainAccessControl.query.all()) + \
	to_no_bt_dict_list('domainqtypeaccesscontrol','rules',DomainQtypeAccessControl.query.all()) + to_no_bt_dict_list('qtypeaccesscontrol','rules',QtypeAccessControl.query.all()) + \
	to_no_bt_dict_list('graydomainaccesscontrol','rules',GrayDomainAccessControl.query.all()) + to_no_bt_dict_list('importdnameprotect','rules',ImportDnameProtect.query.all())


