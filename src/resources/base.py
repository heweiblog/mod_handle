#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading,json,time,asyncio,aiohttp,socket,requests
from common.log import logger,conf_logger
from common.check import check_data
from common.queue import dns_queue,handle_queue,task_queue
from common.conf import crm_cfg
from common.pub import ybind_bt,fpga_bt,dnsys_addr,proxy_bt,xforward_bt,recursion_bt,kernel_bt

from resources.ybind import ybind_map
from resources.task import do_task
from resources.dnsys import dnsys_data_map,dnsys_result_check
from models import content,switch,iptables,proto,threshold,domain,ip,view,acl,dts,bind,handle,register


loop = asyncio.get_event_loop()
handle_loop = asyncio.get_event_loop()
sync_loop = asyncio.get_event_loop()


dns_db_methods = {
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
	},
	'rootcopy': {
		'rules': ip.rootcopy_methods
	}

}



def handle_real_data(data):
	try:
		dns_db_methods[data['bt']][data['sbt']][data['op']](data)
	except Exception as e:
		logger.error(str(e))






async def conf_dnsys(client,data):
	try:
		send_data = dnsys_data_map(data)
		print(send_data,len(send_data))
		if send_data == None:
			return [{'id':data['id'], 'status':'failed', 'msg':'unsupported conf'}]
		tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		tcp_socket.settimeout(10)
		tcp_socket.connect(dnsys_addr)
		tcp_socket.send(send_data)
		recv_data = tcp_socket.recv(1024)
		res = dnsys_result_check(recv_data)
		tcp_socket.close()
		if res == 'success':
			return [{'id':data['id'], 'status':'success', 'msg':''}]
		return [{'id':data['id'], 'status':'failed', 'msg':res}]
	except Exception as e:
		conf_logger.error(str(e))
		return [{'id':data['id'], 'status':'failed', 'msg':str(e)}]
	return [{'id':data['id'], 'status':'failed', 'msg':'unknow error'}]


async def conf_ybind(client,data):
	try:
		# 此处处理data 转换成ybind需要的格式 然后发给ybind ybind的url接口比较丰富，此处需要根据不同数据请求不同url
		#后续if else去掉 ybind所有配置需适配
		if data['bt'] in ybind_map and data['sbt'] in ybind_map[data['bt']]:
			method,url,ybind_data = ybind_map[data['bt']][data['sbt']](data)
			conf_logger.debug('send data to ybind method={} url={} data={}'.format(method,url,ybind_data))
			return {'rcode': 0, 'description': 'Success'}
			if method == 'post':
				async with client.post(url, json = ybind_data, timeout = 10) as resp:
					return await resp.json()
			if method == 'put':
				async with client.put(url, json = ybind_data, timeout = 10) as resp:
					return await resp.json()
			elif method == 'delete':
				async with client.delete(url, json = ybind_data, timeout = 10) as resp:
					return await resp.json()
		else:
			conf_logger.debug('ybind not support conf: {}'.format(data))
			return {'rcode': 0, 'description': 'Success'}
	except Exception as e:
		conf_logger.error(str(e))
		return {'rcode': 999, 'description': str(e)}
	return {'rcode': 999, 'description': 'unknow error'}


async def pub_conf(data):
	async with aiohttp.ClientSession() as client:
		if data['bt'] in fpga_bt:
			fpga_res = await conf_dnsys(client,data)
			conf_logger.debug('recv data from dnsys: {}'.format(fpga_res))
			try:
				if fpga_res[0]['status'] == 'success':
					#可能还需调用ybind commit接口
					content.add_oplog(data, 'success', '')
					handle_real_data(data)
					conf_logger.info('conf success: {}'.format(data))
					return 'success'
				else:
					content.add_oplog(data, 'fail', fpga_res[0]['msg'])
					conf_logger.info('conf failed: {}'.format(data))
					return fpga_res[0]['msg']
			except Exception as e:
				conf_logger.error(str(e))
				content.add_oplog(data, 'fail', 'fpga api return result error')
				conf_logger.info('conf failed: {}'.format(data))
				return 'fpga api return result error'
		elif data['bt'] in ybind_bt:
			ybind_res = await conf_ybind(client,data)
			conf_logger.debug('recv ybind:{}'.format(ybind_res))
			try:
				if ybind_res['description'] == 'Success':
					content.add_oplog(data, 'success', '')
					handle_real_data(data)
					conf_logger.info('conf success: {}'.format(data))
					return 'success'
				else:
					content.add_oplog(data, 'fail', ybind_res['description'])
					conf_logger.info('conf failed: {}'.format(data))
					return ybind_res['description']
			except Exception as e:
				conf_logger.error(str(e))
				content.add_oplog(data, 'fail', 'ybind api return result error')
				conf_logger.info('conf failed: {}'.format(data))
				return 'ybind api return result error'
		else:
			fpga_res = await conf_dnsys(client,data)
			ybind_res = await conf_ybind(client,data)
			conf_logger.debug('recv data from ybind:{} dnsys:{}'.format(ybind_res,fpga_res))
			try:
				if ybind_res['description'] == 'Success' and fpga_res[0]['status'] == 'success':
					#可能还需调用ybind commit接口
					content.add_oplog(data, 'success', '')
					handle_real_data(data)
					conf_logger.info('conf success {}'.format(data))
					return 'success'
				elif ybind_res['description'] == 'Success' and fpga_res[0]['status'] != 'success':
					# ybind回退操作
					#ybind_res = await rollback_ybind(client,data)
					content.add_oplog(data, 'fail', 'ybind conf success and fpga conf failed')
					conf_logger.info('conf failed: {}'.format(data))
					return fpga_res[0]['msg']
				elif ybind_res['description'] != 'Success' and fpga_res[0]['status'] == 'success':
					# fpga回滚操作
					#fpga_res = await rollback_fpga(client,data)
					content.add_oplog(data, 'fail', 'dnsys conf success and ybind conf failed')
					conf_logger.info('conf failed: {}'.format(data))
					return ybind_res['description']
				else:
					content.add_oplog(data, 'fail', 'dnsys and ybind conf failed')
					conf_logger.info('conf failed: {}'.format(data))
					return 'dnsys and ybind conf failed'
			except Exception as e:
				conf_logger.error(str(e))
				content.add_oplog(data, 'fail', 'api return result error')
				conf_logger.info('conf failed: {}'.format(data))
				return 'api return result error'



def get_all_fpga_conf():
	l = acl.get_all_acl() + view.get_all_fpga_view() + dts.get_all_dts() + ip.get_all_ip() + domain.get_all_domain() + \
	iptables.get_all_iptables() + proto.get_all_proto() + switch.get_all_fpga_switch() + threshold.get_all_threshold() + bind.get_all_fpga_bind()
	for i in range(len(l)):
		l[i]['id'] = i+1
	return l


def get_all_conf():
	l = acl.get_all_acl() + view.get_all_view() + dts.get_all_dts() + ip.get_all_ip() + domain.get_all_domain() + \
	iptables.get_all_iptables() + proto.get_all_proto() + switch.get_all_switch() + threshold.get_all_threshold() + bind.get_all_bind()
	for i in range(len(l)):
		l[i]['id'] = i+1
	return l


def main_task():
	while True:
		while dns_queue.empty() is not True:
			data = dns_queue.get()
			task = loop.create_task(pub_conf(data))
			loop.run_until_complete(task)
		time.sleep(0.1)



def handle_query(data):
	try:
		data = data['contents'][0]
		res_msg = check_data(data, 'GET')
		if res_msg == 'true':
			res = handle_db_methods[data['bt']][data['sbt']][data['op']](data) if data['service'] == 'handle' else dns_db_methods[data['bt']][data['sbt']][data['op']](data)
			if res is not None:
				return res
			return {'rcode': 2, 'description': 'The database {} {} table has no data'.format(data['bt'],data['sbt'])}
		else:
			return {'rcode': 1, 'description': 'Request data format error:{}'.format(res_msg)}
	except Exception as e:
		logger.error(str(e))
		return {'rcode': 3, 'description': 'Server program error'}


def handle_data(data,method):
	if 'contents' in data:
		dns_list,handle_list = [],[]
		for i in data['contents']:
			res = check_data(i, method)
			if res == 'true':
				if i['service'] == 'dns':
					dns_queue.put(i)
				else:
					handle_list.append(i)
			elif res == 'done':
				conf_logger.info('conf success: data: {}'.format(data))
				content.add_oplog(i, 'success', '')
			else:
				conf_logger.info('conf failed: {} data: {}'.format(res,data))
				content.add_oplog(i, 'fail', res)
		if len(handle_list) > 0:
			contents = {'contents':handle_list}
			handle_queue.put(contents)


handle_db_methods = {
	'useripwhitelist': {
		'switch': handle.handle_switch_methods,
		'rules': handle.handle_ip_group_methods
	},
	'ipthreshold': {
		'switch': handle.handle_switch_methods,
		'rules': handle.ip_meter_methods
	}, 
	'handlethreshold': {
		'switch': handle.handle_switch_methods,
		'rules': handle.handle_tag_meter_methods
	}, 
	'srcipaccesscontrol': {
		'switch': handle.handle_switch_methods,
		'rules': handle.handle_ip_list_methods
	},
	'handleaccesscontrol': {
		'switch': handle.handle_switch_methods,
		'rules': handle.handle_tag_list_methods
	},
	'backend': {
		'forwardserver': handle.handle_forward_server_methods
	},
	'businessservice': {
		'switch': handle.handle_switch_methods
	},
	'businessproto': {
		'rules': handle.handle_proto_methods
	},
	'certificate': {
		'rules': handle.handle_ca_methods
	},
	'xforce':{
		'switch': handle.handle_switch_methods,
		'rules': handle.handle_xforce_methods
	},
	'cachesmartupdate': {
		'switch': handle.handle_switch_methods
	},
	'cacheprefetch':{
		'switch': handle.handle_switch_methods,
		'rules': handle.handle_tag_list_methods
	},
	'selfcheck': {
		'switch': handle.handle_switch_methods,
		'blackqtype': handle.handle_string_methods,
		'responserules': handle.selfcheck_response_methods
	},
	'backendmeter': {
		'switch': handle.handle_switch_methods,
		'rules': handle.total_meter_methods
	},
	'stub': {
		'rules': handle.handle_stub_methods
	},
	'healthdetect':{
		'config': handle.handle_health_methods
	},
	'loadbalance':{
		'algorithm': handle.loadbalance_methods
	},
	'trusted':{
		'switch': handle.handle_switch_methods
	}
}


async def conf_kernel(client,data):
	return [{'id':i['id'], 'status':'success', 'msg':''} for i in data['contents']]


async def conf_agent(url,client,data):
	try:
		async with client.post(url, json = data, timeout = 10) as resp:
			return await resp.json()
	except Exception as e:
		conf_logger.error(str(e))
	return [{'id':i['id'], 'status':'failed', 'msg':'send error'} for i in data['contents']]


def change_data(data):
	res = {}
	for i in data:
		res[i['id']] = i
	return res


def update_db(data,res):
	data = change_data(data)	
	res = change_data(res)	
	for i in data:
		if i in res:
			content.add_oplog(data[i], res[i]['status'], res[i]['msg'])
			if res[i]['status'] == 'success':
				handle_db_methods[data[i]['bt']][data[i]['sbt']][data[i]['op']](data[i])
				conf_logger.info('conf success: {}'.format(data[i]))
			else:
				conf_logger.info('conf failed: {}'.format(data[i]))
		else:
			content.add_oplog(data[i], 'failed', 'api return error')
			conf_logger.info('conf failed: {}'.format(data[i]))
		

def cmp_update_db(data,proxy_res,xforward_res):
	data = change_data(data)	
	proxy_res = change_data(proxy_res)	
	xforward_res = change_data(xforward_res)
	l = []
	for i in data:
		if i in xforward_res and i in proxy_res:
			if proxy_res[i]['status'] == 'success' and xforward_res[i]['status'] == 'success':
				content.add_oplog(data[i], 'success', '')
				handle_db_methods[data[i]['bt']][data[i]['sbt']][data[i]['op']](data[i])
				conf_logger.info('conf success: {}'.format(data[i]))
				l.append(proxy_res[i])
			elif proxy_res[i]['status'] != 'success' and xforward_res[i]['status'] == 'success':
				content.add_oplog(data[i], proxy_res[i]['status'], proxy_res[i]['msg'])
				conf_logger.info('conf failed: {}'.format(data[i]))
				l.append(proxy_res[i])
			elif proxy_res[i]['status'] == 'success' and xforward_res[i]['status'] != 'success':
				content.add_oplog(data[i], xforward_res[i]['status'], xforward_res[i]['msg'])
				conf_logger.info('conf failed: {}'.format(data[i]))
				l.append(xforward_res[i])
			else:
				content.add_oplog(data[i], 'failed', 'conf failed')
				conf_logger.info('conf failed: {}'.format(data[i]))
				l.append(xforward_res[i])
		else:
			content.add_oplog(data[i], 'failed', 'api return error')
			conf_logger.info('conf failed: {}'.format(data[i]))
			l.append({'id':i, 'status':'faild', 'msg':'api return error'})
	return l


async def pub_handle_conf(data):
	bt = data['contents'][0]['bt']
	async with aiohttp.ClientSession() as client:
		if (bt in proxy_bt and 'proxy' in crm_cfg and 'conf_url' in crm_cfg['proxy']) and (bt in xforward_bt and 'xforward' in crm_cfg and 'conf_url' in crm_cfg['xforward']):
			proxy_res = await conf_agent(crm_cfg['proxy']['conf_url'],client,data)
			xforward_res = await conf_agent(crm_cfg['xforward']['conf_url'],client,data)
			conf_logger.debug('recv data from proxy: {} xforward:{}'.format(proxy_res,xforward_res))
			return cmp_update_db(data['contents'],proxy_res,xforward_res)
		if bt in proxy_bt and 'proxy' in crm_cfg and 'conf_url' in crm_cfg['proxy']:
			res = await conf_agent(crm_cfg['proxy']['conf_url'],client,data)
			conf_logger.debug('recv data from proxy: {}'.format(res))
			update_db(data['contents'],res)
			return res
		elif bt in xforward_bt and 'xforward' in crm_cfg and 'conf_url' in crm_cfg['xforward']:
			res = await conf_agent(crm_cfg['xforward']['conf_url'],client,data)
			conf_logger.debug('recv data from xforward: {}'.format(res))
			update_db(data['contents'],res)
			return res
		elif bt in recursion_bt and 'recursion' in crm_cfg and 'conf_url' in crm_cfg['recursion']:
			res = await conf_agent(crm_cfg['recursion']['conf_url'],client,data)
			conf_logger.debug('recv data from recursion: {}'.format(res))
			update_db(data['contents'],res)
			return res
		elif bt in kernel_bt:
			res = [{'id':i['id'], 'status':'success', 'msg':''} for i in data['contents']]
			update_db(data['contents'],res)
			return res
		else:
			res = [{'id':i['id'], 'status':'failed', 'msg':'no module register or conf url error'} for i in data['contents']]
			update_db(data['contents'],res)
			return res

	

def handle_sync_data(data,method):
	if 'contents' in data:
		dns_list,handle_list,result = [],[],[]
		for i in data['contents']:
			res = check_data(i, method)
			if res == 'true':
				if i['service'] == 'dns':
					#dns_list.append(i)
					dns_queue.put(i)
				else:
					handle_list.append(i)
			elif res == 'done':
				conf_logger.info('conf success: data: {}'.format(data))
				content.add_oplog(i, 'success', '')
				r = {'id':i['id'], 'status': 'success', 'description': 'conf success'}
				result.append(r)
			else:
				conf_logger.info('conf failed: {} data: {}'.format(res,data))
				content.add_oplog(i, 'fail', res)
				r = {'id':i['id'], 'status': 'fail', 'description': res}
				result.append(r)
		if len(handle_list) > 0:
			task = sync_loop.create_task(pub_handle_conf({'contents':handle_list}))
			sync_loop.run_until_complete(task)
			res = task.result()
			return json.dumps(result+res),200,{"Content-Type":"application/json"}



def handle_main_task():
	while True:
		while handle_queue.empty() is not True:
			data = handle_queue.get()
			task = handle_loop.create_task(pub_handle_conf(data))
			handle_loop.run_until_complete(task)
		time.sleep(0.1)


def gen_conf(l):
	for i in range(len(l)):
		l[i]['id'] = i+1
	return l


def get_url(data,ip):
	url = {}
	ip = ip[7:] if '::ffff:' == ip[:7] else ip
	url['ip'] = ip
	url['port'] = data['port']
	url['conf_url'] = 'http://{}:{}{}'.format(ip,data['port'],data['conf_url'])
	url['task_url'] = 'http://{}:{}{}'.format(ip,data['port'],data['task_url'])
	return url


def handle_register(source,data,ip):
	if source == 'ms':
		return {'contents': gen_conf(handle.get_all_handle())}
	elif source == 'proxy':
		crm_cfg['proxy'] = get_url(data,ip)
		register.put_register('proxy',crm_cfg['proxy'])
		conf_logger.info('proxy register: {}'.format(crm_cfg['proxy']))
		return {'contents': gen_conf(handle.get_all_proxy_handle())}
	elif source == 'xforward':
		crm_cfg['xforward'] = get_url(data,ip)
		register.put_register('xforward',crm_cfg['xforward'])
		conf_logger.info('xforward register: {}'.format(crm_cfg['xforward']))
		return {'contents': gen_conf(handle.get_all_xforward_handle())}
	elif source == 'recursion':
		crm_cfg['recursion'] = get_url(data,ip)
		register.put_register('recursion',crm_cfg['recursion'])
		conf_logger.info('recursion register: {}'.format(crm_cfg['recursion']))
		return {'contents': gen_conf(handle.get_all_recursion_handle())}


# 心跳测试
def beat_connect(ip,port):
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(5)
		sock.connect((ip, port))
		sock.close()
		return True
	except Exception as e:
		conf_logger.error(str(e))
	return False


#后续加入定时模块
def beat_main_task():
	d = register.get_all_register()
	if d is not None:
		for k in d:
			crm_cfg[k] = d[k]
			conf_logger.info('load register {}:{}'.format(k,d[k]))
	while True:
		#print(crm_cfg)
		if 'proxy' in crm_cfg and beat_connect(crm_cfg['proxy']['ip'],crm_cfg['proxy']['port']) == False:
			register.del_register('proxy')
			conf_logger.info('del register proxy:{}'.format(crm_cfg['proxy']))
			del crm_cfg['proxy']
		if 'xforward' in crm_cfg and beat_connect(crm_cfg['xforward']['ip'],crm_cfg['xforward']['port']) == False:
			register.del_register('xforward')
			conf_logger.info('del register xforward:{}'.format(crm_cfg['xforward']))
			del crm_cfg['xforward']
		if 'recursion' in crm_cfg and beat_connect(crm_cfg['recursion']['ip'],crm_cfg['recursion']['port']) == False:
			register.del_register('recursion')
			conf_logger.info('del register recursion:{}'.format(crm_cfg['recursion']))
			del crm_cfg['recursion']
		time.sleep(30)


#后续加入定时模块
def task_main_task():
	while True:
		while task_queue.empty() is not True:
			data = task_queue.get()
			do_task(data)
		time.sleep(1)


def init_thread():	
	#threading._start_new_thread(base.main_task,())
	#threading._start_new_thread(base.handle_main_task,())
	#threading._start_new_thread(base.beat_main_task,())
	#threading._start_new_thread(base.task_main_task,())
	threading._start_new_thread(main_task,())
	threading._start_new_thread(handle_main_task,())
	threading._start_new_thread(beat_main_task,())
	threading._start_new_thread(task_main_task,())


'''
def timer_task():
	# 定时归并oplog 去重 备份 等
	schedule.every().day.at("24:00").do(timer_job)
	schedule.every(1).minutes.do(job,'good')
	schedule.every(4).hour.do(job, name)
	while True:
		schedule.run_pending()
		time.sleep(1)
'''





