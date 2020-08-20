#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, unicode_literals, print_function, nested_scopes
import datetime
import logging
import os
import platform
import socket
import sys
import time
from netconf import error, server, util
from netconf import nsmap_add, NSMAP

from lxml import etree
import json,xmltodict

import asyncio,queue
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers

async def run(loop,data):
	nc = NATS()
	await nc.connect("192.168.66.151:4222", loop=loop)
		
	await nc.publish("foo", data.encode())

	try:
		response = await nc.request("fun", data.encode(), timeout=5)
		print("Received response: {message}".format(message=response.data.decode()))
	except ErrTimeout:
		print("Request timed out")

	await nc.close()


nsmap_add("sys", "urn:ietf:params:xml:ns:yang:ietf-system")

def date_time_string(dt):
    tz = dt.strftime("%z")
    s = dt.strftime("%Y-%m-%dT%H:%M:%S.%f")
    if tz:
        s += " {}:{}".format(tz[:-2], tz[-2:])
    return s


class SystemServer(object):
	def __init__(self, port, host_key, auth, debug):
		self.server = server.NetconfSSHServer(auth, self, port, host_key, debug)

	def close():
		self.server.close()

	def nc_append_capabilities(self, capabilities):  # pylint: disable=W0613
		"""The server should append any capabilities it supports to capabilities"""
		util.subelm(capabilities,"capability").text = "urn:ietf:params:netconf:capability:xpath:1.0"
		util.subelm(capabilities, "capability").text = NSMAP["sys"]

	def _add_config (self, data):
		sysc = util.subelm(data, "sys:system")
		
		# System Identification
		sysc.append(util.leaf_elm("sys:hostname", socket.gethostname()))
		
		# System Clock
		clockc = util.subelm(sysc, "sys:clock")
		tzname = time.tzname[time.localtime().tm_isdst]
		clockc.append(util.leaf_elm("sys:timezone-utc-offset", int(time.timezone / 100)))

	def rpc_get(self, session, rpc, filter_or_none):  # pylint: disable=W0613
		"""Passed the filter element or None if not present"""
		data = util.elm("nc:data")
		
		self._add_config(data)

		#
		# State Data
		#
		sysd = util.subelm(data, "sys:system-state")

		# System Identification
		platc = util.subelm(sysd, "sys:platform")
		platc.append(util.leaf_elm("sys:os-name", platform.system()))
		platc.append(util.leaf_elm("sys:os-release", platform.release()))
		platc.append(util.leaf_elm("sys:os-version", platform.version()))
		platc.append(util.leaf_elm("sys:machine", platform.machine()))

		# System Clock
		clockc = util.subelm(sysd, "sys:clock")
		now = datetime.datetime.now()
		clockc.append(util.leaf_elm("sys:current-datetime", date_time_string(now)))

		if os.path.exists("/proc/uptime"):
			with open('/proc/uptime', 'r') as f:
				uptime_seconds = float(f.readline().split()[0])
			boottime = time.time() - uptime_seconds
			boottime = datetime.datetime.fromtimestamp(boottime)
			clockc.append(util.leaf_elm("sys:boot-datetime", date_time_string(boottime)))

		return util.filter_results(rpc, data, filter_or_none, self.server.debug)

	def rpc_get_config(self, session, rpc, source_elm, filter_or_none):  # pylint: disable=W0613
		print('rpc--->',rpc,type(rpc))
		print('source_elm--->',source_elm,type(source_elm))
		print('filter_or_none--->',filter_or_none,type(filter_or_none))
		"""Passed the source element"""
		data = util.elm("nc:data")
		print(data,type(data))
		print(etree.tostring(data, pretty_print=True).decode())
		#
		# Config Data
		#
		self._add_config(data)
		return util.filter_results(rpc, data, filter_or_none)
    
	def rpc_edit_config(self, unused_session, rpc, *unused_params):
		try:
			print("quitting server")
			print('rpc--->',rpc,type(rpc))
			print(json.dumps(xmltodict.parse(etree.tostring(rpc, pretty_print=True).decode(),encoding='utf-8'),indent=4))
			print('unused_session--->',unused_session,type(unused_session))
			print('unused_params--->',unused_params,type(unused_params))
		except Exception as e:
			print(e)
		return '<res>\nok\n</res>\n'

	def rpc_system_restart(self, session, rpc, *params):
		raise error.AccessDeniedAppError(rpc)

	def rpc_system_shutdown(self, session, rpc, *params):
		raise error.AccessDeniedAppError(rpc)


if __name__ == "__main__":
	conf = {
		'host_key':'/home/heweiwei/.ssh/id_rsa',
		'port': 8300,
		'username': 'heweiwei',
		'password': '123',
		'debug': True
	}
	
	print(conf)
	
	auth = server.SSHUserPassController(username = conf['username'], password = conf['password'])
	s = SystemServer(conf['port'], conf['host_key'], auth, conf['debug'])
    
	loop = asyncio.get_event_loop()
	q = queue.Queue()
	#loop.run_forever()
	
	while True:            
		try:
			q.put('hello heweiwei')
			q.put('hello maonini')
			while q.empty() == False:
				loop.run_until_complete(run(loop,q.get()))
			time.sleep(5)    
		except Exception as e:        
			time.sleep(5)    
			print("quitting server",e)
    
	loop.close()
	s.close()

