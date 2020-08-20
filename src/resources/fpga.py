#!/usr/bin/python
# -*- coding: utf-8 -*-


def switch_rollback(data):
	if data['data']['switch'] == 'enable':
		data['data']['switch'] == 'disable'
	elif data['data']['switch'] == 'disable':
		data['data']['switch'] == 'enable'
	return data


def iptables_rollback(data):
	if data['op'] == 'add':
		data['op'] == 'delete'
	elif data['op'] == 'delete':
		#可能需要从数据库读取
		data['op'] == 'add'
	elif data['op'] == 'clear':
		pass
		# 从数据库读出所有iptables添加
	return data


def ip_threshold_rollback(data):
	if data['op'] == 'add':
		data['op'] == 'delete'
	elif data['op'] == 'delete':
		#可能需要从数据库读取
		data['op'] == 'add'
	elif data['op'] == 'update':
		pass
		#读数据库若数据存在则继续修改成数据库原来的数据，不存在则op换成delete
	elif data['op'] == 'clear':
		pass
		# 从数据库读出所有ip限速再添加
	return data
	



'''
fpga_rollback_methods = {
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


