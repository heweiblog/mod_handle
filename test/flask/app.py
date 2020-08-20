#!/usr/bin/python
# -*- coding: utf-8 -*-

import time,json,datetime
from flask import Flask,request,escape

app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello, World!'

@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
	if request.method == 'POST':
		#return 'Post %d' % post_id
		return json.dumps(gen_result('0'))
	elif request.method == 'GET':
		#return 'Get %d' % post_id
		return json.dumps(gen_result('1'))

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
			print(jsonData)
			#print(type(jsonData))
			
			command_func = {1:handle_type_1}

			if intfId in command_func:
				return command_func[intfId](orgId,jsonData)            
			else:                
				print('unsupported intfId : {} \nrequestData : {}'.format(intfId,jsonData))  
		return json.dumps(gen_result('5'))    
	except Exception as e:
		print(e)
		return json.dumps(gen_result('1'))

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080, debug=False)

