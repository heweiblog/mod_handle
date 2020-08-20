#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

db_switch = {
	'iptables': {
		'switch': 'disable'
	},
	'dnsipfragment': {
		'switch': 'disable'
	},
	'ipfragment': {
		'switch': 'disable'
	},
	'icmpflood': {
		'switch': 'disable'
	},
	'tcpflood': {
		'switch': 'disable'
	},
	'creditdname': {
		'switch': 'disable'
	},
	'ipthreshold': {
		'switch': 'disable'
	},
	'domainthreshold': {
		'switch': 'disable'
	},
	'ipdomainthreshold': {
		'switch': 'disable'
	},
	'poisonprotect': {
		'switch': 'disable',
		'x20': 'disable',
		'linkage': 'disable'
	},
	'amplificationattack': {
		'switch': 'disable'
	},
	'useripwhitelist': {
		'switch': 'disable'
	},
	'serviceipwhitelist': {
		'switch': 'disable'
	},
	'srcipaccesscontrol': {
		'switch': 'disable'
	},
	'domainaccesscontrol': {
		'switch': 'disable'
	},
	'ipdomainaccesscontrol': {
		'switch': 'disable'
	},
	'domainqtypeaccesscontrol': {
		'switch': 'disable'
	},
	'qtypeaccesscontrol': {
		'switch': 'disable'
	},
	'ipqtypeaccesscontrol': {
		'switch': 'disable'
	},
	'graydomainaccesscontrol': {
		'switch': 'disable'
	},
	'importdnameprotect': {
		'switch': 'disable'
	},
	'spreadecho': {
		'switch': 'disable'
	},
	'dts': {
		'switch': 'disable'
	},
	'expiredactivate': {
		'switch': 'disable'
	},
	'cachedisable': {
		'switch': 'disable'
	},
	'cachesync': {
		'switch': 'disable'
	},
	'minimalresponses': {
		'switch': 'disable'
	},
	'smartupdate': {
		'switch': 'disable'
	}
}

db_threshold = {
	'icmpflood': {
		'ipv4totalthreshold': 100,
		'ipv6totalthreshold': 100,
	},
	'tcpflood': {
		'ipv4totalthreshold': 100,
		'ipv6totalthreshold': 100,
		'ipv4no53threshold': 100,
		'ipv6no53threshold': 100
	},
	'udpflood': {
		'ipv4no53threshold': 100,
		'ipv6no53threshold': 100
	},
	'creditdname': {
		'totalthreshold': 1000,
	},
	'ipthreshold': {
		'defaultthreshold': 1000 
	},
	'backendthreshold': {
		'updatethreshold': 1000,
		'ipv4nohitthreshold': 1000,
		'ipv6nohitthreshold': 1000,
	},
	'replythreshold': {
		'replythreshold': 1000
	},
	'amplificationattack': {
		'qpsThreshold': 1000
	}
}

#with open('switch.json', 'w') as f:
with open('threshold.json', 'w') as f:
	json.dump(db_threshold, f, sort_keys=True, indent=4, separators=(',',': '))


#with open('switch.json', 'r') as f:
with open('threshold.json', 'r') as f:
	data = json.load(f)
	print(data)



