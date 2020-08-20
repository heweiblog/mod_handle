#!/usr/bin/python
# -*- coding: utf-8 -*-

from common.pub import DEFAULTGROUP
from common.log import logger
from sqlalchemy import and_
from . import db,to_dict_list,to_no_bt_dict_list


def to_dts_dict_list(rules):
	try:
		l = []
		for i in rules:
			d = {c.name: getattr(i, c.name) for c in i.__table__.columns}
			d['groupName'] = d['group']
			del d['group']
			del d['id']
			l.append(d)
		if len(l) > 0:
			return l
	except Exception as e:
		logger.warning(str(e))
	return []


class DtsSrcIpGroup(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	group = db.Column(db.String(80), nullable=False)
	ip = db.Column(db.String(80), nullable=False)

	def __init__(self, group, ip):
		self.group = group
		self.ip = ip


def dts_src_ip_group_exist(group_name):
	try:
		if DtsSrcIpGroup.query.filter_by(group=group_name).first() is not None:
			return True	
	except Exception as e:
		logger.warning(str(e))
	return False


# 获取所有的dts src ip group
def get_dts_src_ip_group(data):
	l = to_dts_dict_list(DtsSrcIpGroup.query.all())
	if len(l) == 0:
		return None
	return l


# 添加 dts src ip group
def add_dts_src_ip_group(data):
	try:
		t = DtsSrcIpGroup.query.filter(and_(DtsSrcIpGroup.group==data['data']['groupname'],DtsSrcIpGroup.ip==data['data']['ip'])).first()
		if t is None:
			t = DtsSrcIpGroup(data['data']['groupname'], data['data']['ip'])
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 删除dts src ip group 
def del_dts_src_ip_group(data):
	try:
		if 'ip' in data['data']:
			t = DtsSrcIpGroup.query.filter(and_(DtsSrcIpGroup.group==data['data']['groupname'],DtsSrcIpGroup.ip==data['data']['ip'])).first()
			if t is not None:
				db.session.delete(t)
				db.session.commit()
		else:
			rules = DtsSrcIpGroup.query.filter_by(group=data['data']['groupname']).all()
			if rules is not None:
				for i in rules:
					db.session.delete(i)
				db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 清空所有的dts src ip group
def clear_dts_src_ip_group(data):
	try:
		rules = DtsSrcIpGroup.query.all()
		if rules is not None:
			for i in rules:
				db.session.delete(i)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


dts_src_ip_group_methods = {
	'query': get_dts_src_ip_group,
	'add': add_dts_src_ip_group,
	'delete': del_dts_src_ip_group,
	'clear': clear_dts_src_ip_group
}


class DtsDstIpGroup(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	group = db.Column(db.String(80), nullable=False)
	ip = db.Column(db.String(80), nullable=False)

	def __init__(self, group, ip):
		self.group = group
		self.ip = ip


def dts_dst_ip_group_exist(group_name):
	try:
		if DtsDstIpGroup.query.filter_by(group=group_name).first() is not None:
			return True	
	except Exception as e:
		logger.warning(str(e))
	return False


# 获取所有的dts dst ip group
def get_dts_dst_ip_group(data):
	l = to_dts_dict_list(DtsDstIpGroup.query.all())
	if len(l) == 0:
		return None
	return l


# 添加 dts dst ip group
def add_dts_dst_ip_group(data):
	try:
		t = DtsDstIpGroup.query.filter(and_(DtsDstIpGroup.group==data['data']['groupname'],DtsDstIpGroup.ip==data['data']['ip'])).first()
		if t is None:
			t = DtsDstIpGroup(data['data']['groupname'], data['data']['ip'])
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 删除dts dst ip group 
def del_dts_dst_ip_group(data):
	try:
		if 'ip' in data['data']:
			t = DtsDstIpGroup.query.filter(and_(DtsDstIpGroup.group==data['data']['groupname'],DtsDstIpGroup.ip==data['data']['ip'])).first()
			if t is not None:
				db.session.delete(t)
				db.session.commit()
		else:
			rules = DtsDstIpGroup.query.filter_by(group=data['data']['groupname']).all()
			if rules is not None:
				for i in rules:
					db.session.delete(i)
				db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 清空所有的dts dst ip group
def clear_dts_dst_ip_group(data):
	try:
		rules = DtsDstIpGroup.query.all()
		if rules is not None:
			for i in rules:
				db.session.delete(i)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


dts_dst_ip_group_methods = {
	'query': get_dts_dst_ip_group,
	'add': add_dts_dst_ip_group,
	'delete': del_dts_dst_ip_group,
	'clear': clear_dts_dst_ip_group
}


class DtsDomainGroup(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	group = db.Column(db.String(80), nullable=False)
	domain = db.Column(db.String(300), nullable=False)

	def __init__(self, group, domain):
		self.group = group
		self.domain = domain


def dts_domain_group_exist(group_name):
	try:
		if DtsDomainGroup.query.filter_by(group=group_name).first() is not None:
			return True	
	except Exception as e:
		logger.warning(str(e))
	return False


# 获取所有的dts domain group
def get_dts_domain_group(data):
	l = to_dts_dict_list(DtsDomainGroup.query.all())
	if len(l) == 0:
		return None
	return l


# 添加 dts domain group
def add_dts_domain_group(data):
	try:
		t = DtsDomainGroup.query.filter(and_(DtsDomainGroup.group==data['data']['groupname'],DtsDomainGroup.domain==data['data']['domain'])).first()
		if t is None:
			t = DtsDomainGroup(data['data']['groupname'], data['data']['domain'])
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 删除dts domain group 
def del_dts_domain_group(data):
	try:
		if 'ip' in data['data']:
			t = DtsDomainGroup.query.filter(and_(DtsDomainGroup.group==data['data']['groupname'],DtsDomainGroup.domain==data['data']['domain'])).first()
			if t is not None:
				db.session.delete(t)
				db.session.commit()
		else:
			rules = DtsDomainGroup.query.filter_by(group=data['data']['groupname']).all()
			if rules is not None:
				for i in rules:
					db.session.delete(i)
				db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 清空所有的dts domain group
def clear_dts_domain_group(data):
	try:
		rules = DtsDomainGroup.query.all()
		if rules is not None:
			for i in rules:
				db.session.delete(i)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


dts_domain_group_methods = {
	'query': get_dts_domain_group,
	'add': add_dts_domain_group,
	'delete': del_dts_domain_group,
	'clear': clear_dts_domain_group
}


class DtsForwardGroup(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	ip = db.Column(db.String(60), nullable=False)
	serverGroup = db.Column(db.String(80), nullable=False)
	weight = db.Column(db.Integer, nullable=False)

	def __init__(self, ip, serverGroup, weight):
		self.ip = ip
		self.serverGroup = serverGroup
		self.weight = weight


# 获取所有的dts_forward_group
def get_dts_forward_group(data):
	return to_dict_list(DtsForwardGroup.query.all())


# 添加/修改dts_forward_group
def modify_dts_forward_group(data):
	try:
		t = DtsForwardGroup.query.filter(and_(DtsForwardGroup.ip==data['data']['ip'],DtsForwardGroup.serverGroup==data['data']['servergroup'])).first()
		if t is not None:
			t.weight = data['data']['weight']
			db.session.commit()
		else:
			t = DtsForwardGroup(data['data']['ip'], data['data']['servergroup'], data['data']['weight'])
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 删除dts_forward_group
def del_dts_forward_group(data):
	try:
		t = DtsForwardGroup.query.filter(and_(DtsForwardGroup.ip==data['data']['ip'],DtsForwardGroup.serverGroup==data['data']['servergroup'])).first()
		if t is not None:
			db.session.delete(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 清空所有的dts_forward_group
def clear_dts_forward_group(data):
	try:
		rules = DtsForwardGroup.query.all()
		if rules is not None:
			for i in rules:
				db.session.delete(i)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


dts_forward_group_methods = {
	'query': get_dts_forward_group,
	'add': modify_dts_forward_group,
	'update': modify_dts_forward_group,
	'delete': del_dts_forward_group,
	'clear': clear_dts_forward_group
}


class DtsFilter(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	forward = db.Column(db.Integer, nullable=False)
	type = db.Column(db.String(20), nullable=False)
	filterName = db.Column(db.String(80), nullable=False)
	srcGroup = db.Column(db.String(80), nullable=False)
	dstGroup = db.Column(db.String(80), nullable=False)
	domainGroup = db.Column(db.String(80), nullable=False)
	gtld = db.Column(db.String(20), nullable=False)
	rd = db.Column(db.String(20), nullable=False)
	creditDname = db.Column(db.String(20), nullable=False)

	def __init__(self, forward, type, filterName, srcGroup, dstGroup, domainGroup, gtld, rd, creditDname):
		self.forward = forward
		self.type = type
		self.filterName = filterName
		self.srcGroup = srcGroup
		self.dstGroup = dstGroup
		self.domainGroup = domainGroup
		self.gtld = gtld
		self.rd = rd
		self.creditDname = creditDname


# 获取所有的DTS过滤器
def get_dts_filter(data):
	return to_dict_list(DtsFilter.query.all())


# 添加/修改DTS过滤器
def modify_dts_filter(data):
	try:
		data = data['data']
		t = DtsFilter.query.filter(and_(DtsFilter.filterName == data['filtername'], DtsFilter.srcGroup == data['srcgroup'], DtsFilter.dstGroup == data['dstgroup'], \
		DtsFilter.domainGroup == data['domaingroup'], DtsFilter.gtld == data['gtld'], DtsFilter.rd == data['rd'], DtsFilter.creditDname == data['creditdname'])).first()
		if t is None:
			tab = DtsFilter(data['forward'], data['type'], data['filtername'], data['srcgroup'], data['dstgroup'], data['domaingroup'], data['gtld'], data['rd'], data['creditdname'])
			db.session.add(tab)
			db.session.commit()
		else:
			t.forward = data['forward']
			t.type = data['type']
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 删除DTS过滤器
def del_dts_filter(data):
	try:
		data = data['data']
		t = DtsFilter.query.filter(and_(DtsFilter.filterName == data['filtername'], DtsFilter.srcGroup == data['srcgroup'], DtsFilter.dstGroup == data['dstgroup'], \
		DtsFilter.domainGroup == data['domaingroup'], DtsFilter.gtld == data['gtld'], DtsFilter.rd == data['rd'], DtsFilter.creditDname == data['creditdname'])).first()
		if t is not None:
			db.session.delete(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 清空所有
def clear_dts_filter(data):
	try:
		rules = DtsFilter.query.all()
		for rule in rules:
			db.session.delete(rule)
		db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 根据group_name查看数量
def get_dts_src_ip_group_num(group_name):
	try:
		rules = DtsSrcIpGroup.query.filter_by(group=group_name).all()
		if rules is not None:
			return len(rules)
	except Exception as e:
		logger.warning(str(e))
	return 0
		

def get_dts_dst_ip_group_num(group_name):
	try:
		rules = DtsDstIpGroup.query.filter_by(group=group_name).all()
		if rules is not None:
			return len(rules)
	except Exception as e:
		logger.warning(str(e))
	return 0
		

def get_dts_domain_group_num(group_name):
	try:
		rules = DtsDomainGroup.query.filter_by(group=group_name).all()
		if rules is not None:
			return len(rules)
	except Exception as e:
		logger.warning(str(e))
	return 0
		

# 根据srcGroup判断group是否存在
def dts_src_ip_group_judge(group_name):
	try:
		if DtsFilter.query.filter_by(srcGroup=group_name).first() is not None:
			return True	
	except Exception as e:
		logger.warning(str(e))
	return False
	

# 根据dstGroup判断group是否存在
def dts_dst_ip_group_judge(group_name):
	try:
		if DtsFilter.query.filter_by(dstGroup=group_name).first() is not None:
			return True	
	except Exception as e:
		logger.warning(str(e))
	return False
	

# 根据domainGroup判断group是否存在
def dts_domain_group_judge(group_name):
	try:
		if DtsFilter.query.filter_by(domainGroup=group_name).first() is not None:
			return True	
	except Exception as e:
		logger.warning(str(e))
	return False


# 根据srcGroup判断group是否可清空
def dts_src_ip_group_clear_judge():
	try:
		rules = DtsSrcIpGroup.query.all()
		if rules is not None:
			l = []
			for i in rules:
				if i.group not in l:
					l.append(i.group)
			for i in l:
				if dts_src_ip_group_judge(i): 
					return False
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 根据dstGroup判断group是否可清空
def dts_dst_ip_group_clear_judge():
	try:
		rules = DtsSrcIpGroup.query.all()
		if rules is not None:
			l = []
			for i in rules:
				if i.group not in l:
					l.append(i.group)
			for i in l:
				if dts_dst_ip_group_judge(i): 
					return False
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 根据domainGroup判断group是否可清空
def dts_domain_group_clear_judge():
	try:
		rules = DtsSrcIpGroup.query.all()
		if rules is not None:
			l = []
			for i in rules:
				if i.group not in l:
					l.append(i.group)
			for i in l:
				if dts_domain_group_judge(i): 
					return False
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


dts_filter_methods = {
	'query': get_dts_filter,
	'add': modify_dts_filter,
	'update': modify_dts_filter,
	'delete': del_dts_filter,
	'clear': clear_dts_filter
}


def get_all_dts():
	l = []
	src = to_dts_dict_list(DtsSrcIpGroup.query.all())
	for i in src:
		l.append({'source':'ms','id':0,'bt':'dts','sbt':'srcipgroup','op':'add','data':i})
	dst = to_dts_dict_list(DtsDstIpGroup.query.all())
	for i in dst:
		l.append({'source':'ms','id':0,'bt':'dts','sbt':'dstipgroup','op':'add','data':i})
	dom = to_dts_dict_list(DtsDomainGroup.query.all())
	for i in dom:
		l.append({'source':'ms','id':0,'bt':'dts','sbt':'domaingroup','op':'add','data':i})
	return l + to_no_bt_dict_list('dts','forwardserver',DtsForwardGroup.query.all()) + to_no_bt_dict_list('dts','dtsfilter',DtsFilter.query.all())

	





