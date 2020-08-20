#!/usr/bin/python3
# -*- coding: utf-8 -*-

from tld import is_tld
import json,IPy,re
from common.log import logger
from models.view import view_exist
from models.acl import src_ip_group_exist,dst_ip_group_exist,domain_group_exist
from models import db
#from common.pub import all_bt,all_sbt

all_bt = ['iptables', 'dnsipfragment', 'ipfragment', 'icmpflood', 'tcpflood', 'udpflood', 'creditdname', 'ipthreshold', 'domainthreshold', 'ipdomainthreshold', 'backendthreshold',
			'replythreshold', 'poisonprotect', 'amplificationattack', 'useripwhitelist', 'serviceipwhitelist', 'srcipaccesscontrol', 'domainaccesscontrol', 'ipdomainaccesscontrol', 
			'domainqtypeaccesscontrol','qtypeaccesscontrol', 'ipqtypeaccesscontrol', 'graydomainaccesscontrol', 'importdnameprotect', 'spreadecho', 'nxr', 'sortlist', 'dts', 
			'iptrans', 'acl', 'view', 'selfcheck', 'ttl', 'rrset', 'rrfilter', 'expiredactivate', 'cachedisable', 'cachesync', 'cachebackup', 'cachedel', 'cachequery', 
			'minimalresponses', 'smartupdate', 'forward', 'edns', 'stub', 'dns64', 'rootconfig']

all_sbt = ['switch', 'rules', 'totalthreshold', 'ipv4totalthreshold', 'ipv6totalthreshold', 'ipthreshold', 'ipv4no53threshold', 'ipv6no53threshold','dnamethreshold', 'dnamelist', 
			'defaultthreshold', 'updatethreshold', 'ipv4nohitthreshold','ipv6nohitthreshold', 'replythreshold','x20', 'linkage', 'maxanswerlen', 'qpsthreshold', 'odds', 'redirectip', 
			'srcipblacklist', 'serviceipblacklist', 'domainblacklist', 'srcipgroup', 'domaingroup', 'dstipgroup', 'dnsqtype', 'gtldomain', 'forwardserver', 'dtsfilter', 'srciptrans', 
			'dstiptrans','iplist', 'dstiplist', 'domainlist', 'view', 'cacheqtype', 'noerrornoanswer', 'onlycname', 'nxdomain', 'viewdisable', 'srcipdisable', 'dstipdisable', 
			'domaindisable', 'globalbackup', 'globalimport', 'viewbackup', 'viewimport', 'viewmapping', 'rootconfig']


def switch_check(data):
	if len(data) == 1 and (data['switch'] == 'enable' or data['switch'] == 'disable'):
		return True
	return False


def is_ip(address):
	try:
		IPy.IP(address)
		return True
	except Exception as e:
		logger.error(str(e))
	return False


def iptables_rules_check(data):
	proto = ['icmp', 'udp', 'tcp']
	try:
		if len(data) != 9:
			return False
		if data['priority'] <= 0 or data['priority'] >= 65535:
			return False
		if data['action'] != 'accept' and data['action'] != 'drop':
			return False
		if data['proto'] not in proto:
			return False
		if is_ip(data['srcip']) == False or is_ip(data['destip']) == False:
			return False
		if data['srcportstart'] <= 0 or data['srcportstart'] >= 65535:
			return False
		if data['srcportend'] <= 0 or data['srcportend'] >= 65535:
			return False
		if data['destportstart'] <= 0 or data['destportstart'] >= 65535:
			return False
		if data['destportend'] <= 0 or data['destportend'] >= 65535:
			return False
		if data['srcportstart'] > data['srcportend'] or data['destportstart'] > data['destportend']:
			return False
		return True
	except Exception as e:
		logger.error(str(e))
	return False


def threshold_check(data):
	if len(data) == 1 and data['threshold'] >= 0 and data['threshold'] <= 0xffffffff:
		return True
	return False


def ip_threshold_check(data):
	if len(data) == 2 and is_ip(data['ip']) and data['threshold'] >= 0 and data['threshold'] <= 0xffffffff:
		return True
	return False


def is_domain(domain):
	pattern = re.compile(
    	r'^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|'
		r'([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|'
		r'([a-zA-Z0-9][-_.a-zA-Z0-9]{0,61}[a-zA-Z0-9]))\.'
		r'([a-zA-Z]{2,13}|[a-zA-Z0-9-]{2,30}.[a-zA-Z]{2,3})$'
	)
	if '*' == domain:
		return True
	elif '*.' in domain:
		if pattern.match(domain.split('*.')[-1]) is not None:
			return True
	elif pattern.match(domain) is not None:
		return True
	return False


def dname_threshold_check(data):
	if len(data) == 2 and is_domain(data['domain']) and data['threshold'] >= 0 and data['threshold'] <= 0xffffffff:
		return True
	return False
	

def domain_check(data):
	if len(data) == 1 and is_domain(data['dname']): 
		return True
	return False


def dnamelist_check(data):
	if len(data) == 2:
		if data['type'] == 'group' and len(data['dname']) > 0:
			return True
		elif data['type'] == 'dname' and is_domain(data['dname']):
			return True
	return False


def ip_dname_threshold_check(data):
	if len(data) == 3 and is_ip(data['ip']) and is_domain(data['domain']) and data['threshold'] > 0 and data['threshold'] < 0xffffffff:
		return True
	return False


def answer_len_check(data):
	if len(data) == 1 and data['maxlen'] > 0 and data['maxlen'] < 0xffff:
		return True
	return False


def action_check(action):
	actions = ['drop', 'refused', 'nxdomain', 'noanswer', 'ipv4', 'ipv6']
	if action in actions:
		return True
	return False


# answer后续可能需要根据action类型判断
def ip_control_check(data):
	if len(data) == 3 and is_ip(data['ip']) and action_check(data['action']) and (data['answer'] == '' or is_ip(data['answer'])):
		return True
	return False


def domain_control_check(data):
	if len(data) == 3 and is_domain(data['domain']) and action_check(data['action']) and (data['answer'] == '' or is_ip(data['answer'])):
		return True
	return False


def ip_domain_control_check(data):
	if len(data) == 4 and is_ip(data['ip']) and is_domain(data['domain']) and action_check(data['action']) and (data['answer'] == '' or is_ip(data['answer'])):
		return True
	return False


def is_qtype(q):
	#列出所有请求类型
	qtypes = ['a', 'aaaa', 'cname', 'ns', 'txt', 'any', 'ptr', 'soa', 'mx']
	if q in qtypes:
		return True
	return False


def domain_qtype_control_check(data):
	if len(data) == 4 and is_domain(data['domain']) and is_qtype(data['qtype']) and action_check(data['action']) and (data['answer'] == '' or is_ip(data['answer'])):
		return True
	return False


def qtype_control_check(data):
	if len(data) == 3 and is_qtype(data['qtype']) and action_check(data['action']) and (data['answer'] == '' or is_ip(data['answer'])):
		return True
	return False


def ip_qtype_control_check(data):
	if len(data) == 4 and is_ip(data['ip']) and is_qtype(data['qtype']) and action_check(data['action']) and (data['answer'] == '' or is_ip(data['answer'])):
		return True
	return False


def gray_domain_control_check(data):
	if len(data) == 2 and action_check(data['action']) and is_domain(data['domain']):
		return True
	return False


def odds_check(data):
	if len(data) == 1 and data['odds'] > 0 and data['odds'] < 16:
		return True
	return False


def redirect_ip_check(data):
	if len(data) == 2 and is_ip(data['ip']) and data['weight'] < 16 and data['weight'] > 0:
		return True
	return False


#不同请求类型对应不同类型的值
def is_answer(qtype,data):
	if 'a' == qtype and '.' in data and (is_ip(data) or is_domain(data)):
		return True
	elif 'aaaa' == qtype and ':' in data and (is_ip(data) or is_domain(data)):
		return True
	elif 'cname' == qtype and is_domain(data):
		return True
	elif 'mx' == qtype:
		mx = data.split('@')
		if int(mx[0]) > 0 and is_domain(mx[1]):
			return True
	elif 'srv' == qtype:
		srv = data.split('@')
		if int(srv[0]) > 0 and int(srv[1]) > 0 and int(srv[2]) > 0 and int(srv[2]) < 65535 and is_domain(srv[3]):
			return True
	elif 'naptr' == qtype:
		ptr = data.split('@')
		#待补充
		#if int(ptr[0]) >i= 0 and int(ptr[1]) > 0 and ptr[2] == 's' and ptr[3] == 'sip+d2u' and ptr[4] == 'regexp' and is_domain(ptr[5]):
		return True
	return False


def dname_protect_check(data):
	action = ['alarm', 'delete', 'backup']
	if len(data) == 5 and is_domain(data['domain']) and is_qtype(data['qtype']) and data['action'] in action and \
	is_answer(data['qtype'],data['answer']) and (len(data['backup']) == 0 or is_answer(data['qtype'],data['backup'])):
		return True
	return False


def ip_check(data):
	if len(data) == 1 and is_ip(data['ip']):
		return True
	return False


def dname_check(data):
	if len(data) == 1 and is_domain(data['domain']):
		return True
	return False


def view_switch_check(data):
	if len(data) == 2 and view_exist(data['view']) and (data['switch'] == 'enable' or data['switch'] == 'disable'):
		return True
	return False


def view_redirect_ip_check(data):
	if len(data) == 3 and view_exist(data['view']) and is_ip(data['ip']) and data['weight'] < 16 and data['weight'] > 0:
		return True
	return False


def sortlist_rules_check(data):
	# 需要判断sortlist数据
	if len(data) == 3 and view_exist(data['view']) and is_domain(data['domain']) and len(data['sortlist']) > 0:
		return True
	return False


def ip_group_check(data):
	if len(data) == 2 and len(data['groupname']) > 0 and is_ip(data['ip']):
		return True
	return False


def domain_group_check(data):
	if len(data) == 2 and len(data['groupname']) > 0 and is_domain(data['domain']):
		return True
	return False


def dts_qtype_check(data):
	if len(data) == 1 and is_qtype(data['qtype']):
		return True
	return False


def dts_tld_check(data):
	if len(data) == 1 and is_tld(data['gtld']):
		return True
	return False


def dts_forward_server_check(data):
	if len(data) == 3 and len(data['servergroup']) > 0 and is_ip(data['ip']) and data['weight'] < 16 and data['weight'] > 0:
		return True
	return False


def dts_filter_check(data):
	if len(data) != 9:
		return False
	try:
		if len(data['filtername']) <= 0 or len(data['srcgroup']) <= 0 or len(data['dstgroup']) <= 0 or len(data['domaingroup']) <= 0:
			return False
		if data['type'] != 'drop' and data['type'] != 'forward' and data['type'] != 'stat':
			return False
		if data['gtld'] != 'and' and data['gtld'] != 'not' and data['gtld'] != 'null':
			return False
		if data['creditdname'] != 'and' and data['creditdname'] != 'not' and data['creditdname'] != 'null':
			return False
		if data['rd'] != 'and' and data['rd'] != 'not' and data['rd'] != 'null':
			return False
		if data['type'] == 'forward':
			if data['forward'] < 0:
				return False
		elif data['forward'] != 0:
				return False
		return True
	except Exception as e:
		return False


def acl_ip_check(data):
	if len(data) == 2 and len(data['ipgroup']) > 0 and is_ip(data['ip']):
		return True
	return False


def acl_domain_check(data):
	if len(data) == 2 and len(data['domaingroup']) > 0 and is_domain(data['domain']):
		return True
	return False


def view_check(data):
	if len(data) == 5 and len(data['viewname']) > 0 and src_ip_group_exist(data['srcipgroup']) and dst_ip_group_exist(data['dstipgroup']) and domain_group_exist(data['domaingroup']) \
	and (data['rd'] == 'set' or data['rd'] == 'unset' or data['rd'] == 'null'):
		return True
	return False


def cache_qtype_check(data):
	if len(data) == 2 and view_exist(data['view']) and is_qtype(data['qtype']):
		return True
	return False


def ttl_rules_check(data):
	if len(data) == 4 and view_exist(data['view']) and is_domain(data['domain']) and data['minttl'] > 0 and data['maxttl'] > 0 and data['maxttl'] > data['minttl']:
		return True
	return False


# 待实现 根据不同类型对应不同的值
def is_dns_answer(qtype,answer):
	return True

	
#后续实现
def rrset_rules_check(data):
	if len(data) == 6 and view_exist(data['view']) and is_domain(data['domain']) and is_qtype(data['qtype']) and data['ttl'] > 0 and data['weight'] > 0 and is_dns_answer(data['qtype'],data['answer']): 
		return True
	return False


def view_ip_check(data):
	if len(data) == 2 and view_exist(data['view']) and is_ip(data['ip']): 
		return True
	return False


def rrfilter_rules_check(data):
	if len(data) == 4 and view_exist(data['view']) and is_domain(data['domain']) and is_qtype(data['qtype']) and is_answer(data['qtype'],data['answer']): 
		return True
	return False


def dns_domain_check(data):
	if len(data) == 1 and is_domain(data['domain']): 
		return True
	return False


def view_domain_check(data):
	if len(data) == 2 and view_exist(data['view']) and is_domain(data['domain']): 
		return True
	return False


def view_ip_domain_check(data):
	if len(data) == 3 and view_exist(data['view']) and is_domain(data['domain']) and is_ip(data['ip']): 
		return True
	return False


def backup_file_check(data):
	if len(data) == 1 and len(data['file']) >= 0:
		return True
	return False


def import_file_check(data):
	if len(data) == 1 and len(data['file']) > 0:
		return True
	return False


def file_view_check(data):
	if len(data) == 2 and view_exist(data['view']) and len(data['file']) > 0: 
		return True
	return False


def view_domain_qtype_check(data):
	if len(data) == 3 and view_exist(data['view']) and is_domain(data['domain']) and is_qtype(data['qtype']): 
		return True
	return False


def forward_server_check(data):
	if len(data) == 4 and view_exist(data['view']) and len(data['servergroup']) > 0 and is_ip(data['ip']) and data['weight'] < 16 and data['weight'] > 0: 
		return True
	return False


def forward_rules_check(data):
	if len(data) == 5 and view_exist(data['view']) and is_domain(data['domain']) and len(data['servergroup']) > 0 and (data['type'] == 'first' or data['type'] == 'only')\
	and (data['action'] == 'merge' or data['action'] == 'normal'):
		return True
	return False


def stub_rules_check(data):
	if len(data) == 5 and view_exist(data['view']) and is_domain(data['domain']) and data['ttl'] > 0 and (len(data['ns']) == 0 or is_domain(data['ns'])) and (len(data['ip']) == 0 or is_ip(data['ip'])):
		return True
	return False


def dns64_rules_check(data):
	if len(data) == 3 and view_exist(data['view']) and is_domain(data['domain']) and is_ip(data['ipv6prefix']):
		return True
	return False
		


data_check_methods = {
	'iptables': {
		'switch': switch_check,
		'rules': iptables_rules_check
	},
	'dnsipfragment': {
		'switch': switch_check
	},
	'ipfragment': {
		'switch': switch_check
	},
	'icmpflood': {
		'switch': switch_check,
		'ipv4totalthreshold': threshold_check,
		'ipv6totalthreshold': threshold_check,
		'ipthreshold': ip_threshold_check
	},
	'tcpflood': {
		'switch': switch_check,
		'ipv4totalthreshold': threshold_check,
		'ipv6totalthreshold': threshold_check,
		'ipthreshold': ip_threshold_check,
		'ipv4no53threshold': threshold_check,
		'ipv6no53threshold': threshold_check
	},
	'udpflood': {
		'ipv4no53threshold': threshold_check,
		'ipv6no53threshold': threshold_check
	},
	'creditdname': {
		'switch': switch_check,
		'totalthreshold': threshold_check,
		'dnamethreshold': dname_threshold_check,
		'dnamelist' : domain_check
	},
	'ipthreshold': {
		'switch': switch_check,
		'rules': ip_threshold_check,
		'defaultthreshold': threshold_check 
	},
	'domainthreshold': {
		'switch': switch_check,
		'rules': dname_threshold_check
	},
	'ipdomainthreshold': {
		'switch': switch_check,
		'rules': ip_dname_threshold_check
	},
	'backendthreshold': {
		'updatethreshold': threshold_check,
		'ipv4nohitthreshold': threshold_check,
		'ipv6nohitthreshold': threshold_check,
		'dnamethreshold': dname_threshold_check
	},
	'replythreshold': {
		'replythreshold': threshold_check
	},
	'poisonprotect': {
		'switch': switch_check,
		'linkage': switch_check,
		'x20': switch_check
	},
	'amplificationattack': {
		'switch': switch_check,
		'maxanswerlen': answer_len_check,
		'qpsThreshold': threshold_check
	},
	'useripwhitelist': {
		'switch': switch_check,
		'rules': ip_check
	},
	'serviceipwhitelist': {
		'switch': switch_check,
		'rules': ip_check
	},
	'srcipaccesscontrol': {
		'switch': switch_check,
		'rules': ip_control_check
	},
	'domainaccesscontrol': {
		'switch': switch_check,
		'rules': domain_control_check
	},
	'ipdomainaccesscontrol': {
		'switch': switch_check,
		'rules': ip_domain_control_check
	},
	'domainqtypeaccesscontrol': {
		'switch': switch_check,
		'rules': domain_qtype_control_check
	},
	'qtypeaccesscontrol': {
		'switch': switch_check,
		'rules': qtype_control_check
	},
	'ipqtypeaccesscontrol': {
		'switch': switch_check,
		'rules': ip_qtype_control_check
	},
	'graydomainaccesscontrol': {
		'switch': switch_check,
		'rules': gray_domain_control_check,
		'odds': odds_check,
		'redirectip': redirect_ip_check
	},
	'importdnameprotect': {
		'switch': switch_check,
		'rules': dname_protect_check
	},
	'spreadecho': {
		'switch': switch_check,
		'srcipblacklist': ip_check,
		'serviceipblacklist': ip_check,
		'domainblacklist': dname_check
	},
	'nxr': {
		'switch': view_switch_check,
		'redirectip': view_redirect_ip_check,
		'domainblacklist': dname_check,
		'srcipblacklist': ip_check
	},
	'sortlist': {
		'switch': view_switch_check,
		'rules': sortlist_rules_check
	},
	'dts': {
		'switch': switch_check,
		'srcipgroup': ip_group_check,
		'domaingroup': domain_group_check,
		'dstipgroup': ip_group_check,
		'dnsqtype' : dts_qtype_check,
		'gtldomain': dts_tld_check,
		'forwardserver': dts_forward_server_check,
		'dtsfilter': dts_filter_check
	},
	'iptrans': {
		'srciptrans': ip_check,
		'dstiptrans': ip_check
	},
	'acl': {
		'iplist': acl_ip_check,
		'dstiplist': ip_group_check,
		'domainlist': acl_domain_check
	},
	'view': {
		'view': view_check
	},
	'selfcheck': {
		'cacheqtype': cache_qtype_check, 
		'noerrornoanswer': view_switch_check,
		'nxdomain': view_switch_check,
		'onlycname': view_switch_check
	},
	'ttl': {
		'switch': view_switch_check,
		'rules': ttl_rules_check
	},
	'rrset': {
		'switch': view_switch_check,
		'rules': rrset_rules_check,
		'srcipblacklist': view_ip_check
	},
	'rrfilter': {
		'switch': view_switch_check,
		'rules': rrfilter_rules_check
	},
	'expiredactivate': {
		'switch': switch_check
	},
	'cachedisable': {
		'switch': switch_check,
		'viewdisable': view_switch_check,
		'srcipdisable': ip_check,
		'dstipdisable': ip_check,
		'domaindisable': dns_domain_check,
		'domainblacklist': dns_domain_check
	},
	'cachesync': {
		'switch': switch_check
	},
	'cachebackup': {
		'globalbackup': backup_file_check,
		'globalimport': import_file_check,
		'viewbackup': file_view_check,
		'viewimport': file_view_check
	},
	'cachedel': {
		'rules': view_domain_qtype_check
	},
	'cachequery': {
		'rules': view_domain_qtype_check
	},
	'minimalresponses': {
		'switch': switch_check
	},	
	'smartupdate': {
		'switch': switch_check
	},	
	'forward': {
		'switch': view_switch_check,
		'forwardserver': forward_server_check,
		'srcipblacklist': view_ip_check,
		'domainblacklist': view_domain_check,
		'rules': forward_rules_check
	},	
	'edns': {
		'switch': view_switch_check,
		'viewmapping': view_ip_check,
		'rules': view_domain_check
	},	
	'stub': {
		'switch': view_switch_check,
		'rules': stub_rules_check
	},	
	'dns64': {
		'switch': view_switch_check,
		'rules': dns64_rules_check
	},
	'rootconfig': {
		'rootconfig': stub_rules_check
	}
}


#合法性校验 {"source":"ms","id":100,"bt":"xxx","sbt":"xxx","op":"update","data":{"switch":"enable"}}
def check_data(data,method):
	try:
		if len(data) != 6:
			return False
		if data['bt'] not in all_bt:
			return False
		if data['sbt'] not in all_sbt:
			return False
		if data['source'] != 'ms' and data['source'] != 'cli':
			return False
		if method == 'POST':
			if data['op'] != 'add':
				return False
			if data['id'] < 0:
				return False
			if data_check_methods[data['bt']][data['sbt']](data['data']) is False:
				return False
		elif method == 'PUT':
			if data['op'] != 'update':
				return False
			if data['id'] < 0:
				return False
			if data_check_methods[data['bt']][data['sbt']](data['data']) is False:
				return False
		elif method == 'DELETE':
			if data['id'] < 0:
				return False
			if data['op'] == 'delete':
				if data_check_methods[data['bt']][data['sbt']](data['data']) is False:
					return False
			elif data['op'] == 'clear':
				pass
			else:
				return False
		elif method == 'GET':
			if data['op'] != 'query':
				return False
			'''
			if len(data['data']) != 0:
				if data_check_methods[data['bt']][data['sbt']](data['data']) is False:
					return False
			'''
		return True
	except Exception as e:
		logger.error(str(e))

	return False		


