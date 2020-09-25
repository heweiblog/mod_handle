#!/usr/bin/python
# -*- coding: utf-8 -*-

from common.conf import crm_cfg
from models import view,acl,bind


def acl_ip_list_map(data):
	if data['op'] == 'add':
		l = []
		l.append(data['data']['ip'])
		ip_list = acl.get_src_ip_list(data)
		if ip_list is not None:
			for i in ip_list:
				if i['ip'] not in l:
					l.append(i['ip'])
		url = 'http://{}:{}/api/ybind/v1.0/acl?name={}'.format(crm_cfg['ybind']['ip'],crm_cfg['ybind']['port'],data['data']['ipgroup'])
		if len(l) == 1:
			return 'post',url,l
		return 'put',url,l
	elif data['op'] == 'delete':
		l = []
		ip_list = acl.get_src_ip_list(data)
		if ip_list is not None:
			for i in ip_list:
				if i['ip'] != data['data']['ip']:
					l.append(i['ip'])
		url = 'http://{}:{}/api/ybind/v1.0/acl?name={}'.format(crm_cfg['ybind']['ip'],crm_cfg['ybind']['port'],data['data']['ipgroup'])
		if len(l) > 0:
			return 'put',url,l
		else:
			return 'delete',url,None
	elif data['op'] == 'clear':
		url = 'http://{}:{}/api/ybind/v1.0/acl'.format(crm_cfg['ybind']['ip'],crm_cfg['ybind']['port'])
		return 'delete',url,None
		

def acl_dst_ip_map(data):
	if data['op'] == 'add':
		l = []
		l.append(data['data']['ip'])
		ip_list = acl.get_dst_ip_list(data)
		if ip_list is not None:
			for i in ip_list:
				if i['ip'] not in l:
					l.append(i['ip'])
		url = 'http://{}:{}/api/ybind/v1.0/acl?name={}'.format(crm_cfg['ybind']['ip'],crm_cfg['ybind']['port'],data['data']['groupname'])
		if len(l) == 1:
			return 'post',url,l
		return 'put',url,l
	elif data['op'] == 'delete':
		l = []
		ip_list = acl.get_dst_ip_list(data)
		if ip_list is not None:
			for i in ip_list:
				if i['ip'] != data['data']['ip']:
					l.append(i['ip'])
		url = 'http://{}:{}/api/ybind/v1.0/acl?name={}'.format(crm_cfg['ybind']['ip'],crm_cfg['ybind']['port'],data['data']['groupname'])
		if len(l) > 0:
			return 'put',url,l
		else:
			return 'delete',url,None
	elif data['op'] == 'clear':
		url = 'http://{}:{}/api/ybind/v1.0/acl'.format(crm_cfg['ybind']['ip'],crm_cfg['ybind']['port'])
		return 'delete',url,None


def view_map(data):
	if data['op'] == 'add':
		domain_list = acl.get_acl_domain_list(data)
		l = []
		for d in domain_list:
			l.append(d['domain'])
		url = 'http://{}:{}/api/ybind/v1.0/view?name={}'.format(crm_cfg['ybind']['ip'],crm_cfg['ybind']['port'],data['data']['viewname'])
		y_data = {
			'match-clients': [data['data']['srcipgroup']],
			'match-destinations': [data['data']['dstipgroup']], 
			'match-domains': l,
			"match-recursive-only": True if data['data']['rd'] == 'set' else False
		}
		return 'post',url,y_data
	elif data['op'] == 'delete':
		url = 'http://{}:{}/api/ybind/v1.0/view?name={}'.format(crm_cfg['ybind']['ip'],crm_cfg['ybind']['port'],data['data']['viewname'])
		return 'delete',url,None
	elif data['op'] == 'clear':
		url = 'http://{}:{}/api/ybind/v1.0/view'.format(crm_cfg['ybind']['ip'],crm_cfg['ybind']['port'])
		return 'delete',url,None


def forward_server_map(data):
	if data['op'] == 'update' or data['op'] == 'add':
		url = 'http://{}:{}/api/ybind/v1.0/forwarders?view={}'.format(crm_cfg['ybind']['ip'],crm_cfg['ybind']['port'],data['data']['view'])
		y_data = bind.get_bind_forward_server(data)
		s = {'ip':data['data']['ip'],'weight':data['data']['weight']}
		size = len(y_data)
		if size > 0:
			for i in range(size):
				if y_data[i]['ip'] == s['ip']:
					y_data[i]['weight'] = s['weight']
		if s not in y_data:
			y_data.append(s)
		return 'put',url,y_data
	elif data['op'] == 'delete':
		url = 'http://{}:{}/api/ybind/v1.0/forwarders?view={}'.format(crm_cfg['ybind']['ip'],crm_cfg['ybind']['port'],data['data']['view'])
		# ybind接口此处为put
		return 'put',url,None
	elif data['op'] == 'clear':
		url = 'http://{}:{}/api/ybind/v1.0/forwarders'.format(crm_cfg['ybind']['ip'],crm_cfg['ybind']['port'])
		# ybind接口此处为put
		return 'put',url,None


def forward_rules_map(data):
	if data['op'] == 'update' or data['op'] == 'add':
		url = 'http://{}:{}/api/ybind/v1.0/forward-zone?name={}&view={}'.format(crm_cfg['ybind']['ip'],crm_cfg['ybind']['port'],data['data']['domain'],data['data']['view'])
		srv_list = bind.get_bind_forward_server(data)
		y_data = {
			'type': 'forward',
			'forward': {
				'mode': data['data']['type'],
				'algo': 'weight'
			},
			'forwarders': srv_list
		}
		return 'post' if data['op'] == 'add' else 'put',url,y_data
	elif data['op'] == 'delete':
		url = 'http://{}:{}/api/ybind/v1.0/forward-zone?name={}&view={}'.format(crm_cfg['ybind']['ip'],crm_cfg['ybind']['port'],data['data']['domain'],data['data']['view'])
		return 'delete',url,None
	elif data['op'] == 'clear': 
		# 现有接口需要发多次，后续是否加类似以下接口
		url = 'http://{}:{}/api/ybind/v1.0/forward-zone'.format(crm_cfg['ybind']['ip'],crm_cfg['ybind']['port'])
		return 'delete',url,None


def stub_map(data):
	if data['op'] == 'add' or data['op'] == 'update':
		url = 'http://{}:{}/api/ybind/v1.0/static-stub-zone?name={}&view={}'.format(crm_cfg['ybind']['ip'],crm_cfg['ybind']['port'],data['data']['domain'],data['data']['view'])
		y_data = {'type':'static-stub', 'server-names': [data['data']['ns']], 'server-addresses': [data['data']['ip']]}
		return 'post' if data['op'] == 'add' else 'put',url,y_data
	elif data['op'] == 'delete':
		url = 'http://{}:{}/api/ybind/v1.0/static-stub-zone?name={}&view={}'.format(crm_cfg['ybind']['ip'],crm_cfg['ybind']['port'],data['data']['domain'],data['data']['view'])
		return 'delete',url,None
	elif data['op'] == 'clear': 
		# 现有接口需要发多次，后续是否加类似以下接口
		url = 'http://{}:{}/api/ybind/v1.0/static-stub-zone'.format(crm_cfg['ybind']['ip'],crm_cfg['ybind']['port'])
		return 'delete',url,None


def rootcopy_map(data):
	if data['op'] == 'add':
		url = 'http://{}:{}/api/ybind/v1.0/static-stub-zone?name=.&view=default'.format(crm_cfg['ybind']['ip'],crm_cfg['ybind']['port'])
		y_data = {'type':'static-stub', 'server-addresses': data['data']['ip']}
		return 'post',url,y_data
	elif data['op'] == 'delete':
		url = 'http://{}:{}/api/ybind/v1.0/static-stub-zone?name=.&view=default'.format(crm_cfg['ybind']['ip'],crm_cfg['ybind']['port'])
		return 'delete',url,None
	elif data['op'] == 'clear': 
		# 现有接口需要发多次，后续是否加类似以下接口
		url = 'http://{}:{}/api/ybind/v1.0/static-stub-zone'.format(crm_cfg['ybind']['ip'],crm_cfg['ybind']['port'])
		return 'delete',url,None


def root_conf_map(data):
	if data['op'] == 'add' or data['op'] == 'update':
		#url = 'http://{}:{}/api/ybind/v1.0/hint-zone?name={}&view={}'.format(crm_cfg['ybind']['ip'],crm_cfg['ybind']['port'],data['data']['domain'],data['data']['view'])
		url = 'http://{}:{}/api/ybind/v1.0/hint-zone?name=.&view={}'.format(crm_cfg['ybind']['ip'],crm_cfg['ybind']['port'],data['data']['view'])
		ns = {'A':[{'rdata':data['data']['ip']}]} if '.' in data['data']['ip'] else {'AAAA':[{'rdata':data['data']['ip']}]}
		rr = {'@':{'NS':[{'ttl':data['data']['ttl'],'rdata':data['data']['ns']}]},data['data']['ns']:ns}
		y_data = {'type':'hint', 'rr': rr}
		return 'post' if data['op'] == 'add' else 'put',url,y_data
	elif data['op'] == 'delete':
		url = 'http://{}:{}/api/ybind/v1.0/hint-zone?name={}&view={}'.format(crm_cfg['ybind']['ip'],crm_cfg['ybind']['port'],data['data']['domain'],data['data']['view'])
		return 'delete',url,None
	elif data['op'] == 'clear': 
		# 现有接口需要发多次，后续是否加类似以下接口
		url = 'http://{}:{}/api/ybind/v1.0/hint-zone'.format(crm_cfg['ybind']['ip'],crm_cfg['ybind']['port'])
		return 'delete',url,None


def cache_view_switch_map(data):
	url = 'http://{}:{}/api/ybind/v1.0/cache/cache-disable?view={}'.format(crm_cfg['ybind']['ip'],crm_cfg['ybind']['port'],data['data']['view'])
	return 'put',url,True if data['data']['switch'] == 'enable' else False


def expiredactivate_switch_map(data):
	url = 'http://{}:{}/api/ybind/v1.0/cache/stale-answer-enable?value={}'.format(crm_cfg['ybind']['ip'],crm_cfg['ybind']['port'],'true' if data['data']['switch'] == 'enable' else 'false')
	return 'put',url,None


def sortlist_map(data):
	pass

ybind_map = {
	'acl': {
		'iplist': acl_ip_list_map,
		'dstiplist': acl_dst_ip_map
	},
	'view': {
		'view': view_map
	},
	'forward': {
		'forwardserver': forward_server_map,
		'rules': forward_rules_map
	},
	'stub': {
		'rules': stub_map
	},
	'rootcopy': {
		'rules': rootcopy_map
	},
	'rootconfig': {
		'rootconfig': root_conf_map
	},
	'cachedisable': {
		'viewdisable': cache_view_switch_map
	},
	'expiredactivate': {
		'switch': expiredactivate_switch_map,
	}
}



'''
ybind_map = {
	'acl': {
		'iplist': acl_ip_list_map,
		'dstiplist': acl_dst_ip_map
	}
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
	'amplificationattack': {
		'switch': switch.switch_methods,
		'maxanswerlen': threshold.total_threshold_methods,
		'qpsThreshold': threshold.total_threshold_methods
	},
	'useripwhitelist': {
		'switch': switch.switch_methods,
		'rules': ip.ip_list_methods
	},
	'serviceipwhitelist': {
		'switch': switch.switch_methods,
		'rules': ip.ip_list_methods
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
		'srcipblacklist': view.view_ip_methods
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
	'cachebackup': {
		'globalbackup': proto.file_list_methods,
		'globaimport': proto.file_list_methods,
		'viewbackup': view.view_file_methods,
		'viewimport': view.view_file_methods
	},
	'cachedelete': {
		#'rules'
	},
	'cachequery': {
		#'rules'
	},
	'minimalresponses': {
		'switch': switch.switch_methods,
	},
	'smartupdate': {
		'switch': switch.switch_methods,
	},
	'forward': {
		'switch': switch.view_switch_methods,
		'forwardserver': view.forward_server_methods,
		'srcipblacklist': view.view_ip_methods,
		'domainblacklist': view.view_domain_methods,
		'rules': view.forward_rules_methods
	},
	'edns': {
		'switch': switch.view_switch_methods,
		'viewmapping': view.view_ip_methods,
		'rules': view.view_domain_methods
	},
	'stub': {
		'switch': switch.view_switch_methods,
		'rules': view.stub_methods
	},
	'dns64': {
		'switch': switch.view_switch_methods,
		'rules': view.dns64_methods
	},
	'rootconfig': {
		'rootconfig': view.stub_methods
	}
}
'''
