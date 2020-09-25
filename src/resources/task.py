#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading,json,requests,asyncio,aiohttp
from common.conf import crm_cfg
from common.log import logger
from common.check import check_task
from common.queue import task_queue
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


async def task_send(url,client,data):
	try:
		async with client.post(url, json = data, timeout = 600) as resp:
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


async def pub_proxy_task(data):
	async with aiohttp.ClientSession() as client:
		proxy_res = await task_send(crm_cfg['proxy']['task_url'],client,data)
		logger.debug('recv task result from proxy:{}'.format(proxy_res))
		try:
			if proxy_res['status'] == 'success':
				logger.info('do task success data:{}'.format(data))
				if data['contents'][0]['tasktype'] == 'cachequery':
					return {'rcode': 0, 'description': 'success', 'status':'complete', 'result': proxy_res['msg']}
				return {'rcode': 0, 'description': 'success', 'status':'complete', 'result':''}
			logger.info('do task failed proxy:{} data:{}'.format(proxy_res,data))
			return {'rcode': 1, 'description': 'proxy do task failed:{}'.format(proxy_res['msg']), 'status':'complete', 'result':''}
		except Exception as e:
			logger.error(str(e))
		return {'rcode': 2, 'description': 'do task failed', 'status':'complete', 'result':''}
			

async def pub_xforward_task(data):
	async with aiohttp.ClientSession() as client:
		xforward_res = await task_send(crm_cfg['xforward']['task_url'],client,data)
		logger.debug('recv task result from xforward:{}'.format(xforward_res))
		try:
			if xforward_res['status'] == 'success':
				logger.info('do task success data:{}'.format(data))
				if data['contents'][0]['tasktype'] == 'cachequery':
					return {'rcode': 0, 'description': 'success', 'status':'complete', 'result': xforward_res['msg']}
				return {'rcode': 0, 'description': 'success', 'status':'complete', 'result':''}
			logger.info('do task failed xforward:{} data:{}'.format(xforward_res,data))
			return {'rcode': 1, 'description': 'xforward do task failed:{}'.format(xforward_res['msg']), 'status':'complete', 'result':''}
		except Exception as e:
			logger.error(str(e))
		return {'rcode': 2, 'description': 'do task failed', 'status':'complete', 'result':''}
			

async def pub_task(data):
	async with aiohttp.ClientSession() as client:
		proxy_res = await task_send(crm_cfg['proxy']['task_url'],client,data)
		xforward_res = await task_send(crm_cfg['xforward']['task_url'],client,data)
		logger.debug('recv task result from xforward:{} proxy:{}'.format(xforward_res,proxy_res))
		try:
			if proxy_res['status'] == 'success' and xforward_res['status'] == 'success':
				logger.info('do task success data:{}'.format(data))
				if data['contents'][0]['tasktype'] == 'cachequery':
					proxy_res['msg']['udp'] = xforward_res['msg']['udp']
					return {'rcode': 0, 'description': 'success', 'status':'complete', 'result': proxy_res['msg']}
				return {'rcode': 0, 'description': 'success', 'status':'complete', 'result':''}
			elif proxy_res['status'] == 'success' and xforward_res['status'] != 'success':
				logger.info('xforward do task failed:{} data:{}'.format(xforward_res,data))
				if data['contents'][0]['tasktype'] == 'cachequery':
					return {'rcode': 0, 'description': 'success', 'status':'complete', 'result': proxy_res['msg']}
				return {'rcode': 1, 'description': 'proxy success and xforward failed with {}'.format(xforward_res['msg']), 'status':'complete', 'result':''}
			elif proxy_res['status'] != 'success' and xforward_res['status'] == 'success':
				logger.info('proxy do task failed:{} data:{}'.format(proxy_res,data))
				if data['contents'][0]['tasktype'] == 'cachequery':
					return {'rcode': 0, 'description': 'success', 'status':'complete', 'result': xforward_res['msg']}
				return {'rcode': 1, 'description': 'xforward success and proxy failed with {}'.format(proxy_res['msg']), 'status':'complete', 'result':''}
			else:
				logger.info('do task failed proxy:{} xforward:{} data:{}'.format(proxy_res,xforward_res,data))
				return {'rcode': 1, 'description': 'xforward failed:{} and proxy failed:{}'.format(xforward_res['msg'],proxy_res['msg']), 'status':'complete', 'result':''}
		except Exception as e:
			logger.error(str(e))
		return {'rcode': 2, 'description': 'do task failed', 'status':'complete', 'result':''}
			
	
def do_task(data):
	task_id = data['id']
	del data['id']
	if 'proxy' in crm_cfg and 'xforward' in crm_cfg:
		task = task_loop.create_task(pub_task(data))
		task_loop.run_until_complete(task)
		res = task.result()
		task_list_methods['update'](task_id,res)
	elif 'proxy' in crm_cfg:
		task = task_loop.create_task(pub_proxy_task(data))
		task_loop.run_until_complete(task)
		res = task.result()
		task_list_methods['update'](task_id,res)
	elif 'xforward' in crm_cfg:
		task = task_loop.create_task(pub_xforward_task(data))
		task_loop.run_until_complete(task)
		res = task.result()
		task_list_methods['update'](task_id,res)
	else:
		res = {'rcode': 2, 'description': 'do task failed because no module register', 'status':'complete', 'result':''}
		task_list_methods['update'](task_id,res)


def handle_task(data):
	try:
		dat = data['contents'][0]
		res = check_task(dat)
		if res == 'true':
			task_id = task_list_methods['add'](dat)
			if task_id > 0:
				data['id'] = task_id
				task_queue.put(data)
				return {'description': 'recevied', 'rcode': 0, 'taskid':task_id}
			return {'rcode': 3, 'description': 'repetitive task the task is running'}
		else:
			logger.warning('Request content format error:{} content:{}'.format(res,data))
			return {'rcode': 1, 'description': 'Request data format error:{}'.format(res)}
	except Exception as e:
		logger.error(str(e))
	return {'rcode': 2, 'description': 'Server program error'}
			



