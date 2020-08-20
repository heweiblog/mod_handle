from netconf.client import NetconfSSHSession

host = '192.168.5.41'
port = 8300
username = 'heweiwei'
password = '123'

try:
	session = NetconfSSHSession(host, port, username, password)
	#config = session.get_config()
	config = session.edit_config('adf')
	print(config)
except Exception as e:        
	print(e)

