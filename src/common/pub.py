#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
from common.log import logger
from common.conf import crm_cfg

version = '1.0.3'

fpga_bt = ['iptables', 'ipfragment', 'dnsipfragment', 'icmpflood', 'tcpflood', 'udpflood', 'creditdname', 'backendthreshold', 'replythreshold', 'spreadecho', 'dts', 'iptrans']

ybind_bt = ['poisonprotect', 'importdnameprotect', 'rrfilter', 'forward', 'edns', 'stub', 'dns64', 'rootconfig']

handle_bt = {'useripwhitelist','ipthreshold','handlethreshold','srcipaccesscontrol','handleaccesscontrol','backend','businessservice','businessproto','certificate','xforce',
			'cachesmartupdate','cacheprefetch','selfcheck','backendmeter','stub'}

proxy_bt = []

xforward_bt = []

proxy_xforward_bt = ['backend','businessservice','certificate','xforce','cachesmartupdate','cacheprefetch','selfcheck','stub']

kernel_bt = ['useripwhitelist','ipthreshold','handlethreshold','srcipaccesscontrol','handleaccesscontrol','backendmeter']

dnsys_addr = (crm_cfg['crm']['ip'], int(crm_cfg['crm']['port']))

ADD = 'add'
DEL = 'delete'
MOD = 'update'
QUERY = 'query'
CLEAR = 'clear'

DEFAULTGROUP = 'None'

CONFDATA = 'conf'
TASKDATA = 'task'


# 后续可能得实现只转换key为小写,值不变
def data_check(data):
	logger.info('recv data: {}'.format(data))
	if isinstance(data,dict):
		#data = json.loads(json.dumps(data).lower())
		return data
	elif isinstance(data,str):
		#data = json.loads(data.lower())
		data = json.loads(data)
		return data
	return None
