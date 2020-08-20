import aiohttp,time
import asyncio,json
from datetime import datetime



async def fetch1(client):
	data = {'cc': '33', 'dd': '44'}
	try:
		#async with client.post('http://192.168.5.41:9000/post', data = json.dumps(data), timeout = 3) as resp:
		async with client.post('http://192.168.5.41:9000/', data = data) as resp:
			return await resp.text()
	except Exception as e:
		#print(e)
		return str(e)


async def fetch(client):
	data = {'aa': '11', 'bb': '22'}
	try:
		#async with client.post('http://192.168.5.41:9000/', json = data, timeout = 2) as resp:
		async with client.post('http://192.168.5.41:9000/', data = data) as resp:
			return await resp.json()
	except Exception as e:
		#print(e)
		return str(e)

async def main():
	async with aiohttp.ClientSession() as client:
		html = await fetch(client)
		#html1 = await fetch1(client)
		print(html,type(html),html=='')
		#print(html1)

loop = asyncio.get_event_loop()

tasks = []
for i in range(1):
	task = loop.create_task(main())
	tasks.append(task)
	print(len(tasks))

print(len(tasks))

start = datetime.now()

loop.run_until_complete(main())

end = datetime.now()

print("aiohttp版爬虫花费时间为：")
print(end - start)
