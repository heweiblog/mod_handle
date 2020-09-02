#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from sqlalchemy import and_
from common.log import logger
from . import db,to_dict_list

class Oplog(db.Model):
	vid = db.Column(db.BigInteger, primary_key=True)
	action = db.Column(db.String(10), nullable=False)
	bt = db.Column(db.String(40), nullable=False)
	sbt = db.Column(db.String(40), nullable=False)
	id = db.Column(db.BigInteger, nullable=False)
	source = db.Column(db.String(10), nullable=False)
	status = db.Column(db.String(10), nullable=False)
	reason = db.Column(db.String(200))
	data = db.Column(db.Text, nullable=False)
	def __init__(self, action, bt, sbt, id, source, status, reason, data):
		self.action = action
		self.bt = bt
		self.sbt = sbt
		self.id = id
		self.source = source
		self.status = status
		self.reason = reason[:200] if len(reason) > 200 else reason
		data = json.dumps(data)
		self.data = data
	def get_oplog(self):
		return {
			'action': self.action,
			'bt': self.bt,
			'sbt': self.sbt,
			'vid': self.vid,
			'id': self.id,
			'source': self.source,
			'status': self.status,
			'reason': self.reason,
			'data': json.loads(self.data)
		}


def get_version():
	try:
		ms = Oplog.query.filter_by(source = 'ms').order_by(Oplog.id.desc()).first()
		crm = Oplog.query.order_by(Oplog.vid.desc()).first()
		return ms.id if ms is not None else 0, crm.vid if crm is not None else 0
	except Exception as e:
		logger.warning(str(e))
		return 0,0
	

def get_oplogs(start,limit):
	try:
		l = []
		oplogs = Oplog.query.filter(and_(Oplog.vid >= start,Oplog.vid < start+limit)).all()
		for i in oplogs:
			l.append(i.get_oplog())
		return {'contents':l}
	except Exception as e:
		logger.warning(str(e))
	return  {}


def id_check(source_id,source):
	try:
		o = Oplog.query.filter(and_(Oplog.id >= source_id,Oplog.source==source)).first()
		if o is None:
			return True
	except Exception as e:
		logger.warning(str(e))
	return False


def add_oplog(data,status,reason):
	#o = Oplog(data['op'], data['bt'], data['sbt'], data['id'], data['source'], status, reason, data['data'])
	o = Oplog(data['op'], data['bt'], data['sbt'], data['id'] if data['source'] == 'ms' else 0, data['source'], status, reason, data['data'])
	try:
		db.session.add(o)
		db.session.commit()
	except Exception as e:
		logger.warning(str(e))
		db.session.rollback()


def batch_add_oplog(data,status,reason):
	o = Oplog(data['op'], data['bt'], data['sbt'], data['id'], data['source'], status, reason, data['data'])
	try:
		db.session.add(o)
		db.session.commit()
	except Exception as e:
		logger.warning(str(e))
		db.session.rollback()


