#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from common.log import logger
from common.pub import DEFAULTGROUP
from sqlalchemy import and_
from . import db,switch,acl,bind,to_dict_list,to_no_bt_dict_list,to_have_bt_dict_list

class NxrRedirectIp(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	ip = db.Column(db.String(60), nullable=False)
	view = db.Column(db.String(80), nullable=False)
	weight = db.Column(db.Integer, nullable=False)

	def __init__(self, ip, view, weight):
		self.ip = ip
		self.view = view
		self.weight = weight


# 获取所有的nxr重定向ip
def get_nxr_redirect_ip(data):
	return to_dict_list(NxrRedirectIp.query.all())


# 添加/修改nxr重定向ip
def modify_nxr_redirect_ip(data):
	try:
		t = NxrRedirectIp.query.filter(and_(NxrRedirectIp.ip==data['data']['ip'],NxrRedirectIp.view==data['data']['view'])).first()
		if t is not None:
			t.weight = data['data']['weight']
			db.session.commit()
		else:
			t = NxrRedirectIp(data['data']['ip'], data['data']['view'], data['data']['weight'])
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 删除nxr重定向ip
def del_nxr_redirect_ip(data):
	try:
		t = NxrRedirectIp.query.filter(and_(NxrRedirectIp.ip==data['data']['ip'],NxrRedirectIp.view==data['data']['view'])).first()
		if t is not None:
			db.session.delete(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 清空所有的nxr重定向ip
def clear_nxr_redirect_ip(data):
	try:
		rules = NxrRedirectIp.query.all()
		if rules is not None:
			for i in rules:
				db.session.delete(i)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


nxr_redirect_ip_methods = {
	'query': get_nxr_redirect_ip,
	'add': modify_nxr_redirect_ip,
	'update': modify_nxr_redirect_ip,
	'delete': del_nxr_redirect_ip,
	'clear': clear_nxr_redirect_ip
}


# sortlist后续看需求修改
class Sortlist(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	domain = db.Column(db.String(300), nullable=False)
	view = db.Column(db.String(80), nullable=False)
	sortlist = db.Column(db.String(300), nullable=False)

	def __init__(self, domain, view, sortlist):
		self.domain = domain
		self.view = view
		self.sortlist = sortlist

	def get_dict(self):
		return {'domain': self.domain, 'view': self.view, 'sortlist': json.loads(self.sortlist)}
	def to_dict(self):
		return {'source':'ms','id':0,'bt':'sortlist','sbt':'rules','op':'add','data':self.get_dict()}


def get_all_sortlist():
	try:
		rules = Sortlist.query.all()
		if rules is not None:
			l = []
			for i in rules:
				l.append(i.get_dict())
			return l
	except Exception as e:
		logger.warning(str(e))
	return []


# 获取所有的sortlist
def get_sortlist(data):
	try:
		rules = Sortlist.query.all()
		if rules is not None:
			l = []
			for i in rules:
				l.append(i.get_dict())
			if len(l) > 0:
				return l
	except Exception as e:
		logger.warning(str(e))
	return None


# 添加/修改sortlist
def modify_sortlist(data):
	try:
		t = Sortlist.query.filter(and_(Sortlist.domain==data['data']['domain'],Sortlist.view==data['data']['view'])).first()
		if t is not None:
			t.sortlist = json.dumps(data['data']['sortlist'])
			db.session.commit()
		else:
			t = Sortlist(data['data']['domain'], data['data']['view'], json.dumps(data['data']['sortlist']))
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 删除sortlist
def del_sortlist(data):
	try:
		t = Sortlist.query.filter(and_(Sortlist.domain==data['data']['domain'],Sortlist.view==data['data']['view'])).first()
		if t is not None:
			db.session.delete(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 清空所有的sortlist
def clear_sortlist(data):
	try:
		rules = Sortlist.query.all()
		if rules is not None:
			for i in rules:
				db.session.delete(i)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


sortlist_methods = {
	'query': get_sortlist,
	'add': modify_sortlist,
	'update': modify_sortlist,
	'delete': del_sortlist,
	'clear': clear_sortlist
}


class View(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	viewName = db.Column(db.String(80), nullable=False)
	srcIpGroup = db.Column(db.String(80), nullable=False)
	domainGroup = db.Column(db.String(80), nullable=False)
	dstIpGroup = db.Column(db.String(80), nullable=False)
	rd = db.Column(db.String(20))

	def __init__(self, viewName, srcIpGroup, domainGroup, dstIpGroup, rd):
		self.viewName = viewName
		self.srcIpGroup = srcIpGroup
		self.domainGroup = domainGroup
		self.dstIpGroup = dstIpGroup
		self.rd = rd


# 判断view是否存在
def view_exist(name):
	try:
		rules = View.query.filter_by(viewName=name).first()
		if rules is not None:
			return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 获取所有view
def get_view(data):
	return to_dict_list(View.query.all())


# 添加view
def modify_view(data):
	try:
		t = View.query.filter(and_(View.viewName==data['data']['viewname'],View.srcIpGroup==data['data']['srcipgroup'],\
		View.domainGroup==data['data']['domaingroup'],View.dstIpGroup==data['data']['dstipgroup'],View.rd==data['data']['rd'])).first()
		if t is  None:
			t = View(data['data']['viewname'], data['data']['srcipgroup'], data['data']['domaingroup'], data['data']['dstipgroup'], data['data']['rd'])
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 删除view
def del_view(data):
	try:
		t = View.query.filter(and_(View.viewName==data['data']['viewname'],View.srcIpGroup==data['data']['srcipgroup'],\
		View.domainGroup==data['data']['domaingroup'],View.dstIpGroup==data['data']['dstipgroup'],View.rd==data['data']['rd'])).first()
		if t is not None:
			db.session.delete(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 清空view
def clear_view(data):
	try:
		rules = View.query.all()
		if rules is not None:
			for i in rules:
				db.session.delete(i)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


def view_src_ip_group_judge(group_name):
	if View.query.filter_by(srcIpGroup=group_name).first() is not None:
		return False
	return True	
	

def view_dst_ip_group_judge(group_name):
	if View.query.filter_by(dstIpGroup=group_name).first() is not None:
		return False
	return True	
	

def view_domain_group_judge(group_name):
	if View.query.filter_by(domainGroup=group_name).first() is not None:
		return False
	return True	
	

view_methods = {
	'query': get_view,
	'add': modify_view,
	'update': modify_view,
	'delete': del_view,
	'clear': clear_view
}


class CacheQtype(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	view = db.Column(db.String(80), nullable=False)
	qtype = db.Column(db.String(20), nullable=False)

	def __init__(self, view, qtype):
		self.view = view
		self.qtype = qtype

	def get_dict(self):
		return {'view': self.view, 'qtype': self.qtype}


# 获取所有的view qtype
def get_view_qtype(data):
	return to_dict_list(CacheQtype.query.all())


# 添加view qtype
def add_view_qtype(data):
	try:
		t = CacheQtype.query.filter(and_(CacheQtype.view==data['data']['view'],CacheQtype.qtype==data['data']['qtype'])).first()
		if t is None:
			t = CacheQtype(data['data']['view'], data['data']['qtype'])
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 删除view qtype
def del_view_qtype(data):
	try:
		t = CacheQtype.query.filter(and_(CacheQtype.view==data['data']['view'],CacheQtype.qtype==data['data']['qtype'])).first()
		if t is not None:
			db.session.delete(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 清空所有的view qtype
def clear_view_qtype(data):
	try:
		rules = CacheQtype.query.all()
		if rules is not None:
			for i in rules:
				db.session.delete(i)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


view_qtype_methods = {
	'query': get_view_qtype,
	'add': add_view_qtype,
	'delete': del_view_qtype,
	'clear': clear_view_qtype
}


class Ttl(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	view = db.Column(db.String(80), nullable=False)
	domain = db.Column(db.String(300), nullable=False)
	minttl = db.Column(db.Integer, nullable=False)
	maxttl = db.Column(db.Integer, nullable=False)

	def __init__(self, view, domain, minttl, maxttl):
		self.view = view
		self.domain = domain
		self.minttl = minttl
		self.maxttl = maxttl


# 获取所有ttl
def get_ttl(data):
	return to_dict_list(Ttl.query.all())


# 添加/修改ttl
def modify_ttl(data):
	try:
		t = Ttl.query.filter(and_(Ttl.view==data['data']['view'],Ttl.domain==data['data']['domain'])).first()
		if t is not None:
			t.maxttl = data['data']['maxttl']
			t.minttl = data['data']['minttl']
			db.session.commit()
		else:
			t = Ttl(data['data']['view'], data['data']['domain'], data['data']['minttl'], data['data']['maxttl'])
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 从ttl删除元素
def del_ttl(data):
	try:
		t = Ttl.query.filter(and_(Ttl.view==data['data']['view'],Ttl.domain==data['data']['domain'])).first()
		if t is not None:
			db.session.delete(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 清空ttl
def clear_ttl(data):
	try:
		rules = Ttl.query.all()
		if rules is not None:
			for i in rules:
				db.session.delete(i)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


ttl_methods = {
	'query': get_ttl,
	'add': modify_ttl,
	'update': modify_ttl,
	'delete': del_ttl,
	'clear': clear_ttl
}


class Rrset(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	view = db.Column(db.String(80), nullable=False)
	qtype = db.Column(db.String(20), nullable=False)
	domain = db.Column(db.String(300), nullable=False)
	ttl = db.Column(db.Integer, nullable=False)
	answer = db.Column(db.String(480), nullable=False)
	weight = db.Column(db.Integer, nullable=False)

	def __init__(self, view, qtype, domain, ttl, answer, weight):
		self.view = view
		self.qtype = qtype
		self.domain = domain
		self.ttl = ttl
		self.answer = answer
		self.weight = weight


# 获取所有rrset
def get_rrset(data):
	return to_dict_list(Rrset.query.all())


# 添加/修改rrset
def modify_rrset(data):
	try:
		t = Rrset.query.filter(and_(Rrset.view==data['data']['view'],Rrset.qtype==data['data']['qtype'],Rrset.domain==data['data']['domain'])).first()
		if t is not None:
			t.answer = data['data']['answer']
			t.weight = data['data']['weight']
			t.ttl = data['data']['ttl']
			db.session.commit()
		else:
			t = Rrset(data['data']['view'], data['data']['qtype'], data['data']['domain'], data['data']['ttl'], data['data']['answer'], data['data']['weight'])
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 删除rrset
def del_rrset(data):
	try:
		t = Rrset.query.filter(and_(Rrset.view==data['data']['view'],Rrset.qtype==data['data']['qtype'],Rrset.domain==data['data']['domain'])).first()
		if t is not None:
			db.session.delete(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 清空rrset
def clear_rrset(data):
	try:
		rules = Rrset.query.all()
		if rules is not None:
			for i in rules:
				db.session.delete(i)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


rrset_methods = {
	'query': get_rrset,
	'add': modify_rrset,
	'update': modify_rrset,
	'delete': del_rrset,
	'clear': clear_rrset
}


class Rrfilter(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	view = db.Column(db.String(80), nullable=False)
	qtype = db.Column(db.String(20), nullable=False)
	domain = db.Column(db.String(300), nullable=False)
	answer = db.Column(db.String(360), nullable=False)

	def __init__(self, view, qtype, domain, answer):
		self.view = view
		self.qtype = qtype
		self.domain = domain
		self.answer = answer


# 获取所有rrfilter
def get_rrfilter(data):
	return to_dict_list(Rrfilter.query.all())


# 添加/修改rrfilter
def modify_rrfilter(data):
	try:
		t = Rrfilter.query.filter(and_(Rrfilter.view==data['data']['view'],Rrfilter.qtype==data['data']['qtype'],Rrfilter.domain==data['data']['domain'])).first()
		if t is not None:
			t.answer = data['data']['answer']
			db.session.commit()
		else:
			t = Rrfilter(data['data']['view'], data['data']['qtype'], data['data']['domain'], data['data']['answer'])
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 删除rrfilter
def del_rrfilter(data):
	try:
		t = Rrfilter.query.filter(and_(Rrfilter.view==data['data']['view'],Rrfilter.qtype==data['data']['qtype'],Rrfilter.domain==data['data']['domain'])).first()
		if t is not None:
			db.session.delete(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 清空rrfilter
def clear_rrfilter(data):
	try:
		rules = Rrfilter.query.all()
		if rules is not None:
			for i in rules:
				db.session.delete(i)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


rrfilter_methods = {
	'query': get_rrfilter,
	'add': modify_rrfilter,
	'update': modify_rrfilter,
	'delete': del_rrfilter,
	'clear': clear_rrfilter
}


# 根据srcGroup判断group是否在view中存在
def acl_src_ip_group_judge(group_name):
	try:
		if View.query.filter_by(srcIpGroup=group_name).first() is not None:
			return True	
	except Exception as e:
		logger.warning(str(e))
	return False
	

# 根据dstGroup判断group是否在view中存在
def acl_dst_ip_group_judge(group_name):
	try:
		if View.query.filter_by(dstIpGroup=group_name).first() is not None:
			return True	
	except Exception as e:
		logger.warning(str(e))
	return False
	

# 根据domainGroup判断group是否在view中存在
def acl_domain_group_judge(group_name):
	try:
		if View.query.filter_by(domainGroup=group_name).first() is not None:
			return True	
	except Exception as e:
		logger.warning(str(e))
	return False


# 根据srcGroup判断group是否可清空
def acl_src_ip_group_clear_judge():
	try:
		rules = acl.SrcIpList.query.all()
		if rules is not None:
			l = []
			for i in rules:
				if i.group not in l:
					l.append(i.group)
			for i in l:
				if acl_src_ip_group_judge(i): 
					return False
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


def acl_dst_ip_group_clear_judge():
	try:
		rules = acl.DstIpList.query.all()
		if rules is not None:
			l = []
			for i in rules:
				if i.group not in l:
					l.append(i.group)
			for i in l:
				if acl_dst_ip_group_judge(i): 
					return False
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


def acl_domain_group_clear_judge():
	try:
		rules = acl.AclDomainList.query.all()
		if rules is not None:
			l = []
			for i in rules:
				if i.group not in l:
					l.append(i.group)
			for i in l:
				if acl_domain_group_judge(i): 
					return False
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


def view_relation_judge(view_name):
	# 开关暂时不做判断
	#if switch.ViewSwitch.query.filter_by(view=view_name).first() is not None:
		#return False
	if NxrRedirectIp.query.filter_by(view=view_name).first() is not None:
		return 'view are referenced by Nxr RedirectIp'
	if Sortlist.query.filter_by(view=view_name).first() is not None:
		return 'view are referenced by Sortlist'
	if CacheQtype.query.filter_by(view=view_name).first() is not None:
		return 'view are referenced by CacheQtype'
	if Ttl.query.filter_by(view=view_name).first() is not None:
		return 'view are referenced by ttl'
	if Rrset.query.filter_by(view=view_name).first() is not None:
		return 'view are referenced by rrset'
	if Rrfilter.query.filter_by(view=view_name).first() is not None:
		return 'view are referenced by rrfilter'
	if bind.ForwardServer.query.filter_by(view=view_name).first() is not None:
		return 'view are referenced by ForwardServer'
	if bind.ForwardRules.query.filter_by(view=view_name).first() is not None:
		return 'view are referenced by ForwardRules'
	if bind.Stub.query.filter_by(view=view_name).first() is not None:
		return 'view are referenced by Stub'
	if bind.Dns64.query.filter_by(view=view_name).first() is not None:
		return 'view are referenced by Dns64'
	if bind.ViewIp.query.filter_by(view=view_name).first() is not None:
		return 'view are referenced by ViewIp'
	if bind.ViewDomain.query.filter_by(view=view_name).first() is not None:
		return 'view are referenced by ViewDomain'
	return 'true'


def view_clear_check():
	try:
		rules = View.query.all()
		if rules is not None:
			l = []
			for i in rules:
				if i.viewName not in l:
					l.append(i.viewName)
			for i in l:
				if view_relation_judge(i) != 'true':
					return False
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


def get_all_fpga_view():
	return to_no_bt_dict_list('nxr','redirectip',NxrRedirectIp.query.all()) + get_all_sortlist() + \
	to_no_bt_dict_list('view','view',View.query.all()) + to_no_bt_dict_list('selfcheck','cacheqtype',CacheQtype.query.all()) + \
	to_no_bt_dict_list('ttl','rules',Ttl.query.all()) + to_no_bt_dict_list('rrset','rules',Rrset.query.all()) 


def get_all_view():
	return to_no_bt_dict_list('nxr','redirectip',NxrRedirectIp.query.all()) + get_all_sortlist() + \
	to_no_bt_dict_list('view','view',View.query.all()) + to_no_bt_dict_list('selfcheck','cacheqtype',CacheQtype.query.all()) + \
	to_no_bt_dict_list('ttl','rules',Ttl.query.all()) + to_no_bt_dict_list('rrset','rules',Rrset.query.all()) + \
	to_no_bt_dict_list('rrfilter','rules',Rrfilter.query.all()) 

