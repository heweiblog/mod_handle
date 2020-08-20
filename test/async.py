import time,datetime,json
import asyncio,requests

now = lambda : time.time()

async def do_some_work(x):
    #print("Waiting:",x)
    #await asyncio.sleep(x)
    #return "Done after {}s".format(x)
	try:
		#url = 'http://192.168.5.41:8080/1/2'
		url = 'http://192.168.5.41:9999/'
		#url = 'http://192.168.66.151:8080/1/2'
		requestData = {'content':[{
			'orgId'         : '2',
			'intfId'        : '1',
			'timeStamp'		: datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
			'dataTag'       : '1',
			'data'          : {'name':'heweiwei','city':'shanghai'},
		}],
		'www':1
		}
        
		headers = {
			"Accept-Charset": "utf-8",
			"Content-Type": "application/json"
		}   

		ret =requests.post(url, json.dumps(requestData), headers = headers, timeout=5)
		retData = json.loads(ret.text)
		print(ret,retData)
        
		'''
		if retData.get('errorCode') == '0':
			print('send to {} waj_dnsCommandAck success'.format(url))
		else:
			print('send to {} waj_dnsCommandAck error'.format(url))
		'''
	except Exception as e:
		print('send to {} waj_dnsCommandAck failed:{}'.format(url,e))


start = now()

tasks = []

for i in range(100):
	coroutine1 = do_some_work(1)
	tasks.append(asyncio.ensure_future(coroutine1))

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))

print("Time:",now()-start)
