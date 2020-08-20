#!/usr/bin/python3
# -*- coding: utf-8 -*-

import datetime,requests,json

def get_data():
	l = []
	for i in range(100000):
		l.append({'num':i,'ip':'1.1.1.'+str(i)})
	return l

def send_request():
	try:
		url = 'http://192.168.5.41:8080/1/2'
		requestData = {
			'orgId'         : '2',
			'intfId'        : '1',
			'timeStamp'		: datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
			'dataTag'       : '1',
			'data'          : get_data(),
		}
        
		headers = {
			"Accept-Charset": "utf-8",
			"Content-Type": "application/json"
		}   

		ret =requests.post(url, json.dumps(requestData), headers = headers, timeout=5)
		retData = json.loads(ret.text)
		print(ret,retData)
        
		if retData.get('errorCode') == '0':
			print('send to {} waj_dnsCommandAck success'.format(url))
		else:
			print('send to {} waj_dnsCommandAck error'.format(url))

	except Exception as e:
		print('send to {} waj_dnsCommandAck failed:{}'.format(url,e))

if __name__ == '__main__':
	send_request()
