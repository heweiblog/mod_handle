#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
from common.check import qtypes,is_ip
from common.log import logger,conf_logger
#from models import view,acl,bind


op_code = {
	'query': (0x01).to_bytes(1, byteorder='big'),
	'add': (0x02).to_bytes(1, byteorder='big'),
	'delete': (0x03).to_bytes(1, byteorder='big'),
	'update': (0x04).to_bytes(1, byteorder='big'),
	'clear': (0x05).to_bytes(1, byteorder='big')
}

rc_code = {
	20: 'success',
	30: 'other format error',
	31: 'proto version error',
	32: 'msg header error',
	33: 'msg body error',
	34: 'msg body too long',
	40: 'system error',
	41: 'system busy',
	42: 'operation timed out',
	43: 'business non-support',
}

sbt_code = {
	'cachedisable': {
		'bt': 0x11,
		'switch': 0x0401,
		'srcipdisable': 0x0403,
		'domaindisable': 0x0404,
		'domainblacklist': 0x0407 
	},
	'amplificationattack': {
		'bt': 0x13,
		'switch': 0x050e
	},
	'ipthreshold': {
		'bt': 0x13,
		'defaultthreshold': 0x0502,
		'rules': 0x0504
	},
	'domainthreshold': {
		'bt': 0x13,
		'rules': 0x0505
	},
	'ipdomainthreshold': {
		'bt': 0x13,
		'rules': 0x050a
	},
	'useripwhitelist': {
		'switch': 0x0201,
		'rules': 0x0202,
	},
	'rrset': {
		'bt': 0x12,
		'switch': 0x0101,
		'rules': 0x0102,
		'srcipblacklist': 0x0104,
	},
	'nxr': {
		'switch': 0x0201,
		'redirectip': 0x0203,
		'domainblacklist': 0x0205,
		'srcipblacklist': 0x0204
	}
}

def switch_map(data):
	if data['switch'] == 'enable':
		return (0x01).to_bytes(1, byteorder='big')
	return (0x00).to_bytes(1, byteorder='big')


def num_map(num,byte):
	return (num).to_bytes(byte, byteorder='big')


def ip_map(data):
	if '.' in data['ip']:
		return (0x04).to_bytes(1, byteorder='big') + socket.inet_pton(socket.AF_INET,data['ip'])
	return (0x06).to_bytes(1, byteorder='big') + socket.inet_pton(socket.AF_INET6,data['ip'])


def ip_mask_map(data):
	l = data['ip'].split('/')
	if '.' in data['ip']:
		return (0x04).to_bytes(1, byteorder='big') + socket.inet_pton(socket.AF_INET,l[0]) + (int(l[-1])).to_bytes(1, byteorder='big')
	return (0x06).to_bytes(1, byteorder='big') + socket.inet_pton(socket.AF_INET6,l[0]) + (int(l[-1])).to_bytes(1, byteorder='big')


def qtype_map(data):
	return (qtypes[data['qtype']]).to_bytes(2, byteorder='big')


def weight_map(data):
	return (data['weight']).to_bytes(1, byteorder='big')


def ttl_map(data):
	return (data['ttl']).to_bytes(4, byteorder='big')


def domain_map(data):
	return data['domain'].encode() + (0x00).to_bytes(1, byteorder='big')


def threshold_map(data):
	return num_map(data['threshold'],4)


def ip_threshold_map(data):
	return num_map(data['threshold'],4) + ip_mask_map(data)
	

def domain_threshold_map(data):
	return num_map(data['threshold'],4) + domain_map(data)


def ip_domain_threshold_map(data):
	return num_map(data['threshold'],4) + ip_mask_map(data) + domain_map(data)


def answer_map(data):
	#根据不同应答产生不同结果
	if data['qtype'] == 'a' or data['qtype'] == 'aaaa':
		if is_ip(data['answer']):
			ip = ip_map({'ip':data['answer']})
			return (len(ip)).to_bytes(2, byteorder='big') + ip
		domain = domain_map({'domain':data['answer']})
		return (len(domain)).to_bytes(2, byteorder='big') + domain
	elif data['qtype'] == 'cname' or data['qtype'] == 'ns':
		domain = domain_map({'domain':data['answer']})
		return (len(domain)).to_bytes(2, byteorder='big') + domain
	elif data['qtype'] == 'mx':
		mx = data['answer'].split('@')
		res = (int(mx[0])).to_bytes(2, byteorder='big') + domain_map({'domain':mx[1]}) 
		return (len(res)).to_bytes(2, byteorder='big') + res
	elif 'srv' == qtype:
		srv = data['answer'].split('@')
		res = (int(srv[0])).to_bytes(2, byteorder='big') + (int(srv[1])).to_bytes(2, byteorder='big') + (int(srv[2])).to_bytes(2, byteorder='big') + domain_map({'domain':srv[3]})
		return (len(res)).to_bytes(2, byteorder='big') + res
	elif 'naptr' == qtype:
		ptr = data['answer'].split('@')
		res = (int(ptr[0])).to_bytes(2, byteorder='big') + (int(ptr[1])).to_bytes(2, byteorder='big') + ptr[2].encode() +  ptr[3].encode() + ptr[4].encode() + domain_map({'domain':ptr[5]})
		return (len(res)).to_bytes(2, byteorder='big') + res


def rrset_map(data):
	return ip_mask_map({'ip':'0.0.0.0/0'}) + qtype_map(data) + domain_map(data) + weight_map(data) + ttl_map(data) + answer_map(data) 
	

def nxr_redirect_ip_map(data):
	return num_map(data['weight'],1) + ip_map(data)


dnsys_data_methods = {
	'cachedisable': {
		'switch': switch_map,
		'srcipdisable': ip_mask_map,
		'domaindisable': domain_map,
		'domainblacklist': domain_map
	},
	'amplificationattack': {
		'switch': switch_map,
	},
	'ipthreshold': {
		'rules': ip_threshold_map,
		'defaultthreshold': threshold_map 
	},
	'ipdomainthreshold': {
		'rules': ip_domain_threshold_map
	},
	'domainthreshold': {
		'rules': domain_threshold_map,
	},
	'useripwhitelist': {
		'switch': switch_map,
		'rules': ip_mask_map,
	},
	'spreadecho': {
		'srcipblacklist': ip_map, 
		'domainblacklist': domain_map,
	},
	'rrset': {
		'switch': switch_map,
		'rules': rrset_map,
		'srcipblacklist': ip_mask_map
	},
	'nxr': {
		'switch': switch_map,
		'redirectip': nxr_redirect_ip_map,
		'domainblacklist': domain_map,
		'srcipblacklist': ip_mask_map
	}
}


def dnsys_data_map(data):
	try:
		ver = (0x01).to_bytes(1, byteorder='big')
		cid = (data['id']%65535).to_bytes(2, byteorder='big')
		dt = (0x01).to_bytes(1, byteorder='big')
		did = (0x01).to_bytes(1, byteorder='big')
		bt = (sbt_code[data['bt']]['bt']).to_bytes(1, byteorder='big')
		sbt = (sbt_code[data['bt']][data['sbt']]).to_bytes(2, byteorder='big')
		op = op_code[data['op']]
		opt = (0x00).to_bytes(7, byteorder='big')
		if data['op'] == 'clear':
			bl = (0x00).to_bytes(4, byteorder='big')
			return ver+cid+dt+did+bt+sbt+op+bl+opt
		body = dnsys_data_methods[data['bt']][data['sbt']](data['data'])
		bl = (6+len(body)).to_bytes(4, byteorder='big')
		ul = (4+len(body)).to_bytes(2, byteorder='big')
		sn = (data['id']).to_bytes(4, byteorder='big')
		#print(ver,cid,dt,did,bt,sbt,op,bl,opt,ul,sn,body)
		#print(6+len(body))
		return ver+cid+dt+did+bt+sbt+op+bl+opt+ul+sn+body
	except Exception as e:
		conf_logger.error(str(e))
	return None


def dnsys_result_check(data):
	#print(data)
	try:
		rc = data[8]
		if rc in rc_code:
			#print(rc_code[rc])
			return rc_code[rc]
	except Exception as e:
		conf_logger.error(str(e))
		return str(e)
	return 'failed'


'''
db_methods = {
	'iptables': {
		'switch': switch.switch_methods,
		'rules': iptables.iptables_methods,
	},
	'dnsipfragment': {
		'switch': switch.switch_methods
	},
	'ipfragment': {
		'switch': switch.switch_methods
	},
	'icmpflood': {
		'switch': switch.switch_methods,
		'ipv4totalthreshold': threshold.total_threshold_methods,
		'ipv6totalthreshold': threshold.total_threshold_methods,
		'ipthreshold': threshold.ip_threshold_methods
	},
	'tcpflood': {
		'switch': switch.switch_methods,
		'ipv4totalthreshold': threshold.total_threshold_methods,
		'ipv6totalthreshold': threshold.total_threshold_methods,
		'ipthreshold': threshold.ip_threshold_methods,
		'ipv4no53threshold': threshold.total_threshold_methods,
		'ipv6no53threshold': threshold.total_threshold_methods 
	},
	'udpflood': {
		'ipv4no53threshold': threshold.total_threshold_methods,
		'ipv6no53threshold': threshold.total_threshold_methods 
	},
	'creditdname': {
		'switch': switch.switch_methods,
		'totalthreshold': threshold.total_threshold_methods,
		'dnamethreshold': threshold.domain_threshold_methods,
		'dnamelist': domain.credit_dname_methods
	},
	'ipthreshold': {
		'switch': switch.switch_methods,
		'rules': threshold.ip_threshold_methods,
		'defaultthreshold': threshold.total_threshold_methods
	},
	'domainthreshold': {
		'switch': switch.switch_methods,
		'rules': threshold.domain_threshold_methods
	},
	'ipdomainthreshold': {
		'switch': switch.switch_methods,
		'rules': threshold.ip_domain_threshold_methods
	},
	'backendthreshold': {
		'updatethreshold': threshold.total_threshold_methods,
		'ipv4nohitthreshold': threshold.total_threshold_methods,
		'ipv6nohitthreshold': threshold.total_threshold_methods,
		'dnamethreshold': threshold.domain_threshold_methods
	},
	'replythreshold': {
		'replythreshold': threshold.total_threshold_methods
	},
	'poisonprotect': {
		'switch': switch.switch_methods,
		'x20': switch.switch_methods,
		'linkage': switch.switch_methods
	},
	'amplificationattack': {
		'switch': switch.switch_methods,
		'maxanswerlen': threshold.total_threshold_methods,
		'qpsthreshold': threshold.total_threshold_methods
	},
	'useripwhitelist': {
		'switch': switch.switch_methods,
		'rules': ip.ip_list_methods
	},
	'serviceipwhitelist': {
		'switch': switch.switch_methods,
		'rules': ip.ip_list_methods
	},
	'accesscontrolanswerip': {
		'ipv4': ip.access_ip_methods,
		'ipv6': ip.access_ip_methods	
	},
	'srcipaccesscontrol': {
		'switch': switch.switch_methods,
		'rules': ip.src_ip_access_control_methods 
	},
	'domainaccesscontrol': {
		'switch': switch.switch_methods,
		'rules': domain.domain_access_control_methods
	},
	'ipdomainaccesscontrol': {
		'switch': switch.switch_methods,
		'rules': domain.ip_domain_access_control_methods
	},
	'domainqtypeaccesscontrol': {
		'switch': switch.switch_methods,
		'rules': domain.domain_qtype_access_control_methods
	},
	'qtypeaccesscontrol': {
		'switch': switch.switch_methods,
		'rules': domain.qtype_access_control_methods
	},
	'ipqtypeaccesscontrol': {
		'switch': switch.switch_methods,
		'rules': ip.ip_qtype_access_control_methods
	},
	'graydomainaccesscontrol': {
		'switch': switch.switch_methods,
		'rules': domain.gray_domain_access_control_methods,
		'odds': threshold.total_threshold_methods,
		'redirectip': ip.ip_weight_methods
	},
	'importdnameprotect': {
		'switch': switch.switch_methods,
		'rules': domain.import_dname_methods
	},
	'spreadecho': {
		'switch': switch.switch_methods,
		'srcipblacklist': ip.ip_list_methods, 
		'serviceipblacklist': ip.ip_list_methods,
		'domainblacklist': domain.domain_list_methods
	},
	'nxr': {
		'switch': switch.view_switch_methods,
		'redirectip': view.nxr_redirect_ip_methods,
		'domainblacklist': domain.domain_list_methods,
		'srcipblacklist': ip.ip_list_methods
	},
	'sortlist': {
		'switch': switch.view_switch_methods,
		'rules': view.sortlist_methods
	},
	'dts': {
		'switch': switch.switch_methods,
		'srcipgroup': dts.dts_src_ip_group_methods,
		'domaingroup': dts.dts_domain_group_methods,
		'dstipgroup': dts.dts_dst_ip_group_methods,
		'dnsqtype': proto.qtype_methods,
		'gtldomain': proto.tld_methods,
		'forwardserver': dts.dts_forward_group_methods,
		'dtsfilter': dts.dts_filter_methods 
	},
	'iptrans': {
		'srciptrans': ip.ip_list_methods, 
		'dstiptrans': ip.ip_list_methods
	},
	'acl': {
		'iplist': acl.src_ip_list_methods,
		'dstiplist': acl.dst_ip_list_methods,
		'domainlist': acl.acl_domain_list_methods
	},
	'view': {
		'view': view.view_methods
	},
	'selfcheck': {
		'cacheqtype': view.view_qtype_methods,
		'noerrornoanswer': switch.view_switch_methods,
		'nxdomain': switch.view_switch_methods,
		'onlycname': switch.view_switch_methods
	},
	'ttl': {
		'switch': switch.view_switch_methods,
		'rules': view.ttl_methods
	},
	'rrset': {
		'switch': switch.view_switch_methods,
		'rules': view.rrset_methods,
		'srcipblacklist': bind.view_ip_methods
	},
	'rrfilter': {
		'switch': switch.view_switch_methods,
		'rules': view.rrfilter_methods
	},
	'expiredactivate': {
		'switch': switch.switch_methods,
	},
	'cachedisable': {
		'switch': switch.switch_methods,
		'viewdisable': switch.view_switch_methods,
		'srcipdisable': ip.ip_list_methods,
		'dstipdisable': ip.ip_list_methods,
		'domaindisable': domain.domain_list_methods,
		'domainblacklist': domain.domain_list_methods
	},
	'cachesync': {
		'switch': switch.switch_methods
	},
	'minimalresponses': {
		'switch': switch.switch_methods,
	},
	'smartupdate': {
		'switch': switch.switch_methods,
	},
	'forward': {
		'switch': switch.view_switch_methods,
		'forwardserver': bind.forward_server_methods,
		'srcipblacklist': bind.view_ip_methods,
		'domainblacklist': bind.view_domain_methods,
		'rules': bind.forward_rules_methods
	},
	'edns': {
		'switch': switch.view_switch_methods,
		'viewmapping': bind.view_ip_methods,
		'rules': bind.view_domain_methods
	},
	'stub': {
		'switch': switch.view_switch_methods,
		'rules': bind.stub_methods
	},
	'dns64': {
		'switch': switch.view_switch_methods,
		'rules': bind.dns64_methods
	},
	'rootconfig': {
		'rootconfig': bind.stub_methods
	}

}
'''

