
async def conf_fpga(client,data):
	try:
		# 此处处理data 转换成fpga_agent需要的格式 然后发给fpga_agent
		async with client.post(crm_cfg['fpga']['url'], json = data, timeout = 10) as resp:
			#return await resp.json()
			return await resp.text()
	except Exception as e:
		logger.error(str(e))
	return ''


async def conf_ybind(client,data):
	try:
		# 此处处理data 转换成ybind需要的格式 然后发给ybind ybind的url接口比较丰富，此处需要根据不同数据请求不同url
		#async with client.post('http://192.168.5.41:9999/post', json = data, timeout = 10) as resp:
		async with client.post('http://{}:{}/'.format(crm_cfg['ybind']['ip'],crm_cfg['ybind']['port']), json = data, timeout = 10) as resp:
		#async with client.post('http://192.168.5.41:9000/', json = data) as resp:
			#return await resp.text()
			return await resp.json()
	except Exception as e:
		logger.error(str(e))
	return ''


def pub_conf_callback(future):
	print(future.result())


async def pub_conf(data):
	# 此处需要根据配置类型看是否要ybind和fpga都要下发还是其中之一需要下发
	async with aiohttp.ClientSession() as client:
		fpga_result = await conf_fpga(client,data)
		#print(fpga_result)
		ybind_result = await conf_ybind(client,data)
		#此处判断fpga_agent和ybind是否都返回成功，都成功则将真实数据存入数据库，记录oplog，后续定时模块线程会定期将成功的oplog归并，并将已同步的oplog删除。
		print(fpga_result,ybind_result)
		content.add_oplog(data['contents'][0], 'success', '')
		#return {'fpga': fpga_result, 'ybind': ybind_result}


def main_task():
	while True:
		while task_queue.empty() is not True:
			data = task_queue.get()
			task = loop.create_task(pub_conf(data))
			#task.add_done_callback(pub_conf_callback)
			loop.run_until_complete(task)
		'''
		#此处可阻塞接受一个信号，即队列里有数据了 
		size = task_queue.qsize()
		if size > 100:
			tasks = []
			for i in range(100):
				data = task_queue.get()
				task = loop.create_task(pub_conf(data))
				tasks.append(task)
			loop.run_until_complete(asyncio.wait(tasks))
			continue
		elif size > 0:
			tasks = []
			while task_queue.empty() is not True:
				data = task_queue.get()
				task = loop.create_task(pub_conf(data))
				task.add_done_callback(pub_conf_callback)
				tasks.append(task)
			loop.run_until_complete(asyncio.wait(tasks))
		'''
		time.sleep(0.1)
		#print('--------------------------')
	

