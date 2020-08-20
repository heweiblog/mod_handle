#!/usr/bin/python
# -*- coding: utf-8 -*-

import click,pymysql,dns
from daemonocle.cli import DaemonCLI
import sys,json,threading,time,copy,asyncio,aiohttp
from flask import Flask,request,jsonify
from common.conf import crm_cfg
from common.log import logger
from common.pub import data_check
from models import db
from resources import base,task
from models import content

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(crm_cfg['db']['user'],\
crm_cfg['db']['passwd'],crm_cfg['db']['host'],crm_cfg['db']['port'],crm_cfg['db']['database'])
# 设置每次请求结束后会自动提交数据库的改动
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.app = app
db.init_app(app=app)
db.create_all()


# 配置查询
@app.route('/dnsys/v1.0/internal/configs', methods=['GET'])
@app.route('/dnsys/v1.0/internal/sync-configs', methods=['GET'])
def handle_get_request():
	try:
		data = data_check(request.get_json())
		if data is not None:
			res = json.dumps(base.handle_query(data))
			logger.info('query results: {}'.format(res))
			return res,200,{"Content-Type":"application/json"}
	except Exception as e:
		logger.error(str(e))
	return {'rcode': 1, 'description': 'Request data format error'}


# dns 配置下发 异步
@app.route('/dnsys/v1.0/internal/configs', methods=['POST','PUT','DELETE'])
def handle_post_request():
	try:
		data = data_check(request.get_json())
		if data is not None:
			base.handle_dns_data(data,request.method)
		else:
			return {'rcode': 1, 'description': 'Data format error cannot be handled'}
	except Exception as e:
		logger.error(str(e))
		return {'rcode': 1, 'description': 'Data format error cannot be handled'}
	return {'rcode': 0, 'description': 'Recevied'}


# handle配置查询
@app.route('/handle/v1.0/internal/configs', methods=['GET'])
def handle_handle_get_request():
	try:
		data = data_check(request.get_json())
		if data is not None:
			res = json.dumps(base.handle_handle_query(data))
			logger.info('query results: {}'.format(res))
			return res,200,{"Content-Type":"application/json"}
	except Exception as e:
		logger.error(str(e))
	return {'rcode': 1, 'description': 'Request data format error'}


# handle 配置下发 异步
@app.route('/handle/v1.0/internal/configs', methods=['POST','PUT','DELETE'])
def handle_handle_request():
	try:
		data = data_check(request.get_json())
		if data is not None:
			base.handle_handle_data(data,request.method)
		else:
			return {'rcode': 1, 'description': 'Data format error cannot be handled'}
	except Exception as e:
		logger.error(str(e))
		return {'rcode': 1, 'description': 'Data format error cannot be handled'}
	return {'rcode': 0, 'description': 'Recevied'}


# 配置下发 同步
@app.route('/dnsys/v1.0/internal/sync-configs', methods=['POST','PUT','DELETE'])
def handle_sync_request():
	try:
		data = data_check(request.get_json())
		if data is not None:
			return base.handle_sync_data(data,request.method)
	except Exception as e:
		logger.error(str(e))
	return {'rcode': 1, 'description': 'Data format error cannot be handled'}


# 任务下发
@app.route('/handle/v1.0/internal/tasks', methods=['POST','GET','DELETE'])
def handle_task_request():
	try:
		if request.method == 'POST':
			data = data_check(request.get_json())
			if data is not None:
				return task.handle_task(data)
		elif request.method == 'GET':
			task_id = request.args.get('taskid',type=int)
			if task_id is not None:
				return task.handle_task_query(task_id)
			return {'rcode': 2, 'description': 'Url parameters error taskID:{}'.format(task_id)}
		elif request.method == 'DELETE':
			task_id = request.args.get('taskid',type=int)
			if task_id is not None:
				return task.handle_task_delete(task_id)
			return {'rcode': 2, 'description': 'Url parameters error taskID:{}'.format(task_id)}
	except Exception as e:
		logger.error(str(e))
	return {'rcode': 1, 'description': 'Data format error cannot be handled'}



# 心跳检测
@app.route('/api/v1/internal/status', methods=['GET'])
def handle_heartbeat_request():
	ms_v,crm_v = content.get_version()
	return {'status':"running",'msRelease':'1','msVersion':ms_v,'deviceRelease': "1",'deviceVersion':crm_v,'softwareVersion':'1.0','licenseInfo':{'dev':'centos7','cpu':'i7-9700H'}}


# 增量传输
@app.route('/api/v1/internal/oplog', methods=['GET'])
def handle_add_download_request():
	try:
		version = request.args.get('startVersion',type=int) # 获得的是整数
		limit = request.args.get('limit',type=int)
		return content.get_oplogs(version,limit)
	except Exception as e:
		logger.error(str(e))
	return {}


# 全量传输
@app.route('/api/v1/internal/configs', methods=['GET'])
def handle_all_download_request():
	source = request.args.get('source')
	if source == 'ms':
		return {'contents':base.get_all_conf()}
	elif source == 'fpga':
		return {'contents':base.get_all_fpga_conf()}
	elif source == 'ybind':
		return {'contents':base.get_all_conf()}
	return {'rcode': 1, 'description': 'source parameter error cannot be handled'}


@app.route('/post', methods=['POST','GET','PUT','DELETE'])
def show():
	data = request.get_json()
	print(data)
	if 'contents' in data:
		return jsonify([{'id':1, 'status':'success', 'msg':''}])
	return jsonify({'rcode': 0, 'description': 'complete', 'status':'complete'})


@click.command(cls=DaemonCLI, daemon_params={'pidfile': '/var/hcrm/hcrm.pid'})
@click.option('-v',help='Show version and exit')
def main():
	threading._start_new_thread(base.main_task,())
	threading._start_new_thread(base.handle_main_task,())
	logger.error('hcrm start listen on {}:{}'.format(crm_cfg['net']['ip'],crm_cfg['net']['port']))
	app.run(host=crm_cfg['net']['ip'],port=int(crm_cfg['net']['port']),debug=False)


if __name__ == '__main__':
	if len(sys.argv) == 2 and (sys.argv[1] == '-v' or sys.argv[1] == 'version'):
		print('1.0.2')
		sys.exit(0)
	main()


