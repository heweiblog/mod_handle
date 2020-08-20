#!/usr/bin/python
# -*- coding: utf-8 -*-

from common.log import logger
from sqlalchemy import and_
from . import db


def to_acl_dict_list(rules):
	try:
		l = []
		for i in rules:
			d = {c.name: getattr(i, c.name) for c in i.__table__.columns}
			del d['id']
			if i.__tablename__ == SrcIpList.__tablename__:
				d['ipGroup'] = d['group']
				del d['group']
			elif i.__tablename__ == DstIpList.__tablename__:
				d['groupName'] = d['group']
				del d['group']
			elif i.__tablename__ == AclDomainList.__tablename__:
				d['domainGroup'] = d['group']
				del d['group']
			l.append(d)
		if len(l) > 0:
			return l
	except Exception as e:
		logger.warning(str(e))
	return []


class SrcIpList(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	group = db.Column(db.String(80), nullable=False)
	ip = db.Column(db.String(60), nullable=False)

	def __init__(self, group, ip):
		self.group = group
		self.ip = ip


# 判断源ip组是否存在
def src_ip_group_exist(name):
	try:
		rules = SrcIpList.query.filter_by(group=name).first()
		if rules is not None:
			return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 根据group_name获取数量
def get_acl_src_ip_group_num(group_name):
	try:
		rules = SrcIpList.query.filter_by(group=group_name).all()
		if rules is not None:
			return len(rules)
	except Exception as e:
		logger.warning(str(e))
	return 0


# 获取所有的src ip list
def get_src_ip_list(data):
	l = to_acl_dict_list(SrcIpList.query.all())
	if len(l) == 0:
		return None
	return l


# 添加 src ip list
def add_src_ip_list(data):
	try:
		t = SrcIpList.query.filter(and_(SrcIpList.group==data['data']['ipgroup'],SrcIpList.ip==data['data']['ip'])).first()
		if t is None:
			t = SrcIpList(data['data']['ipgroup'], data['data']['ip'])
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 删除src ip list 
def del_src_ip_list(data):
	try:
		if 'ip' in data['data']:
			t = SrcIpList.query.filter(and_(SrcIpList.group==data['data']['ipgroup'],SrcIpList.ip==data['data']['ip'])).first()
			if t is not None:
				db.session.delete(t)
				db.session.commit()
		else:
			rules = SrcIpList.query.filter_by(group=data['data']['ipgroup']).all()
			if rules is not None:
				for i in rules:
					db.session.delete(i)
				db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 清空所有的src ip list
def clear_src_ip_list(data):
	try:
		rules = SrcIpList.query.all()
		if rules is not None:
			for i in rules:
				db.session.delete(i)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


src_ip_list_methods = {
	'query': get_src_ip_list,
	'add': add_src_ip_list,
	'delete': del_src_ip_list,
	'clear': clear_src_ip_list
}


class DstIpList(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	group = db.Column(db.String(80), nullable=False)
	ip = db.Column(db.String(60), nullable=False)

	def __init__(self, group, ip):
		self.group = group
		self.ip = ip


# 判断目的ip组是否存在
def dst_ip_group_exist(name):
	try:
		rules = DstIpList.query.filter_by(group=name).first()
		if rules is not None:
			return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 根据group_name获取数量
def get_acl_dst_ip_group_num(group_name):
	try:
		rules = DstIpList.query.filter_by(group=group_name).all()
		if rules is not None:
			return len(rules)
	except Exception as e:
		logger.warning(str(e))
	return 0


# 获取所有的dst ip list
def get_dst_ip_list(data):
	l = to_acl_dict_list(DstIpList.query.all())
	if len(l) == 0:
		return None
	return l


# 添加 dst ip list
def add_dst_ip_list(data):
	try:
		t = DstIpList.query.filter(and_(DstIpList.group==data['data']['groupname'],DstIpList.ip==data['data']['ip'])).first()
		if t is None:
			t = DstIpList(data['data']['groupname'], data['data']['ip'])
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 删除dst ip list 
def del_dst_ip_list(data):
	try:
		if 'ip' in data['data']:
			t = DstIpList.query.filter(and_(DstIpList.group==data['data']['groupname'],DstIpList.ip==data['data']['ip'])).first()
			if t is not None:
				db.session.delete(t)
				db.session.commit()
		else:
			rules = DstIpList.query.filter_by(group=data['data']['groupname']).all()
			if rules is not None:
				for i in rules:
					db.session.delete(i)
				db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 清空所有的dst ip list
def clear_dst_ip_list(data):
	try:
		rules = DstIpList.query.all()
		if rules is not None:
			for i in rules:
				db.session.delete(i)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


dst_ip_list_methods = {
	'query': get_dst_ip_list,
	'add': add_dst_ip_list,
	'delete': del_dst_ip_list,
	'clear': clear_dst_ip_list
}


class AclDomainList(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	group = db.Column(db.String(80), nullable=False)
	domain = db.Column(db.String(300), nullable=False)

	def __init__(self, group, domain):
		self.group = group
		self.domain = domain


# 判断domain组是否存在
def domain_group_exist(name):
	try:
		rules = AclDomainList.query.filter_by(group=name).first()
		if rules is not None:
			return True
	except Exception as e:
		logger.warning(str(e))
	return False


def get_acl_domain_group_num(group_name):
	try:
		rules = AclDomainList.query.filter_by(group=group_name).all()
		if rules is not None:
			return len(rules)
	except Exception as e:
		logger.warning(str(e))
	return 0


# 获取所有的acl domain list
def get_acl_domain_list(data):
	l = to_acl_dict_list(AclDomainList.query.all())
	if len(l) == 0:
		return None
	return l


# 添加 acl domain list
def add_acl_domain_list(data):
	try:
		t = AclDomainList.query.filter(and_(AclDomainList.group==data['data']['domaingroup'],AclDomainList.domain==data['data']['domain'])).first()
		if t is None:
			t = AclDomainList(data['data']['domaingroup'], data['data']['domain'])
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 删除acl domain list 
def del_acl_domain_list(data):
	try:
		if 'ip' in data['data']:
			t = AclDomainList.query.filter(and_(AclDomainList.group==data['data']['domaingroup'],AclDomainList.domain==data['data']['domain'])).first()
			if t is not None:
				db.session.delete(t)
				db.session.commit()
		else:
			rules = AclDomainList.query.filter_by(group=data['data']['domaingroup']).all()
			if rules is not None:
				for i in rules:
					db.session.delete(i)
				db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 清空所有的acl domain list
def clear_acl_domain_list(data):
	try:
		rules = AclDomainList.query.all()
		if rules is not None:
			for i in rules:
				db.session.delete(i)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


acl_domain_list_methods = {
	'query': get_acl_domain_list,
	'add': add_acl_domain_list,
	'delete': del_acl_domain_list,
	'clear': clear_acl_domain_list
}


def get_all_acl():
	l = []
	src = to_acl_dict_list(SrcIpList.query.all())
	for i in src:
		l.append({'source':'ms','id':0,'bt':'acl','sbt':'iplist','op':'add','data':i})
	dst = to_acl_dict_list(DstIpList.query.all())
	for i in dst:
		l.append({'source':'ms','id':0,'bt':'acl','sbt':'dstiplist','op':'add','data':i})
	dom = to_acl_dict_list(AclDomainList.query.all())
	for i in dom:
		l.append({'source':'ms','id':0,'bt':'acl','sbt':'domainlist','op':'add','data':i})
	return l

