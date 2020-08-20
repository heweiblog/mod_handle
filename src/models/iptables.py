#!/usr/bin/python
# -*- coding: utf-8 -*-

from common.log import logger
from sqlalchemy import and_
from . import db,to_dict_list,to_no_bt_dict_list


class Iptables(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	priority = db.Column(db.Integer, nullable=False)
	action = db.Column(db.String(20), nullable=False)
	proto = db.Column(db.String(20), nullable=False)
	srcIp = db.Column(db.String(60), nullable=False)
	destIp = db.Column(db.String(60), nullable=False)
	srcPortStart= db.Column(db.Integer, nullable=False)
	srcPortEnd = db.Column(db.Integer, nullable=False)
	destPortStart= db.Column(db.Integer, nullable=False)
	destPortEnd = db.Column(db.Integer, nullable=False)

	def __init__(self, priority, action, proto, srcip, destip, srcportstart, srcportend, destportstart, destportend):
		self.priority = priority
		self.action = action
		self.proto = proto
		self.srcIp = srcip
		self.destIp = destip
		self.srcPortStart = srcportstart
		self.srcPortEnd = srcportend
		self.destPortStart = destportstart
		self.destPortEnd = destportend


# 获取所有的五元组策略
def get_iptables_rules(data):
	return to_dict_list(Iptables.query.all())


def check_iptables_priority(level):
	try:
		rules = Iptables.query.filter_by(priority=level).first()
		if rules is not None:
			return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 添加/修改五元组策略
def modify_iptables_rules(data):
	try:
		data = data['data']
		#t = Iptables.query.filter(and_(Iptables.proto == data['proto'], Iptables.srcIp == data['srcip'], Iptables.destIp == data['destip'], Iptables.srcPortStart == data['srcportstart'],\
		#Iptables.srcPortEnd == data['srcportend'], Iptables.destPortStart == data['destportstart'], Iptables.destPortEnd == data['destportend'], Iptables.priority == data['priority'])).first()
		t = Iptables.query.filter_by(priority=data['priority']).first()
		if t is None:
			tab = Iptables(data['priority'], data['action'], data['proto'], data['srcip'], data['destip'], data['srcportstart'], data['srcportend'], data['destportstart'], data['destportend'])
			db.session.add(tab)
			db.session.commit()
		else:
			#t.priority = data['priority']
			t.action = data['action']

			t.proto = data['proto']
			t.srcIp = data['srcip']
			t.destIp = data['destip']
			t.srcPortStart = data['srcportstart']
			t.srcPortEnd = data['srcportend']
			t.destPortStart = data['destportstart']
			t.destPortEnd = data['destportend']

			db.session.commit()

		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 删除五元组策略
def del_iptables_rules(data):
	try:
		data = data['data']
		t = Iptables.query.filter(and_(Iptables.proto == data['proto'], Iptables.srcIp == data['srcip'], Iptables.destIp == data['destip'], Iptables.srcPortStart == data['srcportstart'],\
		Iptables.srcPortEnd == data['srcportend'], Iptables.destPortStart == data['destportstart'], Iptables.destPortEnd == data['destportend'])).first()
		if t is not None:
			db.session.delete(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False



# 清空所有的五元组策略
def clear_iptables_rules(data):
	try:
		rules = Iptables.query.all()
		for rule in rules:
			db.session.delete(rule)
		db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


iptables_methods = {
	'query': get_iptables_rules,
	'add': modify_iptables_rules,
	'update': modify_iptables_rules,
	'delete': del_iptables_rules,
	'clear': clear_iptables_rules
}


def get_all_iptables():
	return to_no_bt_dict_list('iptables','rules',Iptables.query.all()) 

