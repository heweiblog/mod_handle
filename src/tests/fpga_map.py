#!/usr/bin/python
# -*- coding: utf-8 -*-

from models import view,acl,dts


def view_id_map(data):
	if data['op'] == 'clear':
		return True
	group_id = view.get_view_id(data['data']['view'])
	if group_id != 0:
		data['data']['view'] = group_id
		return True
	return False


def acl_src_ip_list_id_map(data):
	if data['op'] == 'add':
		if acl.add_src_ip_list_map(data['data']['ipgroup']) is not True:
			return False
	elif data['op'] == 'clear':
		return True
	group_id = acl.get_src_ip_list_id(data['data']['ipgroup'])
	if group_id != 0:
		data['data']['ipgroup'] = group_id
		return True
	return False


def acl_dst_ip_list_id_map(data):
	if data['op'] == 'add':
		if acl.add_dst_ip_list_map(data['data']['groupname']) is not True:
			return False
	elif data['op'] == 'clear':
		return True
	group_id = acl.get_dst_ip_list_id(data['data']['groupname'])
	if group_id != 0:
		data['data']['groupname'] = group_id
		return True
	return False


def acl_domain_list_id_map(data):
	if data['op'] == 'add':
		if acl.add_acl_domain_list_map(data['data']['domaingroup']) is not True:
			return False
	elif data['op'] == 'clear':
		return True
	group_id = acl.get_acl_domain_list_id(data['data']['domaingroup'])
	if group_id != 0:
		data['data']['groupname'] = group_id
		return True
	return False


def acl_view_id_map(data):
	if data['op'] == 'add':
		if view.add_view_map(data['data']['viewname']) is not True:
			return False
	elif data['op'] == 'clear':
		return True
	view_id = view.get_view_id(data['data']['viewname'])
	src_id = acl.get_src_ip_list_id(data['data']['srcipgroup'])
	dst_id = acl.get_dst_ip_list_id(data['data']['dstipgroup'])
	domain_id = acl.get_acl_domain_list_id(data['data']['domaingroup'])
	if view_id != 0 and src_id != 0 and dst_id != 0 and domain_id != 0:
		data['data']['viewname'] = view_id
		data['data']['srcipgroup'] = src_id
		data['data']['dstipgroup'] = dst_id
		data['data']['domaingroup'] = domain_id
		return True
	return False


def dts_src_id_map(data):
	if data['op'] == 'add':
		if dts.add_dts_src_map(data['data']['groupname']) is not True:
			return False
	elif data['op'] == 'clear':
		return True
	group_id = dts.get_dts_src_id(data['data']['groupname'])
	if group_id != 0:
		data['data']['groupname'] = group_id
		return True
	return False


def dts_dst_id_map(data):
	if data['op'] == 'add':
		if dts.add_dts_dst_map(data['data']['groupname']) is not True:
			return False
	elif data['op'] == 'clear':
		return True
	group_id = dts.get_dts_dst_id(data['data']['groupname'])
	if group_id != 0:
		data['data']['groupname'] = group_id
		return True
	return False


def dts_domain_id_map(data):
	if data['op'] == 'add':
		if dts.add_dts_domain_map(data['data']['groupname']) is not True:
			return False
	elif data['op'] == 'clear':
		return True
	group_id = dts.get_dts_domain_id(data['data']['groupname'])
	if group_id != 0:
		data['data']['groupname'] = group_id
		return True
	return False


def dts_filter_id_map(data):
	if data['op'] == 'add':
		if dts.add_dts_filter_map(data['data']['filtername']) is not True:
			return False
	elif data['op'] == 'clear':
		return True
	dts_filter_id = dts.get_dts_filter_id(data['data']['filtername'])
	src_id = dts.get_dts_src_id(data['data']['srcgroup'])
	dst_id = dts.get_dts_dst_id(data['data']['dstgroup'])
	domain_id = dts.get_dts_domain_id(data['data']['domaingroup'])
	if dts_filter_id != 0 and src_id != 0 and dst_id != 0 and domain_id != 0:
		data['data']['filtername'] = dts_filter_id
		data['data']['srcgroup'] = src_id
		data['data']['dstgroup'] = dst_id
		data['data']['domaingroup'] = domain_id
		return True
	return False


def dts_forward_id_map(data):
	if data['op'] == 'add':
		if dts.add_dts_forward_map(data['data']['servergroup']) is not True:
			return False
	elif data['op'] == 'clear':
		return True
	group_id = dts.get_dts_forward_id(data['data']['servergroup'])
	if group_id != 0:
		data['data']['servergroup'] = group_id
		return True
	return False


def sortlist_id_map(data):
	if data['op'] == 'clear':
		return True
	group_id = view.get_view_id(data['data']['view'])
	if group_id != 0:
		data['data']['view'] = group_id
		sort_list = []
		for l in data['data']['sortlist']:
			acl_list = []
			for i in l:
				acl_id = acl.get_src_ip_list_id(i)
				if acl_id != 0:
					acl_list.append(acl_id)
				else:
					return False
			sort_list.append(acl_list)
		data['data']['sortlist'] = sort_list
		return True
	return False


fpga_map = {
	'nxr': {
		'switch': view_id_map,
		'redirectip': view_id_map
	},
	'sortlist': {
		'rules': sortlist_id_map
	},
	'acl': {
		'iplist': acl_src_ip_list_id_map,
		'dstiplist': acl_dst_ip_list_id_map,
		'domainlist': acl_domain_list_id_map
	},
	'view': {
		'view': acl_view_id_map
	},
	'dts': {
		'srcipgroup': dts_src_id_map,
		'dstipgroup': dts_dst_id_map,
		'domaingroup': dts_domain_id_map,
		'forwardserver': dts_forward_id_map,
		'dtsfilter': dts_filter_id_map 
	},
	'selfcheck': {
		'cacheqtype': view_id_map,
		'noerrornoanswer': view_id_map,
		'nxdomain': view_id_map,
		'onlycname': view_id_map
	},
	'ttl': {
		'switch': view_id_map,
		'rules': view_id_map
	},
	'rrset': {
		'switch': view_id_map,
		'rules': view_id_map,
		'srcipblacklist': view_id_map
	},
	'rrfilter': {
		'switch': view_id_map,
		'rules': view_id_map
	},
	'cachedisable': {
		'viewdisable': view_id_map
	},
	'cachesync': {
		'switch': view_id_map
	},
	'cachebackup': {
		'viewbackup': view_id_map,
		'viewimport': view_id_map
	},
	'cachedelete': {
		'rules': view_id_map
	},
	'cachequery': {
		'rules': view_id_map
	}
}



