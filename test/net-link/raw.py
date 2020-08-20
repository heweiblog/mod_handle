import os,json
import socket

s = socket.socket(socket.AF_NETLINK, socket.SOCK_RAW, socket.NETLINK_ROUTE)
s.bind((os.getpid(), 0))
s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65536)
s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
#send_data = b'\x14\x00\x00\x00\x12\x00\x01\x03\x00\x00\x00\x00\xd5\x1b\x00\x00\x11\x00\x00\x00'
json_data = {'domain':'www.qq.com','type':'a','answer':'1.1.1.1'}
jb = json.dumps(json_data).encode()
send_data = (len(jb) + 16).to_bytes(4, byteorder='little') + b'\x12\x00\x01\x03\x00\x00\x00\x00\xd5\x1b\x00\x00' + jb
print(jb)
print(send_data)
print(len(send_data))
s.sendto(b'\x14\x00\x00\x00\x12\x00\x01\x03\x00\x00\x00\x00\xd5\x1b\x00\x00\x11\x00\x00\x00', (0, 0))
while True:
	res = s.recvfrom(65536)
	print(res)
	#print(res[0].decode())
	#print(res[1])

