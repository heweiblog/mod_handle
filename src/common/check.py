#!/usr/bin/python3
# -*- coding: utf-8 -*-

from dns.rdatatype import _by_text as rr_type
import json,IPy,re
from common.log import logger
from models import db,view,acl,dts,bind,iptables,ip


dns_bt = ['iptables', 'dnsipfragment', 'ipfragment', 'icmpflood', 'tcpflood', 'udpflood', 'creditdname', 'ipthreshold', 'domainthreshold', 'ipdomainthreshold', 'backendthreshold',
			'replythreshold', 'poisonprotect', 'amplificationattack', 'useripwhitelist', 'serviceipwhitelist', 'srcipaccesscontrol', 'domainaccesscontrol', 'ipdomainaccesscontrol', 
			'domainqtypeaccesscontrol','qtypeaccesscontrol', 'ipqtypeaccesscontrol', 'graydomainaccesscontrol', 'importdnameprotect', 'spreadecho', 'nxr', 'sortlist', 'dts', 'iptrans', 
			'acl', 'view', 'selfcheck', 'ttl', 'rrset', 'rrfilter', 'expiredactivate', 'cachedisable', 'cachesync', 'minimalresponses', 'smartupdate', 'forward', 'edns', 'stub', 'dns64', 
			'rootconfig', 'accesscontrolanswerip']

dns_sbt = ['switch', 'rules', 'totalthreshold', 'ipv4totalthreshold', 'ipv6totalthreshold', 'ipthreshold', 'ipv4no53threshold', 'ipv6no53threshold','dnamethreshold', 'dnamelist', 
			'defaultthreshold', 'updatethreshold', 'ipv4nohitthreshold','ipv6nohitthreshold', 'replythreshold','x20', 'linkage', 'maxanswerlen', 'qpsthreshold', 'odds', 'redirectip', 
			'srcipblacklist', 'serviceipblacklist', 'domainblacklist', 'srcipgroup', 'domaingroup', 'dstipgroup', 'dnsqtype', 'gtldomain', 'forwardserver', 'dtsfilter', 'srciptrans', 
			'dstiptrans','iplist', 'dstiplist', 'domainlist', 'view', 'cacheqtype', 'noerrornoanswer', 'onlycname', 'nxdomain', 'viewdisable', 'srcipdisable', 'dstipdisable', 
			'domaindisable', 'viewimport', 'viewmapping', 'rootconfig', 'ipv4', 'ipv6']

handle_bt = ['useripwhitelist', 'ipthreshold', 'handlethreshold', 'srcipaccesscontrol', 'handleaccesscontrol', 'backend', 'businessservice', 'businessproto', 'certificate', 'selfcheck', 
			'xforce', 'cachesmartupdate', 'cacheprefetch', 'backendmeter', 'stub'] 

handle_sbt = ['switch', 'rules', 'forwardserver']


#所有请求类型
qtypes = json.loads(json.dumps(rr_type).lower())


def switch_check(op,data):
	if op == 'update' or op == 'add':
		if len(data) != 1:
			return 'data feild num error'
		if data['switch'] != 'enable' and data['switch'] != 'disable':
			return 'switch format error'
		return 'true'	
	elif op == 'delete':
		return 'done'	
	elif op == 'query':
		return 'true'	
	return 'unsupported operations'


def is_ip(address):
	try:
		IPy.IP(address)
		return True
	except Exception as e:
		logger.error(str(e))
	return False


def iptables_rules_check(op,data):
	proto = ['icmp', 'udp', 'tcp']
	#if op == 'add' or op == 'update' or op == 'delete':
	if op == 'add' or op == 'delete':
		if len(data) != 9:
			return 'data feild num error'
		if data['priority'] < 0 or data['priority'] > 65535:
			return 'priority value range error'
		if op == 'add' and iptables.check_iptables_priority(data['priority']):
			return 'duplicate priority'
		if data['action'] != 'accept' and data['action'] != 'drop':
			return 'action format error'
		if data['proto'] not in proto:
			return 'proto format error'
		if '/' not in data['srcip'] or is_ip(data['srcip']) == False:
			return 'srcIp {} format error'.format(data['srcip'])
		if '/' not in data['destip'] or is_ip(data['destip']) == False:
			return 'destIp {} format error'.format(data['destip'])
		if data['srcportstart'] <= 0 or data['srcportstart'] >= 65535:
			return 'srcPortStart value range error'
		if data['srcportend'] <= 0 or data['srcportend'] >= 65535:
			return 'srcPortEnd value range error'
		if data['destportstart'] <= 0 or data['destportstart'] >= 65535:
			return 'destPortEnd value range error'
		if data['destportend'] <= 0 or data['destportend'] >= 65535:
			return 'destPortEnd value range error'
		if data['srcportstart'] > data['srcportend'] or data['destportstart'] > data['destportend']:
			return 'port start must less than end'
		return 'true'
	elif op == 'query' or op == 'clear':
		return 'true'
	return 'unsupported operations'


def threshold_check(op,data):
	if op == 'update' or op == 'add':
		if len(data) != 1:
			return 'data feild num error'
		if data['threshold'] < 0 or data['threshold'] > 0xffffffff:
			return 'threshold value range error'
		return 'true'	
	elif op == 'delete':
		return 'done'	
	elif op == 'query':
		return 'true'	
	return 'unsupported operations'


def ip_threshold_check(op,data):
	if op == 'add' or op == 'update' or op == 'delete':
		if len(data) != 2:
			return 'data feild num error'
		if '/' not in data['ip'] or is_ip(data['ip']) is not True:
			return 'ip {} format error'.format(data['ip'])
		if data['threshold'] < 0 or data['threshold'] > 0xffffffff:
			return 'threshold value range error'
		return 'true'	
	elif op == 'query' or op == 'clear':
		return 'true'
	return 'unsupported operations'


def is_domain_tag(t):
	if t == '*':
		return True
	elif len(t) > 0:
		r = re.match(r'[0-9a-zd_d-]{0,63}',t)
		if r is not None and r.span()[1] == len(t):
			return True
	return False


def is_domain(domain):
	if len(domain) > 253:
		return False
	if '--' in domain or '__' in domain:
		return False
	if '-' == domain[:1] or '-' == domain[-1:]:
		return False

	l = domain.split('.')
	if len(l) == 1:
		if '-' in domain or '_' in domain:
			return False
		if is_domain_tag(domain):
			return True
	elif len(l) > 1:
		if '-' in l[-1] or '_' in l[-1]:
			return False
		for i in l:
			if is_domain_tag(i) is False:
				return False
		return True
	return False


def dname_threshold_check(op,data):
	if op == 'add' or op == 'update':
		if len(data) != 2:
			return 'data feild num error'
		if is_domain(data['domain']) is not True:
			return 'domain {} format error'.format(data['domain'])
		if data['threshold'] < 0 or data['threshold'] > 0xffffffff:
			return 'threshold value range error'
		return 'true'	
	elif op == 'query' or op == 'clear' or op == 'delete':
		return 'true'
	return 'unsupported operations'
	

def domain_check(op,data):
	if op == 'add' or op == 'delete':
		if len(data) != 1:
			return 'data feild num error'
		if is_domain(data['dname']) is not True:	
			return 'dname {} format error'.format(data['dname'])
		return 'true'	
	elif op == 'query' or op == 'clear':
		return 'true'
	return 'unsupported operations'


def ip_dname_threshold_check(op,data):
	if op == 'add' or op == 'update' or op == 'delete':
		if len(data) != 3:
			return 'data feild num error'
		if '/' not in data['ip'] or is_ip(data['ip']) is not True:
			return 'ip {} format error'.format(data['ip'])
		if is_domain(data['domain']) is not True:
			return 'domain {} format error'.format(data['domain'])
		if data['threshold'] < 0 or data['threshold'] > 0xffffffff:
			return 'threshold value range error'
		return 'true'	
	elif op == 'query' or op == 'clear':
		return 'true'
	return 'unsupported operations'


def answer_len_check(op,data):
	if op == 'update' or op == 'add':
		if len(data) != 1:
			return 'data feild num error'
		elif data['maxlen'] < 0 or data['maxlen'] > 0xffff:
			return 'maxlen value range error'
		return 'true'	
	elif op == 'delete':
		return 'done'	
	elif op == 'query':
		return 'true'
	return 'unsupported operations'


def action_check(action):
	actions = ['drop', 'refused', 'nxdomain', 'noanswer', 'ip']
	if action not in actions:
		return 'unsupported action'
	return 'true'	


def ip_control_check(op,data):
	if op == 'add' or op == 'update' or op == 'delete':
		if len(data) != 2:
			return 'data feild num error'
		if '/' not in data['ip'] or is_ip(data['ip']) is not True:
			return 'ip {} format error'.format(data['ip'])
		return action_check(data['action'])
	elif op == 'query' or op == 'clear':
		return 'true'
	return 'unsupported operations'
				

def domain_control_check(op,data):
	if op == 'add' or op == 'update' or op == 'delete':
		if len(data) != 2:
			return 'data feild num error'
		if is_domain(data['domain']) is not True:
			return 'domain {} format error'.format(data['domain'])
		return action_check(data['action'])
	elif op == 'query' or op == 'clear':
		return 'true'
	return 'unsupported operations'
				


def ip_domain_control_check(op,data):
	if op == 'add' or op == 'update' or op == 'delete':
		if len(data) != 3:
			return 'data feild num error'
		if '/' not in data['ip'] or is_ip(data['ip']) is not True:
			return 'ip {} format error'.format(data['ip'])
		if is_domain(data['domain']) is not True:
			return 'domain {} format error'.format(data['domain'])
		return action_check(data['action'])
	elif op == 'query' or op == 'clear':
		return 'true'
	return 'unsupported operations'


def is_qtype(q):
	if q in qtypes:
		return True
	return False


def domain_qtype_control_check(op,data):
	if op == 'add' or op == 'update' or op == 'delete':
		if len(data) != 3:
			return 'data feild num error'
		if is_qtype(data['qtype']) is not True:
			return 'qtype format error'
		if is_domain(data['domain']) is not True:
			return 'domain {} format error'.format(data['domain'])
		return action_check(data['action'])
	elif op == 'query' or op == 'clear':
		return 'true'
	return 'unsupported operations'


def qtype_control_check(op,data):
	if op == 'add' or op == 'update' or op == 'delete':
		if len(data) != 2:
			return 'data feild num error'
		if is_qtype(data['qtype']) is not True:
			return 'qtype format error'
		return action_check(data['action'])
	elif op == 'query' or op == 'clear':
		return 'true'
	return 'unsupported operations'


def ip_qtype_control_check(op,data):
	if op == 'add' or op == 'update' or op == 'delete':
		if len(data) != 3:
			return 'data feild num error'
		if is_qtype(data['qtype']) is not True:
			return 'qtype format error'
		if '/' not in data['ip'] or is_ip(data['ip']) is not True:
			return 'ip {} format error'.format(data['ip'])
		return action_check(data['action'])
	elif op == 'query' or op == 'clear':
		return 'true'
	return 'unsupported operations'


def gray_domain_control_check(op,data):
	actions = ['drop', 'refused', 'nxdomain', 'noanswer']
	if op == 'add' or op == 'update' or op == 'delete':
		if len(data) != 2:
			return 'data feild num error'
		if is_domain(data['domain']) is not True:
			return 'domain {} format error'.format(data['domain'])
		if data['action'] not in actions:
			'unsupported action'
		return 'true'
	elif op == 'query' or op == 'clear':
		return 'true'
	return 'unsupported operations'


def odds_check(op,data):
	if op == 'update' or op == 'add':
		if len(data) != 1:
			return 'data feild num error'
		if data['odds'] <= 0 or data['odds'] >= 16:
			return 'odds value range error'
		return 'true'
	elif op == 'delete':
		return 'done'	
	elif op == 'query':
		return 'true'
	return 'unsupported operations'


def redirect_ip_check(op,data):
	if op == 'add' or op == 'update' or op == 'delete':
		if len(data) != 2:
			return 'data feild num error'
		if '/' in data['ip'] or is_ip(data['ip']) is not True:
			return 'ip {} format error'.format(data['ip'])
		if data['weight'] <= 0 or data['weight'] >= 16:
			return 'weight value range error'
		return 'true'
	elif op == 'query' or op == 'clear':
		return 'true'
	return 'unsupported operations'



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
		if int(mx[0]) > 0 and int(mx[0]) <= 30 and is_domain(mx[1]):
			return True
	elif 'srv' == qtype:
		srv = data.split('@')
		if int(srv[0]) > 0 and int(srv[0]) <= 0xffff and int(srv[1]) > 0 and int(srv[1]) <= 0xffff and int(srv[2]) > 0 and int(srv[2]) <= 0xffff and is_domain(srv[3]):
			return True
	elif 'naptr' == qtype:
		ptr = data.split('@')
		if int(ptr[0]) > 0 and int(ptr[0]) <= 0xffff and int(ptr[1]) > 0 and int(ptr[1]) <= 0xffff and len(ptr[2]) == 1 and (ptr[2].isalpha() or ptr[2].isdigit()) \
		and len(ptr[3]) > 0 and len(ptr[3]) <= 80 and len(ptr[4]) > 0 and len(ptr[4]) <= 80  and is_domain(ptr[5]):
			return True
	return False


def dname_protect_check(op,data):
	action = ['alarm', 'delete', 'backup']
	if op == 'add' or op == 'update' or op == 'delete':
		if len(data) != 5:
			return 'data feild num error'
		if is_domain(data['domain']) is not True:
			return 'domain {} format error'.format(data['domain'])
		if is_qtype(data['qtype']) is not True:
			return 'qtype format error'
		if data['action'] not in action:
			return 'unsupported action'
		if is_answer(data['qtype'],data['answer']) is not True:
			return 'answer format error'
		if len(data['backup']) != 0 and is_answer(data['qtype'],data['backup']) == False:
			return 'backup format error'
		return 'true'
	elif op == 'query' or op == 'clear':
		return 'true'
	return 'unsupported operations'


def ip_check(op,data):
	if op == 'add' or op == 'delete':
		if len(data) != 1:
			return 'data feild num error'
		if '/' in data['ip'] or is_ip(data['ip']) is not True:
			return 'ip {} format error'.format(data['ip'])
		return 'true'
	elif op == 'query' or op == 'clear':
		return 'true'
	return 'unsupported operations'


def ip_sec_check(op,data):
	if op == 'add' or op == 'delete':
		if len(data) != 1:
			return 'data feild num error'
		if '/' not in data['ip'] or is_ip(data['ip']) is not True:
			return 'ip {} format error'.format(data['ip'])
		return 'true'
	elif op == 'query' or op == 'clear':
		return 'true'
	return 'unsupported operations'


def ipv4_check(op,data):
	if op == 'update':
		if len(data) != 1:
			return 'data feild num error'
		if '.' not in data['ip'] or '/' in data['ip'] or is_ip(data['ip']) is not True:
			return 'ip {} format error'.format(data['ip'])
		return 'true'
	elif op == 'query' or op == 'delete':
		return 'true'
	return 'unsupported operations'


def ipv6_check(op,data):
	if op == 'update':
		if len(data) != 1:
			return 'data feild num error'
		if ':' not in data['ip'] or '/' in data['ip'] or is_ip(data['ip']) is not True:
			return 'ip {} format error'.format(data['ip'])
		return 'true'
	elif op == 'query' or op == 'delete':
		return 'true'
	return 'unsupported operations'


def dname_check(op,data):
	if op == 'add' or op == 'delete':
		if len(data) != 1:
			return 'data feild num error'
		if is_domain(data['domain']) is not True:
			return 'domain {} format error'.format(data['domain'])
		return 'true'
	elif op == 'query' or op == 'clear':
		return 'true'
	return 'unsupported operations'


def view_switch_check(op,data):
	if op == 'update':
		if len(data) != 2:
			return 'data feild num error'
		if view.view_exist(data['view']) is not True:
			return 'view not exist'
		if data['switch'] != 'enable' and data['switch'] != 'disable':
			return 'switch format error'
		return 'true'
	elif op == 'query':
		return 'true'
	return 'unsupported operations'


def view_redirect_ip_check(op,data):
	if op == 'add' or op == 'update' or op == 'delete':
		if len(data) != 3:
			return 'data feild num error'
		if '/' in data['ip'] or is_ip(data['ip']) is not True:
			return 'ip {} format error'.format(data['ip'])
		if data['weight'] <= 0 or data['weight'] >= 16:
			return 'weight value range error'
		if op == 'delete':
			if len(data['view']) == 0:
				return 'view format error'
		else:
			if view.view_exist(data['view']) is not True:
				return 'view not exist'
		return 'true'
	elif op == 'query' or op == 'clear':
		return 'true'
	return 'unsupported operations'


def sortlist_rules_check(op,data):
	if op == 'add' or op == 'update':
		if len(data) != 3:
			return 'data feild num error'
		if is_domain(data['domain']) is not True:
			return 'domain {} format error'.format(data['domain'])
		if view.view_exist(data['view']) is not True:
			return 'view not exist'
		for l in data['sortlist']:
			for i in l:
				if acl.src_ip_group_exist(i) is False:
					return 'sortlist acl ip list Not Exist'
		return 'true'
	elif op == 'delete':
		if len(data['view']) == 0:
			return 'view format error'
		if is_domain(data['domain']) is not True:
			return 'domain {} format error'.format(data['domain'])
		return 'true'
	elif op == 'query' or op == 'clear':
		return 'true'
	return 'unsupported operations'


def dts_src_ip_group_check(op,data):
	if op == 'add': 
		if len(data) != 2:
			return 'data feild num error'
		if len(data['groupname']) == 0 or len(data['groupname']) > 80:
			return 'groupName format error'
		if '/' not in data['ip'] or is_ip(data['ip']) is not True:
			return 'ip {} format error'.format(data['ip'])
		return 'true'
	elif op == 'delete': 
		if len(data) != 2:
			return 'data feild num error'
		if len(data['groupname']) == 0:
			return 'groupName format error'
		if is_ip(data['ip']) is not True:
			return 'ip {} format error'.format(data['ip'])
		if dts.get_dts_src_ip_group_num(data['groupname']) == 1 and dts.dts_src_ip_group_judge(data['groupname']): 
			return 'the group referenced can not delete'
		return 'true'
	elif op == 'clear':
		#先查询所有的组 再看组有没有被引用 有引用则不能清除
		if dts.dts_src_ip_group_clear_judge() is False:
			return 'there are group referenced can not delete'
		return 'true'
	elif op == 'query':
		return 'true'
	return 'unsupported operations'


def dts_dst_ip_group_check(op,data):
	if op == 'add': 
		if len(data) != 2:
			return 'data feild num error'
		if len(data['groupname']) == 0 or len(data['groupname']) > 80:
			return 'groupName format error'
		if '/' not in data['ip'] or is_ip(data['ip']) is not True:
			return 'ip {} format error'.format(data['ip'])
		return 'true'
	elif op == 'delete': 
		if len(data) != 2:
			return 'data feild num error'
		if len(data['groupname']) == 0:
			return 'groupName format error'
		if is_ip(data['ip']) is not True:
			return 'ip {} format error'.format(data['ip'])
		if dts.get_dts_dst_ip_group_num(data['groupname']) == 1 and dts.dts_dst_ip_group_judge(data['groupname']): 
			return 'the group referenced can not delete'
		return 'true'
	elif op == 'clear':
		if dts.dts_dst_ip_group_clear_judge() is False:
			return 'there are group referenced can not delete'
		return 'true'
	elif op == 'query':
		return 'true'
	return 'unsupported operations'


def dts_domain_group_check(op,data):
	if op == 'add': 
		if len(data) != 2:
			return 'data feild num error'
		if len(data['groupname']) == 0 or len(data['groupname']) > 80:
			return 'groupName format error'
		if is_domain(data['domain']) is not True:
			return 'domain {} format error'.format(data['domain'])
		return 'true'
	elif op == 'delete': 
		if len(data) != 2:
			return 'data feild num error'
		if len(data['groupname']) == 0:
			return 'groupName format error'
		if is_domain(data['domain']) is not True:
			return 'domain {} format error'.format(data['domain'])
		if dts.get_dts_domain_group_num(data['groupname']) == 1 and dts.dts_domain_group_judge(data['groupname']): 
			return 'the group referenced can not delete'
		return 'true'
	elif op == 'clear':
		if dts.dts_domain_group_clear_judge() is False:
			return 'there are group referenced can not delete'
		return 'true'
	elif op == 'query':
		return 'true'
	return 'unsupported operations'


def dts_qtype_check(op,data):
	if op == 'add' or op == 'delete': 
		if len(data) != 1:
			return 'data feild num error'
		if is_qtype(data['qtype']) is not True:
			return 'unsupported qtype'
		return 'true'
	elif op == 'query' or op == 'clear':
		return 'true'
	return 'unsupported operations'


def is_tld(t):
	if len(t) > 0:
		r = re.match(r'[0-9a-z]{0,63}',t)
		if r is not None and r.span()[1] == len(t):
			return True
	return False


def dts_tld_check(op,data):
	if op == 'add' or op == 'delete': 
		if len(data) != 1:
			return 'data feild num error'
		if is_tld(data['gtld']) is False:
			return 'tld error'
		return 'true'
	elif op == 'query' or op == 'clear':
		return 'true'
	return 'unsupported operations'


def dts_forward_server_check(op,data):
	if op == 'add' or op == 'update' or op == 'delete':
		if len(data) != 3:
			return 'data feild num error'
		if len(data['servergroup']) == 0 or len(data['servergroup']) > 80:
			return 'servergroup format error'
		if '/' in data['ip'] or is_ip(data['ip']) is not True:
			return 'ip {} format error'.format(data['ip'])
		if data['weight'] <= 0 or data['weight'] >= 16:
			return 'weight value range error'
		return 'true'
	elif op == 'query' or op == 'clear':
		return 'true'
	return 'unsupported operations'


def dts_filter_check(op,data):
	if op == 'add' or op == 'update' or op == 'delete':
		if len(data) != 9:
			return 'data feild num error'
		if len(data['filtername']) == 0 or len(data['filtername']) > 80:
			return 'filtername format error'
		if op == 'delete':
			if len(data['srcgroup']) == 0:
				return 'srcgroup format error'
			if len(data['dstgroup']) == 0:
				return 'srcgroup format error'
			if len(data['domaingroup']) == 0:
				return 'srcgroup format error'
		else:
			if dts.dts_src_ip_group_exist(data['srcgroup']) is False:
				return 'srcgroup not exist'
			if dts.dts_dst_ip_group_exist(data['dstgroup']) is False:
				return 'dstgroup not exist'
			if dts.dts_domain_group_exist(data['domaingroup']) is False:
				return 'domaingroup not exist'
		if data['type'] != 'drop' and data['type'] != 'forward' and data['type'] != 'stat':
			return 'type format error'
		if data['gtld'] != 'and' and data['gtld'] != 'not' and data['gtld'] != 'null':
			return 'gtld format error'
		if data['creditdname'] != 'and' and data['creditdname'] != 'not' and data['creditdname'] != 'null':
			return 'creditname format error'
		if data['rd'] != 'and' and data['rd'] != 'not' and data['rd'] != 'null':
			return 'rd format error'
		if data['type'] == 'forward':
			if data['forward'] <= 0 or data['forward'] > 0xffff:
				return 'forward value error'
		else:
			if data['forward'] != 0:
				return 'forward value error'
		return 'true'
	elif op == 'query' or op == 'clear':
		return 'true'
	return 'unsupported operations'


def acl_src_ip_group_check(op,data):
	if op == 'add': 
		if len(data) != 2:
			return 'data feild num error'
		if len(data['ipgroup']) == 0 or len(data['ipgroup']) > 80:
			return 'groupName format error'
		if '/' not in data['ip'] or is_ip(data['ip']) is not True:
			return 'ip {} format error'.format(data['ip'])
		return 'true'
	elif op == 'delete': 
		if len(data) != 2:
			return 'data feild num error'
		if len(data['ipgroup']) == 0:
			return 'groupName format error'
		if is_ip(data['ip']) is not True:
			return 'ip {} format error'.format(data['ip'])
		if acl.get_acl_src_ip_group_num(data['ipgroup']) == 1 and view.acl_src_ip_group_judge(data['ipgroup']): 
			return 'the group referenced can not delete'
		return 'true'
	elif op == 'clear':
		#先查询所有的组 再看组有没有被引用 有引用则不能清除
		if view.acl_src_ip_group_clear_judge() is not True:
			return 'there are group referenced can not delete'
		return 'true'
	elif op == 'query':
		return 'true'
	return 'unsupported operations'


def acl_dst_ip_group_check(op,data):
	if op == 'add': 
		if len(data) != 2:
			return 'data feild num error'
		if len(data['groupname']) == 0 or len(data['groupname']) > 80:
			return 'groupName format error'
		if '/' in data['ip'] or is_ip(data['ip']) is not True:
			return 'ip {} format error'.format(data['ip'])
		return 'true'
	elif op == 'delete': 
		if len(data) != 2:
			return 'data feild num error'
		if len(data['groupname']) == 0:
			return 'groupName format error'
		if is_ip(data['ip']) is not True:
			return 'ip {} format error'.format(data['ip'])
		if acl.get_acl_dst_ip_group_num(data['groupname']) == 1 and view.acl_dst_ip_group_judge(data['groupname']): 
			return 'the group referenced can not delete'
		return 'true'
	elif op == 'clear':
		if view.acl_dst_ip_group_clear_judge() is not True:
			return 'there are group referenced can not delete'
		return 'true'
	elif op == 'query':
		return 'true'
	return 'unsupported operations'


def acl_domain_group_check(op,data):
	if op == 'add': 
		if len(data) != 2:
			return 'data feild num error'
		if len(data['domaingroup']) == 0 or len(data['domaingroup']) > 80:
			return 'groupName format error'
		if is_domain(data['domain']) is not True:
			return 'domain {} format error'.format(data['domain'])
		return 'true'
	elif op == 'delete': 
		if len(data) != 2:
			return 'data feild num error'
		if len(data['domaingroup']) == 0:
			return 'groupName format error'
		if is_domain(data['domain']) is not True:
			return 'domain {} format error'.format(data['domain'])
		if acl.get_acl_domain_group_num(data['domaingroup']) == 1 and view.acl_domain_group_judge(data['domaingroup']): 
			return 'the group referenced can not delete'
		return 'true'
	elif op == 'clear':
		if view.acl_domain_group_clear_judge() is not True:
			return 'there are group referenced can not delete'
		return 'true'
	elif op == 'query':
		return 'true'
	return 'unsupported operations'


def view_check(op,data):
	if op == 'add':
		if len(data) != 5:
			return 'data feild num error'
		if len(data['viewname']) == 0 or len(data['viewname']) > 80:
			return 'viewName format error'
		if acl.src_ip_group_exist(data['srcipgroup']) is False:
			return 'srcIpGroup Not Exist'
		if acl.dst_ip_group_exist(data['dstipgroup']) is False:
			return 'dstIpGroup Not Exist'
		if acl.domain_group_exist(data['domaingroup']) is False:
			return 'domainGroup Not Exist'
		if data['rd'] != 'set' and data['rd'] != 'unset' and data['rd'] != 'null':
			return 'rd format error'
		return 'true'
	elif op == 'delete':
		return view.view_relation_judge(data['viewname'])
	elif op == 'clear':
		if view.view_clear_check() is False:
			return 'Views are referenced by others conf can not delete'
		return 'true'
	elif op == 'query':
		return 'true'
	return 'unsupported operations'


def cache_qtype_check(op,data):
	if op == 'add' or op == 'delete':
		if len(data) != 2:
			return 'data feild num error'
		if is_qtype(data['qtype']) is not True:
			return 'qtype format error'
		if op == 'delete':
			if len(data['view']) == 0:
				return 'view format error'
		else:
			if view.view_exist(data['view']) is not True:
				return 'view not exist'
		return 'true'
	elif op == 'query' or op == 'clear':
		return 'true'
	return 'unsupported operations'


def ttl_rules_check(op,data):
	if op == 'add' or op == 'update' or op =='delete':
		if len(data) != 4:
			return 'data feild num error'
		if is_domain(data['domain']) is not True:
			return 'domain {} format error'.format(data['domain'])
		if data['minttl'] < 1 or data['minttl'] > 604800 or data['maxttl'] < 1 or data['maxttl'] > 604800 or data['maxttl'] < data['minttl']:
			return 'ttl value range error'
		if op == 'delete':
			if len(data['view']) == 0:
				return 'view fommat error'
		else:
			if view.view_exist(data['view']) is not True:
				return 'view not exist'
		return 'true'
	elif op == 'query' or op == 'clear':
		return 'true'
	return 'unsupported operations'


def rrset_rules_check(op,data):
	if op == 'add' or op == 'delete' or op == 'update':
		if len(data) != 6:
			return 'data feild num error'
		if is_domain(data['domain']) is not True:
			return 'domain {} format error'.format(data['domain'])
		if is_qtype(data['qtype']) is not True:
			return 'qtype format error'
		if data['ttl'] < 1 or data['ttl'] > 604800:
			return 'ttl value range error'
		if data['weight'] <= 0 or data['weight'] >= 16:
			return 'weight value range error'
		if is_answer(data['qtype'],data['answer']) is not True:
			return 'answer format error'
		'''
		if op == 'delete':
			if len(data['view']) == 0:
				return 'view format error'
		else:
			if view.view_exist(data['view']) is not True:
				return 'view not exist'
		'''
		return 'true'
	elif op == 'query' or op == 'clear':
		return 'true'
	return 'unsupported operations'


def rrset_view_ip_check(op,data):
	if op == 'add':
		if len(data) != 2:
			return 'data feild num error'
		if '/' in data['ip'] or is_ip(data['ip']) is not True:
			return 'ip {} format error'.format(data['ip'])
		if view.view_exist(data['view']) is not True:
			return 'view not exist'
		return 'true'
	elif op == 'query' or op == 'clear' or op == 'delete':
		return 'true'
	return 'unsupported operations'


def view_ip_check(op,data):
	if op == 'add' or op == 'delete':
		if len(data) != 2:
			return 'data feild num error'
		if '/' not in data['ip'] or is_ip(data['ip']) is not True:
			return 'ip {} format error'.format(data['ip'])
		if op == 'delete':
			if len(data['view']) == 0:
				return 'view format error'
		else:
			if view.view_exist(data['view']) is not True:
				return 'view not exist'
		return 'true'
	elif op == 'query' or op == 'clear':
		return 'true'
	return 'unsupported operations'


def rrfilter_rules_check(op,data):
	if op == 'add' or op == 'delete' or op == 'update':
		if len(data) != 4:
			return 'data feild num error'
		if is_domain(data['domain']) is not True:
			return 'domain {} format error'.format(data['domain'])
		if is_qtype(data['qtype']) is not True:
			return 'qtype format error'
		if is_answer(data['qtype'],data['answer']) is not True:
			return 'answer format error'
		if op == 'delete':
			if len(data['view']) == 0:
				return 'view format error'
		else:
			if view.view_exist(data['view']) is not True:
				return 'view not exist'
		return 'true'
	elif op == 'query' or op == 'clear':
		return 'true'
	return 'unsupported operations'



def dns_domain_check(op,data):
	if op == 'add' or op == 'delete':
		if len(data) != 1:
			return 'data feild num error'
		if is_domain(data['domain']) is not True:	
			return 'domain {} format error'.format(data['domain'])
		return 'true'	
	elif op == 'query' or op == 'clear':
		return 'true'
	return 'unsupported operations'


def view_domain_check(op,data):
	if op == 'add' or op == 'delete':
		if len(data) != 2:
			return 'data feild num error'
		if is_domain(data['domain']) is not True:	
			return 'domain {} format error'.format(data['domain'])
		if op == 'delete':
			if len(data['view']) == 0:
				return 'view format error'
		else:
			if view.view_exist(data['view']) is not True:
				return 'view not exist'
		return 'true'	
	elif op == 'query' or op == 'clear':
		return 'true'
	return 'unsupported operations'


def forward_server_check(op,data):
	if op == 'add' or op == 'update' or op == 'delete':
		if len(data) != 4:
			return 'data feild num error'
		if '/' in data['ip'] or is_ip(data['ip']) is not True:
			return 'ip {} format error'.format(data['ip'])
		if data['weight'] < 0 or data['weight'] > 16:
			return 'weight value range error'
		if op == 'delete':
			if len(data['view']) == 0:
				return 'view format error'
			if bind.forward_server_delete_judge(data['servergroup']):
				return 'servergroup referenced can not delete'
		else:
			if view.view_exist(data['view']) is not True:
				return 'view not exist'
			if len(data['servergroup']) == 0 or len(data['servergroup']) > 80:
				return 'servergroup format error'
		return 'true'
	elif op == 'clear':
		if bind.forward_server_clear_judge() is not True:
			return 'there are servergroup referenced can not delete'
		return 'true'
	elif op == 'query':
		return 'true'
	return 'unsupported operations'


def forward_rules_check(op,data):
	if op == 'add' or op == 'update' or op == 'delete':
		if len(data) != 5:
			return 'data feild num error'
		if is_domain(data['domain']) is not True:	
			return 'domain {} format error'.format(data['domain'])
		if data['type'] != 'first' and data['type'] != 'only':
			return 'type format error'
		if data['action'] != 'merge' and data['action'] != 'normal':		
			return 'action format error'
		if op == 'delete':
			if len(data['view']) == 0:
				return 'view format error'
			if len(data['servergroup']) == 0:
				return 'servergroup not exist'
		else:
			if view.view_exist(data['view']) is not True:
				return 'view not exist'
			if bind.forward_server_exist(data['servergroup']) is not True:
				return 'servergroup not exist'
		return 'true'
	elif op == 'query' or op == 'clear':
		return 'true'
	return 'unsupported operations'



def stub_rules_check(op,data):
	if op == 'add' or op == 'update' or op == 'delete':
		if len(data) != 5:
			return 'data feild num error'
		if data['ttl'] < 1 or data['ttl'] > 604800:
			return 'ttl format error'
		if is_domain(data['domain']) is not True:	
			return 'domain {} format error'.format(data['domain'])
		if len(data['ns']) != 0 and is_domain(data['ns']) is not True:
			return 'ns format error'
		if len(data['ip']) != 0 and ('/' in data['ip'] or is_ip(data['ip']) is not True):		
			return 'ip {} format error'.format(data['ip'])
		if op == 'delete':
			if len(data['view']) == 0:
				return 'view format error'
		else:
			if view.view_exist(data['view']) is not True:
				return 'view not exist'
		return 'true'
	elif op == 'query' or op == 'clear':
		return 'true'
	return 'unsupported operations'



def dns64_rules_check(op,data):
	if op == 'add' or op == 'update' or op == 'delete':
		if len(data) != 3:
			return 'data feild num error'
		if is_domain(data['domain']) is not True:	
			return 'domain {} format error'.format(data['domain'])
		if ':' not in data['ipv6prefix'] or '/' in data['ipv6prefix'] or is_ip(data['ipv6prefix']) is not True:
			return 'ipv6prefix format error'
		if op == 'delete':
			if len(data['view']) == 0:
				return 'view format error'
		else:
			if view.view_exist(data['view']) is not True:
				return 'view not exist'
		return 'true'
	elif op == 'query' or op == 'clear':
		return 'true'
	return 'unsupported operations'




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
		'qpsthreshold': threshold_check
	},
	'useripwhitelist': {
		'switch': switch_check,
		'rules': ip_check
	},
	'serviceipwhitelist': {
		'switch': switch_check,
		'rules': ip_check
	},
	'accesscontrolanswerip': {
		'ipv4': ipv4_check,
		'ipv6': ipv6_check	
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
		'srcipblacklist': ip_sec_check,
		'serviceipblacklist': ip_sec_check,
		'domainblacklist': dname_check
	},
	'nxr': {
		'switch': view_switch_check,
		'redirectip': view_redirect_ip_check,
		'domainblacklist': dname_check,
		'srcipblacklist': ip_sec_check
	},
	'sortlist': {
		'switch': view_switch_check,
		'rules': sortlist_rules_check
	},
	'dts': {
		'switch': switch_check,
		'srcipgroup': dts_src_ip_group_check,
		'domaingroup': dts_domain_group_check,
		'dstipgroup': dts_dst_ip_group_check,
		'dnsqtype' : dts_qtype_check,
		'gtldomain': dts_tld_check,
		'forwardserver': dts_forward_server_check,
		'dtsfilter': dts_filter_check
	},
	'iptrans': {
		'srciptrans': ip_sec_check,
		'dstiptrans': ip_sec_check
	},
	'acl': {
		'iplist': acl_src_ip_group_check,
		'dstiplist': acl_dst_ip_group_check,
		'domainlist': acl_domain_group_check
	},
	'view': {
		'view': view_check
	},
	'selfcheck': {
		'cacheqtype': cache_qtype_check, 
		'noerrornoanswer': view_switch_check,
		'nxdomain': view_switch_check,
		'onlycname': view_switch_check,
	},
	'ttl': {
		'switch': view_switch_check,
		'rules': ttl_rules_check
	},
	'rrset': {
		'switch': view_switch_check,
		'rules': rrset_rules_check,
		'srcipblacklist': rrset_view_ip_check
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
		'srcipdisable': ip_sec_check,
		'dstipdisable': ip_sec_check,
		'domaindisable': dns_domain_check,
		'domainblacklist': dns_domain_check
	},
	'cachesync': {
		'switch': switch_check
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

def base_data_check(data,method):
	if len(data) != 6:
		return 'data feild num error'
	if data['source'] != 'ms' and data['source'] != 'cli':
		return 'source error'
	if method == 'POST':
		if data['op'] != 'add':
			return 'op error'
		if data['id'] < 0:
			return 'id error'
	elif method == 'PUT':
		if data['op'] != 'update':
			return 'op error'
		if data['id'] < 0:
			return 'id error'
	elif method == 'DELETE':
		if data['op'] != 'delete' and data['op'] != 'clear':
			return 'op error'
		if data['id'] < 0:
			return 'id error'
	elif method == 'GET':
		if data['op'] != 'query':
			return 'op error'
	return 'true'	


#合法性校验 {"source":"ms","id":100,"bt":"xxx","sbt":"xxx","op":"update","data":{"switch":"enable"}}
def check_dns_data(data,method):
	try:
		res = base_data_check(data,method)
		if res != 'true':
			return res
		if data['bt'] not in dns_bt:
			return 'bt error'
		if data['sbt'] not in dns_sbt:
			return 'sbt error'
		return data_check_methods[data['bt']][data['sbt']](data['op'],data['data'])
	except Exception as e:
		logger.error(str(e))
	return 'unknown error'	



def file_check(data):
	if len(data) != 1:
		return 'data feild num error'
	if len(data['file']) == 0:	
		return 'file format error'
	return 'true'	


def handle_cache_check(data):
	if len(data) != 3:
		return 'data feild num error'
	if len(data['handle']) == 0:
		return 'handle tag {} format error'.format(data['handle'])
	#  index type check
	return 'true'	


task_check_methods = {
	'cachebackup': file_check,
	'cacheimport': file_check,
	'cachedelete': handle_cache_check,
	'cachequery': handle_cache_check
}


# task 合法性校验
def check_task(data):
	try:
		if len(data) != 3:
			return 'data feild num error'
		if data['source'] != 'ms' and data['source'] != 'cli':
			return 'source error'
		return task_check_methods[data['tasktype']](data['data'])
	except Exception as e:
		logger.error(str(e))
	return 'unknown error'	



#以下为handle数据校验

def handle_ip_group_check(op,data):
	if op == 'add' or op == 'delete': 
		if len(data) != 2:
			return 'data feild num error'
		if len(data['ipgroup']) == 0 or len(data['ipgroup']) > 80:
			return 'groupName format error'
		if '/' not in data['ip'] or is_ip(data['ip']) is not True:
			return 'ip {} format error'.format(data['ip'])
		return 'true'
	elif op == 'clear' or op == 'query':
		return 'true'
	return 'unsupported operations'


def handle_ip_threshold_check(op,data):
	if op == 'add' or op == 'update' or op == 'delete':
		if len(data) != 2:
			return 'data feild num error'
		if '/' not in data['ip'] or is_ip(data['ip']) is not True:
			return 'ip {} format error'.format(data['ip'])
		if data['meter'] < 0 or data['meter'] > 0xffffffff:
			return 'meter value range error'
		return 'true'	
	elif op == 'query' or op == 'clear':
		return 'true'
	return 'unsupported operations'


def handle_meter_check(op,data):
	if op == 'add' or op == 'update' or op == 'delete':
		if len(data) != 2:
			return 'data feild num error'
		# 后续添加此字段规则
		if len(data['handle']) == 0:
			return 'handle tag {} format error'.format(data['handle'])
		if data['meter'] < 0 or data['meter'] > 0xffffffff:
			return 'meter value range error'
		return 'true'	
	elif op == 'query' or op == 'clear':
		return 'true'
	return 'unsupported operations'


def handle_tag_check(op,data):
	if op == 'add' or op == 'delete':
		if len(data) != 1:
			return 'data feild num error'
		# handle标识校验
		if len(data['handle']) > 255 or len(data['handle']) == 0:
			return 'handle tag {} format error'.format(data['handle'])
		return 'true'	
	elif op == 'query' or op == 'clear':
		return 'true'
	return 'unsupported operations'


def handle_forward_check(op,data):
	proto = ['icmp', 'udp', 'tcp', 'http', 'https']
	if op == 'add' or op == 'update':
		if len(data) != 4:
			return 'data feild num error'
		if len(data['group']) == 0 or len(data['group']) > 80:
			return 'group format error'
		if data['proto'] not in proto:
			return 'proto format error'
		if '/' in data['ip'] or is_ip(data['ip']) is not True:
			return 'ip {} format error'.format(data['ip'])
		if data['port'] <= 0 or data['port'] >= 65535:
			return 'port value range error'
		return 'true'	
	if op == 'delete':
		if len(data['group']) == 0 or len(data['group']) > 80:
			return 'group format error'
		return 'true'	
	elif op == 'query' or op == 'clear':
		return 'true'
	return 'unsupported operations'


def handle_proto_check(op,data):
	proto = ['icmp', 'udp', 'tcp', 'http', 'https']
	if op == 'add' or op == 'update':
		if len(data) != 5:
			return 'data feild num error'
		if data['action'] != 'enable' and data['action'] != 'disable':
			return 'action value error'
		if data['proto'] not in proto:
			return 'proto format error'
		if data['port'] <= 0 or data['port'] >= 65535:
			return 'port value range error'
		if '/' in data['ipv4'] or is_ip(data['ipv4']) is not True:
			return 'ipv4 {} format error'.format(data['ip'])
		if len(data['ipv6']) > 0 and ('/' in data['ipv6'] or is_ip(data['ipv4']) is not True):
			return 'ipv6 {} format error'.format(data['ip'])
		return 'true'	
	if op == 'delete':
		if len(data['group']) == 0 or len(data['group']) > 80:
			return 'group format error'
		return 'true'	
	elif op == 'query' or op == 'clear':
		return 'true'
	return 'unsupported operations'


def handle_cert_check(op,data):
	if op == 'add' or op == 'delete':
		if len(data) != 2:
			return 'data feild num error'
		if len(data['ca_cert']) == 0:
			return 'ca_cert format error'
		if len(data['rsa_key']) == 0:
			return 'rsa_key format error'
		return 'true'	
	elif op == 'query' or op == 'clear':
		return 'true'
	return 'unsupported operations'


def handle_servicecontrol_check(op,data):
	proto = ['ipv4-icmp', 'ipv4-udp', 'ipv4-tcp', 'ipv4-http', 'ipv4-https', 'ipv6-icmp', 'ipv6-udp', 'ipv6-tcp', 'ipv6-http', 'ipv6-https']
	if op == 'add' or op == 'update' or op == 'delete':
		if len(data) != 2:
			return 'data feild num error'
		if data['proto'] not in proto:
			return 'proto format error'
		if data['action'] != 'enable' and data['action'] != 'disable':
			return 'action value error'
		return 'true'	
	elif op == 'query' or op == 'clear':
		return 'true'
	return 'unsupported operations'


def handle_xforce_check(op,data):
	if op == 'add' or op == 'update' or op == 'delete':
		if len(data) != 5:
			return 'data feild num error'
		# 后续添加此字段规则
		if len(data['handle']) == 0 or len(data['handle']) > 255:
			return 'handle tag {} format error'.format(data['handle'])
		if data['ttl'] < 1 or data['ttl'] > 604800:
			return 'ttl value range error'
		# 补充index校验
		if data['index'] < 1 or data['index'] > 0xffff:
			return 'index value range error'
		#补充type校验
		if len(data['type']) == 0:
			return 'type error'
		#根据type校验data
		if len(data['data']) == 0:
			return 'data error'
		return 'true'	
	elif op == 'query' or op == 'clear':
		return 'true'
	return 'unsupported operations'


def meter_check(op,data):
	if op == 'update' or op == 'add':
		if len(data) != 1:
			return 'data feild num error'
		if data['meter'] < 0 or data['meter'] > 0xffffffff:
			return 'meter value range error'
		return 'true'	
	elif op == 'delete':
		return 'done'	
	elif op == 'query':
		return 'true'	
	return 'unsupported operations'


handle_check_methods = {
	'useripwhitelist': {
		'switch': switch_check,
		'rules': handle_ip_group_check
	},
	'ipthreshold': {
		'switch': switch_check,
		'rules': handle_ip_threshold_check
	}, 
	'handlethreshold': {
		'switch': switch_check,
		'rules': handle_meter_check
	}, 
	'srcipaccesscontrol': {
		'switch': switch_check,
		'rules': ip_sec_check
	},
	'handleaccesscontrol': {
		'switch': switch_check,
		'rules': handle_tag_check
	},
	'backend': {
		'forwardserver': handle_forward_check
	},
	'businessservice': {
		'switch': switch_check
	},
	'businessproto': {
		'rules': handle_proto_check
	},
	'certificate': {
		'rules': handle_cert_check
	},
	'xforce':{
		'switch': switch_check,
		'rules': handle_xforce_check
	},
	'cachesmartupdate': {
		'switch': switch_check
	},
	'cacheprefetch':{
		'switch': switch_check,
		'rules': handle_tag_check
	},
	'backendmeter': {
		'switch': switch_check,
		'rules': meter_check
	},
	'stub': {
		'rules': handle_xforce_check 
	}
}


def check_handle_data(data,method):
	try:
		res = base_data_check(data,method)
		if res != 'true':
			return res
		if data['bt'] not in handle_bt:
			return 'handle bt error'
		if data['sbt'] not in handle_sbt:
			return 'handle sbt error'
		return handle_check_methods[data['bt']][data['sbt']](data['op'],data['data'])
	except Exception as e:
		logger.error(str(e))
	return 'unknown error'	


