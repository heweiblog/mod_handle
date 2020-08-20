#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
from common.log import logger
from common.conf import crm_cfg

fpga_bt = ['iptables', 'ipfragment', 'dnsipfragment', 'icmpflood', 'tcpflood', 'udpflood', 'creditdname', 'backendthreshold', 'replythreshold', 'spreadecho', 'dts', 'iptrans']

ybind_bt = ['poisonprotect', 'importdnameprotect', 'rrfilter', 'forward', 'edns', 'stub', 'dns64', 'rootconfig']

handle_bt = ['ipacl', 'ipmeter', 'handlemeter', 'ipblack', 'handleblack', 'forwardserver', 'servicecontrol', 'xforce', 'cacheprefetch', 'selfcheck', 'backendmeter']

proxy_bt = ['forwardserver', 'servicecontrol']

dnsys_addr = (crm_cfg['crm']['ip'], int(crm_cfg['crm']['port']))

ADD = 'add'
DEL = 'delete'
MOD = 'update'
QUERY = 'query'
CLEAR = 'clear'

DEFAULTGROUP = 'None'

CONFDATA = 'conf'
TASKDATA = 'task'

'''
def data_change(data):
	if 'contents' in data:
		for i in data['contents']:
			for k in i:
				if k != k.lower():
					i[k.lower()] = i[k]
					del i[k]
				if k == 'data':
					for j in i[k]:
						if j != j.lower():
						i[j.lower()] = i[k][j]
						del i[j]
'''


# 后续可能得实现只转换key为小写,值不变
def data_check(data):
	logger.info('recv data: {}'.format(data))
	if isinstance(data,dict):
		data = json.loads(json.dumps(data).lower())
		return data
	elif isinstance(data,str):
		data = json.loads(data.lower())
		return data
	return None
