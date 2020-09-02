#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading,json,requests,asyncio,aiohttp
from common.conf import crm_cfg
from common.log import logger
from common.check import check_task
from models.task import task_list_methods

task_loop = asyncio.get_event_loop()


def handle_task_delete(task_id):
	try:
		task_list_methods['delete'](task_id)
	except Exception as e:
		logger.error(str(e))
	return {"description": "Success","rcode": 0}


def handle_task_query(task_id):
	try:
		res = task_list_methods['query'](task_id)
		if res is not None:
			return res
		return {'rcode': 2, 'description': 'not exist task id {}'.format(task_id)}
	except Exception as e:
		logger.error(str(e))
	return {'rcode': 3, 'description': 'Server program error'}


async def task_proxy_xforward(url,client,data):
	try:
		async with client.post(url, json = data, timeout = 10) as resp:
			return await resp.json()
	except Exception as e:
		logger.error(str(e))
		return {'rcode': 1, 'msg': str(e), 'status':'error'}
	return {'rcode': 2, 'msg': 'unknown error', 'status':'error'}
	

async def task_kernel(client,data):
	try:
		return {'rcode': 2, 'description': 'success', 'status':'complete', 'result':''}
	except Exception as e:
		logger.error(str(e))
	return {'rcode': 2, 'description': 'do task failed', 'status':'complete', 'result':''}


async def pub_task(data):
	async with aiohttp.ClientSession() as client:
		proxy_res = await task_proxy_xforward(crm_cfg['proxy']['task_url'],client,data)
		xforward_res = await task_proxy_xforward(crm_cfg['xforward']['task_url'],client,data)
		logger.debug('recv task result from xforward:{} proxy:{}'.format(xforward_res,proxy_res))
		try:
			if proxy_res['status'] == 'success' and xforward_res['status'] == 'success':
				logger.info('do task success data:{}'.format(data))
				if data['contents'][0]['tasktype'] == 'cachequery':
					proxy_res['msg']['udp'] = xforward_res['msg']
					return {'rcode': 0, 'description': 'success', 'status':'complete', 'result': proxy_res['msg']}
				return {'rcode': 0, 'description': 'success', 'status':'complete', 'result':''}
			elif proxy_res['status'] == 'success' and xforward_res['status'] != 'success':
				logger.info('xforward do task failed:{} data:{}'.format(xforward_res,data))
				return {'rcode': 1, 'description': 'proxy success and xforward failed with {}'.format(xforward_res['msg']), 'status':'complete', 'result':''}
			elif proxy_res['status'] != 'success' and xforward_res['status'] == 'success':
				logger.info('proxy do task failed:{} data:{}'.format(proxy_res,data))
				return {'rcode': 1, 'description': 'xforward success and proxy failed with {}'.format(proxy_res['msg']), 'status':'complete', 'result':''}
			else:
				logger.info('do task failed proxy:{} xforward:{} data:{}'.format(proxy_res,xforward_res,data))
				return {'rcode': 1, 'description': 'xforward failed:{} and proxy failed:{}'.format(xforward_res['msg'],proxy_res['msg']), 'status':'complete', 'result':''}
		except Exception as e:
			logger.error(str(e))
		return {'rcode': 2, 'description': 'do task failed', 'status':'complete', 'result':''}
			
	
def do_task(data,task_id):
	task = task_loop.create_task(pub_task(data))
	task_loop.run_until_complete(task)
	res = task.result()
	task_list_methods['update'](task_id,res)


def handle_task(data):
	try:
		dat = data['contents'][0]
		res = check_task(dat)
		if res == 'true':
			task_id = task_list_methods['add'](dat)
			if task_id > 0:
				threading._start_new_thread(do_task,(data,task_id))
				return {'description': 'recevied', 'rcode': 0, 'taskid':task_id}
		else:
			logger.warning('Request content format error:{} content:{}'.format(res,data))
			return {'rcode': 1, 'description': 'Request data format error:{}'.format(res)}
	except Exception as e:
		logger.error(str(e))
	return {'rcode': 2, 'description': 'Server program error'}
			

