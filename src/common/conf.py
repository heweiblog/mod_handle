#!/usr/bin/python3
# -*- coding: utf-8 -*-

from configparser import ConfigParser

class CrmParser(ConfigParser):
	def as_dict(self):
		d = dict(self._sections)
		for k in d:
			d[k] = dict(d[k])
		return d

config = CrmParser()
config.read('/etc/hcrm.ini')

crm_cfg = config.as_dict()

