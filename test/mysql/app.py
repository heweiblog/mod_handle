#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import requests
from flask import Flask,request,escape,make_response
app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello, World!'

@app.route('/redirect/')
def redirect():
	return '/redirect/!'

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		return 'func do_the_login()'
	else:
		return {'user':'heweiwei', 'time':time.strftime('%Y-%m-%d %H:%M:%S'), 'location':'yanan'}

@app.route('/user/<username>', methods=['GET', 'POST'])
def show_user_profile(username):
	if request.method == 'POST':
		return 'POST User %s' % escape(username)
	elif request.method == 'GET':
		return 'GET User %s' % escape(username)

@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
	if request.method == 'POST':
		return 'Post %d' % post_id
	elif request.method == 'GET':
		return 'Get %d' % post_id

@app.route('/dns/auth', methods=['POST'])
def handerHttpRequest(intfId, orgId):
	try:
		if request.method == 'POST':
			jsonData = json.loads(request.get_data().decode('utf-8'))			
			print(jsonData)
	except Exception as e:
		pass

def sendHttpMessage():
	try:
		url = 'http://192.168.5.41:8080/'
		requestData = {
			'id'		: 1,
			'user'		: 'heweiwei',
			'email'		: 'ww.he@yamu.com',
		}
		headers = {
			"Accept-Charset": "utf-8",
			"Content-Type": "application/json"
		}   

		ret =requests.post(url, json.dumps(requestData), headers = headers)
		retData = json.loads(ret.text)
        
		if retData.get('errorCode') == '0':
			print('send to {} success'.format(url))
		else:
			print('send to {} error'.format(url))

	except Exception as e:
		print('send to {} failed:{}'.format(url,e))


if __name__ == '__main__':
	#print(make_response('hh'))
	app.run(host='192.168.5.41', port=8080, debug=False)
