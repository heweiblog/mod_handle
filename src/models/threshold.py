#!/usr/bin/python
# -*- coding: utf-8 -*-

from common.log import logger
from sqlalchemy import and_
from . import db,to_dict_list,to_no_bt_dict_list,to_have_bt_dict_list


class TotalThreshold(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	bt = db.Column(db.String(40), nullable=False)
	sbt = db.Column(db.String(40), nullable=False)
	threshold = db.Column(db.BigInteger, nullable=False)

	def __init__(self, bt, sbt, threshold):
		self.bt = bt
		self.sbt = sbt
		self.threshold = threshold
	def get_dict(self):
		return {'threshold': self.threshold}
	def get_answer_len(self):
		return {'maxLen': self.threshold}
	def get_odds(self):
		return {'odds': self.threshold}
	def to_dict(self):
		if self.sbt == 'maxanswerlen':
			return {'source':'ms','id':0,'bt':self.bt,'sbt':self.sbt,'op':'update','data':{'maxLen':self.threshold}}
		elif self.sbt == 'odds':
			return {'source':'ms','id':0,'bt':self.bt,'sbt':self.sbt,'op':'update','data':{'odds':self.threshold}}
		return {'source':'ms','id':0,'bt':self.bt,'sbt':self.sbt,'op':'update','data':{'threshold':self.threshold}}


def get_all_total_threshold():
	try:
		rules = TotalThreshold.query.all()
		l = []
		for i in rules:
			l.append(i.to_dict())
		return l
	except Exception as e:
		logger.warning(str(e))
	return []


# 获取总限速阈值
def get_total_threshold(data):
	try:
		t = TotalThreshold.query.filter(and_(TotalThreshold.bt==data['bt'],TotalThreshold.sbt==data['sbt'])).first()
		if t is not None:
			if data['sbt'] == 'maxanswerlen':
				return t.get_answer_len()
			elif data['sbt'] == 'odds':
				return t.get_odds()
			return t.get_dict()
	except Exception as e:
		logger.warning(str(e))
	return None



# 修改总限速阈值
def modify_total_threshold(data):
	try:
		t = TotalThreshold.query.filter(and_(TotalThreshold.bt==data['bt'],TotalThreshold.sbt==data['sbt'])).first()
		if t is not None:
			if data['sbt'] == 'maxanswerlen':
				t.threshold = data['data']['maxlen']
				db.session.commit()
			elif data['sbt'] == 'odds':
				t.threshold = data['data']['odds']
				db.session.commit()
			else:
				t.threshold = data['data']['threshold']
				db.session.commit()
		else:
			if data['sbt'] == 'maxanswerlen':
				t = TotalThreshold(data['bt'], data['sbt'], data['data']['maxlen'])
				db.session.add(t)
				db.session.commit()
			elif data['sbt'] == 'odds':
				t = TotalThreshold(data['bt'], data['sbt'], data['data']['odds'])
				db.session.add(t)
				db.session.commit()
			else:
				t = TotalThreshold(data['bt'], data['sbt'], data['data']['threshold'])
				db.session.add(t)
				db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


total_threshold_methods = {
	'query': get_total_threshold,
	'add': modify_total_threshold,
	'update': modify_total_threshold
}


class IpThreshold(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	bt = db.Column(db.String(40), nullable=False)
	sbt = db.Column(db.String(40), nullable=False)
	ip = db.Column(db.String(60), nullable=False)
	threshold = db.Column(db.BigInteger, nullable=False)

	def __init__(self, bt, sbt, ip, threshold):
		self.bt = bt
		self.sbt = sbt
		self.ip = ip
		self.threshold = threshold


# 获取所有的ip限速策略
def get_ip_threshold(data):
	return to_dict_list(IpThreshold.query.filter(and_(IpThreshold.bt==data['bt'],IpThreshold.sbt==data['sbt'])).all())


# 添加/修改ip限速策略
def modify_ip_threshold(data):
	try:
		t = IpThreshold.query.filter(and_(IpThreshold.bt==data['bt'],IpThreshold.sbt==data['sbt'],IpThreshold.ip==data['data']['ip'])).first()
		if t is not None:
			t.threshold = data['data']['threshold']
			db.session.commit()
		else:
			t = IpThreshold(data['bt'], data['sbt'], data['data']['ip'], data['data']['threshold'])
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 删除ip限速策略
def del_ip_threshold(data):
	try:
		t = IpThreshold.query.filter(and_(IpThreshold.bt==data['bt'],IpThreshold.sbt==data['sbt'],IpThreshold.ip==data['data']['ip'])).first()
		if t is not None:
			db.session.delete(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 清空所有的ip限速策略
def clear_ip_threshold(data):
	try:
		rules = IpThreshold.query.filter(and_(IpThreshold.bt==data['bt'],IpThreshold.sbt==data['sbt'])).all()
		if rules is not None:
			for i in rules:
				db.session.delete(i)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


ip_threshold_methods = {
	'query': get_ip_threshold,
	'add': modify_ip_threshold,
	'update': modify_ip_threshold,
	'delete': del_ip_threshold,
	'clear': clear_ip_threshold
}



class DomainThreshold(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	bt = db.Column(db.String(40), nullable=False)
	sbt = db.Column(db.String(40), nullable=False)
	domain = db.Column(db.String(300), nullable=False)
	threshold = db.Column(db.BigInteger, nullable=False)

	def __init__(self, bt, sbt, domain, threshold):
		self.bt = bt
		self.sbt = sbt
		self.domain = domain
		self.threshold = threshold


# 获取所有的domain限速策略
def get_domain_threshold(data):
	return to_dict_list(DomainThreshold.query.filter(and_(DomainThreshold.bt==data['bt'],DomainThreshold.sbt==data['sbt'])).all())


# 添加/修改domain限速策略
def modify_domain_threshold(data):
	try:
		t = DomainThreshold.query.filter(and_(DomainThreshold.bt==data['bt'],DomainThreshold.sbt==data['sbt'],DomainThreshold.domain==data['data']['domain'])).first()
		if t is not None:
			t.threshold = data['data']['threshold']
			db.session.commit()
		else:
			t = DomainThreshold(data['bt'], data['sbt'], data['data']['domain'], data['data']['threshold'])
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 删除domain限速策略
def del_domain_threshold(data):
	try:
		t = DomainThreshold.query.filter(and_(DomainThreshold.bt==data['bt'],DomainThreshold.sbt==data['sbt'],DomainThreshold.domain==data['data']['domain'])).first()
		if t is not None:
			db.session.delete(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 清空所有的domain限速策略
def clear_domain_threshold(data):
	try:
		rules = DomainThreshold.query.filter(and_(DomainThreshold.bt==data['bt'],DomainThreshold.sbt==data['sbt'])).all()
		if rules is not None:
			for i in rules:
				db.session.delete(i)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


domain_threshold_methods = {
	'query': get_domain_threshold,
	'add': modify_domain_threshold,
	'update': modify_domain_threshold,
	'delete': del_domain_threshold,
	'clear': clear_domain_threshold
}


class IpDomainThreshold(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	ip = db.Column(db.String(60), nullable=False)
	domain = db.Column(db.String(300), nullable=False)
	threshold = db.Column(db.BigInteger, nullable=False)

	def __init__(self, ip, domain, threshold):
		self.ip = ip
		self.domain = domain
		self.threshold = threshold


# 获取所有的 ip domain 限速策略
def get_ip_domain_threshold(data):
	return to_dict_list(IpDomainThreshold.query.all())


# 添加/修改 ip domain 限速策略
def modify_ip_domain_threshold(data):
	try:
		t = IpDomainThreshold.query.filter(and_(IpDomainThreshold.ip==data['data']['ip'],IpDomainThreshold.domain==data['data']['domain'])).first()
		if t is not None:
			t.threshold = data['data']['threshold']
			db.session.commit()
		else:
			t = IpDomainThreshold(data['data']['ip'], data['data']['domain'], data['data']['threshold'])
			db.session.add(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 删除domain限速策略
def del_ip_domain_threshold(data):
	try:
		t = IpDomainThreshold.query.filter(and_(IpDomainThreshold.ip==data['data']['ip'],IpDomainThreshold.domain==data['data']['domain'])).first()
		if t is not None:
			db.session.delete(t)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


# 清空所有的domain限速策略
def clear_ip_domain_threshold(data):
	try:
		rules = IpDomainThreshold.query.all()
		if rules is not None:
			for i in rules:
				db.session.delete(i)
			db.session.commit()
		return True
	except Exception as e:
		logger.warning(str(e))
	return False


ip_domain_threshold_methods = {
	'query': get_ip_domain_threshold,
	'add': modify_ip_domain_threshold,
	'update': modify_ip_domain_threshold,
	'delete': del_ip_domain_threshold,
	'clear': clear_ip_domain_threshold
}


def get_all_threshold():
	return get_all_total_threshold() + to_have_bt_dict_list(IpThreshold.query.all()) + \
	to_have_bt_dict_list(DomainThreshold.query.all()) + to_no_bt_dict_list('ipdomainthreshold','rules',IpDomainThreshold.query.all())
