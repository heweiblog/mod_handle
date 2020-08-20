#!/usr/bin/python
# -*- coding: utf-8 -*-

from common.log import logger
from sqlalchemy import and_
from . import db,to_dict_list,to_no_bt_dict_list,to_have_bt_dict_list


class ForwardServer(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	view = db.Column(db.String(80), nullable=False)
	servergroup = db.Column(db.String(80), nullable=False)
	ip = db.Column(db.String(80), nullable=False)
	weight = db.Column(db.Integer, nullable=False)

	def __init__(self, view, servergroup, ip, weight):
		self.view = view
		self.servergroup = servergroup
		self.ip = ip
		self.weight = weight


def forward_server_exist(srv):
	try:
		t = ForwardServer.query.filter_by(servergroup=srv).first()
		if t is not None:
			return True
	except Exception as e:
		logger.warning(str(e))
	return False


def get_bind_forward_server(data):
	try:
		t = ForwardServer.query.filter(and_(ForwardServer.view==data['data']['view'],ForwardServer.servergroup==data['data']['servergroup'])).all()
		if t is not None:
			l = []
			for i in t:
				s = {'ip':i.ip,'weight':i.weight}
				l.append(s)
			return l
	except Exception as e:
		logger.warning(str(e))
	return []


# 获取所有forward_server
def get_forward_server(data):
	return to_dict_list(ForwardServer.query.all())


# 添加/修改forward_server
def modify_forward_server(data):
	try:
		t = ForwardServer.query.filter(and_(ForwardServer.view==data['data']['view'],ForwardServer.servergroup==data['data']['servergroup'],ForwardServer.ip==data['data']['ip'])).first()
		if t is not None:
			t.weight = data['data']['weight']
			db.session.commit()
		else:
			t = ForwardServer(data['data']['view'], data['data']['servergroup'], data['data']['ip'], data['data']['weight'])
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 删除forward_server
def del_forward_server(data):
	try:
		t = ForwardServer.query.filter(and_(ForwardServer.view==data['data']['view'],ForwardServer.servergroup==data['data']['servergroup'],ForwardServer.ip==data['data']['ip'])).first()
		if t is not None:
			db.session.delete(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 清空forward_server
def clear_forward_server(data):
	try:
		rules = ForwardServer.query.all()
		if rules is not None:
			for i in rules:
				db.session.delete(i)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


forward_server_methods = {
	'query': get_forward_server,
	'add': modify_forward_server,
	'update': modify_forward_server,
	'delete': del_forward_server,
	'clear': clear_forward_server
}


class ForwardRules(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	view = db.Column(db.String(80), nullable=False)
	domain = db.Column(db.String(300), nullable=False)
	servergroup = db.Column(db.String(80), nullable=False)
	type = db.Column(db.String(20), nullable=False)
	action = db.Column(db.String(20), nullable=False)

	def __init__(self, view, domain, servergroup, type, action):
		self.view = view
		self.domain = domain
		self.servergroup = servergroup
		self.type = type
		self.action = action


def forward_server_delete_judge(srv):
	try:
		rules = ForwardRules.query.filter_by(servergroup=srv).first()
		if rules is not None:
			return True
	except Exception as e:
		logger.warning(str(e))
	return False


def forward_server_clear_judge():
	try:
		rules = ForwardServer.query.all()
		if rules is not None:
			for i in rules:
				if forward_server_delete_judge(i.servergroup):
					return False
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 获取所有forward_rules
def get_forward_rules(data):
	return to_dict_list(ForwardRules.query.all())


# 添加/修改forward_rules
def modify_forward_rules(data):
	try:
		t = ForwardRules.query.filter(and_(ForwardRules.view==data['data']['view'],ForwardRules.domain==data['data']['domain'])).first()
		if t is not None:
			t.type = data['data']['type']
			t.servergroup = data['data']['servergroup']
			t.action = data['data']['action']
			db.session.commit()
		else:
			t = ForwardRules(data['data']['view'], data['data']['domain'], data['data']['servergroup'], data['data']['type'], data['data']['action'])
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 从forward_rules删除元素
def del_forward_rules(data):
	try:
		t = ForwardRules.query.filter(and_(ForwardRules.view==data['data']['view'],ForwardRules.domain==data['data']['domain'])).first()
		if t is not None:
			db.session.delete(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 清空forward_rules
def clear_forward_rules(data):
	try:
		rules = ForwardRules.query.all()
		if rules is not None:
			for i in rules:
				db.session.delete(i)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


forward_rules_methods = {
	'query': get_forward_rules,
	'add': modify_forward_rules,
	'update': modify_forward_rules,
	'delete': del_forward_rules,
	'clear': clear_forward_rules
}


class Stub(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	bt = db.Column(db.String(40), nullable=False)
	sbt = db.Column(db.String(40), nullable=False)
	view = db.Column(db.String(80), nullable=False)
	domain = db.Column(db.String(300), nullable=False)
	ttl = db.Column(db.Integer, nullable=False)
	ns = db.Column(db.String(300))
	ip = db.Column(db.String(80))

	def __init__(self, bt, sbt, view, domain, ttl, ns, ip):
		self.bt = bt
		self.sbt = sbt
		self.view = view
		self.domain = domain
		self.ttl = ttl
		self.ns = ns
		self.ip = ip


# 获取所有stub
def get_stub(data):
	return to_dict_list(Stub.query.filter(and_(Stub.bt==data['bt'],Stub.sbt==data['sbt'])).all())


# 添加/修改stub
def modify_stub(data):
	try:
		t = Stub.query.filter(and_(Stub.bt==data['bt'],Stub.sbt==data['sbt'],Stub.view==data['data']['view'],Stub.domain==data['data']['domain'])).first()
		if t is not None:
			t.ns = data['data']['ns']
			t.ttl = data['data']['ttl']
			t.ip = data['data']['ip']
			db.session.commit()
		else:
			t = Stub(data['bt'], data['sbt'], data['data']['view'], data['data']['domain'], data['data']['ttl'], data['data']['ns'], data['data']['ip'])
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 从stub删除元素
def del_stub(data):
	try:
		t = Stub.query.filter(and_(Stub.bt==data['bt'],Stub.sbt==data['sbt'],Stub.view==data['data']['view'],Stub.domain==data['data']['domain'])).first()
		if t is not None:
			db.session.delete(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 清空stub
def clear_stub(data):
	try:
		rules = Stub.query.filter(and_(Stub.bt==data['bt'],Stub.sbt==data['sbt'])).all()
		if rules is not None:
			for i in rules:
				db.session.delete(i)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


stub_methods = {
	'query': get_stub,
	'add': modify_stub,
	'update': modify_stub,
	'delete': del_stub,
	'clear': clear_stub
}


class Dns64(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	view = db.Column(db.String(80), nullable=False)
	domain = db.Column(db.String(300), nullable=False)
	ipv6prefix = db.Column(db.String(80))

	def __init__(self, view, domain, ipv6prefix):
		self.view = view
		self.domain = domain
		self.ipv6prefix = ipv6prefix


# 获取所有dns64
def get_dns64(data):
	return to_dict_list(Dns64.query.all())


# 添加/修改dns64
def modify_dns64(data):
	try:
		t = Dns64.query.filter(and_(Dns64.view==data['data']['view'],Dns64.domain==data['data']['domain'])).first()
		if t is not None:
			t.ipv6prefix = data['data']['ipv6prefix']
			db.session.commit()
		else:
			t = Dns64(data['data']['view'], data['data']['domain'], data['data']['ipv6prefix'])
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 从dns64删除元素
def del_dns64(data):
	try:
		t = Dns64.query.filter(and_(Dns64.view==data['data']['view'],Dns64.domain==data['data']['domain'])).first()
		if t is not None:
			db.session.delete(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 清空dns64
def clear_dns64(data):
	try:
		rules = Dns64.query.all()
		if rules is not None:
			for i in rules:
				db.session.delete(i)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


dns64_methods = {
	'query': get_dns64,
	'add': modify_dns64,
	'update': modify_dns64,
	'delete': del_dns64,
	'clear': clear_dns64
}


class ViewIp(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	bt = db.Column(db.String(40), nullable=False)
	sbt = db.Column(db.String(40), nullable=False)
	view = db.Column(db.String(80), nullable=False)
	ip = db.Column(db.String(60), nullable=False)

	def __init__(self, bt, sbt, view, ip):
		self.bt = bt
		self.sbt = sbt
		self.view = view
		self.ip = ip


# 获取所有的view ip
def get_view_ip(data):
	return to_dict_list(ViewIp.query.filter(and_(ViewIp.bt==data['bt'],ViewIp.sbt==data['sbt'])).all())


# 添加 view ip
def add_view_ip(data):
	try:
		t = ViewIp.query.filter(and_(ViewIp.bt==data['bt'],ViewIp.sbt==data['sbt'],ViewIp.view==data['data']['view'],ViewIp.ip==data['data']['ip'])).first()
		if t is None:
			t = ViewIp(data['bt'], data['sbt'], data['data']['view'], data['data']['ip'])
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 删除view ip 
def del_view_ip(data):
	try:
		t = ViewIp.query.filter(and_(ViewIp.bt==data['bt'],ViewIp.sbt==data['sbt'],ViewIp.view==data['data']['view'],ViewIp.ip==data['data']['ip'])).first()
		if t is not None:
			db.session.delete(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 清空所有的view ip
def clear_view_ip(data):
	try:
		rules = ViewIp.query.filter(and_(ViewIp.bt==data['bt'],ViewIp.sbt==data['sbt'])).all()
		if rules is not None:
			for i in rules:
				db.session.delete(i)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


view_ip_methods = {
	'query': get_view_ip,
	'add': add_view_ip,
	'delete': del_view_ip,
	'clear': clear_view_ip
}


class ViewDomain(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	bt = db.Column(db.String(40), nullable=False)
	sbt = db.Column(db.String(40), nullable=False)
	view = db.Column(db.String(80), nullable=False)
	domain = db.Column(db.String(300), nullable=False)

	def __init__(self, bt, sbt, view, domain):
		self.bt = bt
		self.sbt = sbt
		self.view = view
		self.domain = domain


# 获取所有的view domain
def get_view_domain(data):
	return to_dict_list(ViewDomain.query.filter(and_(ViewDomain.bt==data['bt'],ViewDomain.sbt==data['sbt'])).all())


# 添加 view domain
def add_view_domain(data):
	try:
		t = ViewDomain.query.filter(and_(ViewDomain.bt==data['bt'],ViewDomain.sbt==data['sbt'],ViewDomain.view==data['data']['view'],ViewDomain.domain==data['data']['domain'])).first()
		if t is None:
			t = ViewDomain(data['bt'], data['sbt'], data['data']['view'], data['data']['domain'])
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 删除view domain 
def del_view_domain(data):
	try:
		t = ViewDomain.query.filter(and_(ViewDomain.bt==data['bt'],ViewDomain.sbt==data['sbt'],ViewDomain.view==data['data']['view'],ViewDomain.domain==data['data']['domain'])).first()
		if t is not None:
			db.session.delete(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 清空所有的view domain
def clear_view_domain(data):
	try:
		rules = ViewDomain.query.filter(and_(ViewDomain.bt==data['bt'],ViewDomain.sbt==data['sbt'])).all()
		if rules is not None:
			for i in rules:
				db.session.delete(i)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


view_domain_methods = {
	'query': get_view_domain,
	'add': add_view_domain,
	'delete': del_view_domain,
	'clear': clear_view_domain
}


def get_all_fpga_bind():
	no_list = ['edns','forward']
	view_ip_list = to_have_bt_dict_list(ViewIp.query.all())
	for i in view_ip_list:
		if i['bt'] in no_list: 
			view_ip_list.remove(i)
	return view_ip_list


def get_all_bind():
	return to_no_bt_dict_list('forward','forwardserver',ForwardServer.query.all()) + \
	to_no_bt_dict_list('forward','rules',ForwardRules.query.all()) + to_no_bt_dict_list('dns64','rules',Dns64.query.all()) + \
	to_have_bt_dict_list(ViewIp.query.all()) + to_have_bt_dict_list(ViewDomain.query.all()) + to_have_bt_dict_list(Stub.query.all())

