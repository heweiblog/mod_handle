#!/usr/bin/python
# -*- coding: utf-8 -*-

import time,json,datetime
import requests
from flask import Flask,request,escape
import asyncio
from threading import Thread
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers

app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello, World!'

@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
	if request.method == 'POST':
		return 'Post %d' % post_id
	elif request.method == 'GET':
		return 'Get %d' % post_id

def gen_result(rcode):
	lookaside = {    
		'0' : '',    
		'1' : 'Failure for unknown reason',    
		'2' : 'Certification error',    
		'3' : 'Check failure',    
		'4' : 'De-compression error',    
		'5' : 'Format error',    
	}   
	result = {
		"errorCode"         : rcode,
		"errorMsg"          : lookaside[rcode],
		'timeStamp'			: datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
	}
	return result

def handle_type_1(orgId,jsonData):
	#print('handle',orgId,jsonData)
	return json.dumps(gen_result('0'))

#flask 处理https的入口函数
@app.route('/<int:intfId>/<int:orgId>', methods=['POST'])
def handele_dns_conf(intfId, orgId):
	try:
		if request.method == 'POST':
			#print('recv len = ',len(request.get_data()))
			jsonData = json.loads(request.get_data().decode('utf-8'))			
			print('recv waj cmd {}'.format(jsonData))
			
			command_func = {1:handle_type_1}

			if intfId in command_func:
				return command_func[intfId](orgId,jsonData)            
			else:                
				print('unsupported intfId : {} \nrequestData : {}'.format(intfId,jsonData))  
		return json.dumps(gen_result('5'))    
	except Exception as e:
		print(e)
		return json.dumps(gen_result('1'))


async def run(loop):
	nc = NATS()

	async def error_cb(e):
		print("Error:", e)

	async def closed_cb():
		print("Connection to NATS is closed.")
		await asyncio.sleep(0.1, loop=loop)
		loop.stop()

	async def reconnected_cb():
		print("Connected to NATS at {}...".format(nc.connected_url.netloc))

	async def subscribe_handler(msg):
		subject = msg.subject
		reply = msg.reply
		data = msg.data.decode()
		print("Received a message on '{subject} {reply}': {data}".format(
							   subject=subject, reply=reply, data=data))
		options = {
			"loop": loop,
			"error_cb": error_cb,
			"closed_cb": closed_cb,
			"reconnected_cb": reconnected_cb,
			"servers": ["nats://192.168.66.151:4222"],
		}


		try:
			await nc.connect(**options)
		except Exception as e:
			print(e)
			sys.exit(1)
		print('options---------->\n',options)

		print("Connected to NATS at {}...".format(nc.connected_url.netloc))
		def signal_handler():
			if nc.is_closed:
				return
			print("Disconnecting...")
			loop.create_task(nc.close())

			for sig in ('SIGINT', 'SIGTERM'):
				loop.add_signal_handler(getattr(signal, sig), signal_handler)

		await nc.subscribe("foo","",subscribe_handler)


def app_start():
	app.run(host='192.168.5.41', port=8080, debug=False)

if __name__ == '__main__':
	t = Thread(target=app_start)
	t.start()
	loop = asyncio.get_event_loop()
	loop.run_until_complete(run(loop))
	try:
		loop.run_forever()
	finally:
		loop.close()

