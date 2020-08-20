#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading,json,requests,asyncio,aiohttp
from common.conf import crm_cfg
from common.log import logger
from common.check import check_task
from models.proto import task_list_methods

task_loop = asyncio.get_event_loop()

def task_map(data):
	if data['tasktype'] == 'globalcachebackup':
		url = 'http://{}:{}/api/kernel/v1.0/cache/backups'.format(crm_cfg['kernel']['ip'],crm_cfg['kernel']['port'])
		data = {'filePath':data['data']['file'], 'cacheType':'all'}
		return 'post',url,data
	elif data['tasktype'] == 'globalcacheimport':
		pass
		#接口不一致
	elif data['tasktype'] == 'viewcachebackup':
		url = 'http://{}:{}/api/kernel/v1.0/cache/backups'.format(crm_cfg['kernel']['ip'],crm_cfg['kernel']['port'])
		data = {'view':data['data']['view'], 'filePath':data['data']['file'], 'cacheType':'cache'}
		return 'post',url,data
	elif data['tasktype'] == 'viewcacheimport':
		pass
		#接口不一致
	elif data['tasktype'] == 'cachedelete':
		pass
	elif data['tasktype'] == 'cachequery':
		pass
	


def handle_task_delete(task_id):
	try:
		task_list_methods['delete'](task_id)
	except Exception as e:
		logger.error(str(e))
	return {"description": "Recevied","rcode": 0}



def handle_task_query(task_id):
	try:
		res = task_list_methods['query'](task_id)
		if res is not None:
			return res
		return {'rcode': 2, 'description': 'not exist task_id {}'.format(task_id)}
	except Exception as e:
		logger.error(str(e))
	return {'rcode': 3, 'description': 'Server program error'}


async def task_proxy(client,data):
	try:
		async with client.post(crm_cfg['proxy']['url'], json = data, timeout = 10) as resp:
			return await resp.json()
	except Exception as e:
		logger.error(str(e))
		return {'rcode': 1, 'description': str(e), 'status':'error'}
	return {'rcode': 2, 'description': 'unknown error', 'status':'error'}
	

async def task_kernel(client,data):
	try:
		#method,url,y_data = task_map(data)
		#async with client.post(url, json = y_data, timeout = 10) as resp:
		# 映射kernel接口 根据返回method判断 请求方法
		async with client.post(crm_cfg['proxy']['url'], json = data, timeout = 10) as resp:
			return await resp.json()
	except Exception as e:
		logger.error(str(e))
		return {'rcode': 1, 'description': str(e), 'status':'error'}
	return {'rcode': 2, 'description': 'unknown error', 'status':'error'}


async def pub_task(data):
	async with aiohttp.ClientSession() as client:
		proxy_res = await task_proxy(client,data)
		kernel_res = await task_kernel(client,data)
		logger.debug('recv task result from kernel:{} proxy:{}'.format(kernel_res,proxy_res))
		try:
			if proxy_res['status'] == 'complete' and kernel_res['status'] == 'complete':
				logger.info('do task complete data:{}'.format(data))
				return {'rcode': 0, 'description': 'complete', 'status':'complete'}
			elif proxy_res['status'] == 'complete' and kernel_res['status'] != 'complete':
				logger.info('kernel do task failed:{} data:{}'.format(kernel_res,data))
				return kernel_res
			elif proxy_res['status'] != 'complete' and kernel_res['status'] == 'complete':
				logger.info('proxy do task failed:{} data:{}'.format(proxy_res,data))
				return proxy_res
			else:
				logger.info('do task failed proxy:{} kernel:{} data:{}'.format(proxy_res,kernel_res,data))
				return {'rcode': 1, 'description': 'do task failed proxy:{} kernel:{}'.format(proxy_res['description'],kernel_res['description']), 'status':'error'}
		except Exception as e:
			logger.error(str(e))
			return {'rcode': 2, 'description': 'task api return result error', 'status':'error'}
			
	
def do_task(data,task_id):
	task = task_loop.create_task(pub_task(data))
	task_loop.run_until_complete(task)
	res = task.result()
	task_list_methods['update'](task_id,res)


def handle_task(data):
	try:
		data = data['contents'][0]
		print(data)
		res = check_task(data)
		print(res)
		if res == 'true':
			task_id = task_list_methods['add'](data)
			if task_id > 0:
				threading._start_new_thread(do_task,(data,task_id))
				return {'description': 'Recevied', 'rcode': 0, 'taskID':task_id}
		else:
			logger.warning('Request content format error:{} content:{}'.format(res,data))
			return {'rcode': 1, 'description': 'Request data format error:{}'.format(res)}
	except Exception as e:
		logger.error(str(e))
	return {'rcode': 3, 'description': 'Server program error'}
			

