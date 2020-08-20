#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from ftplib import FTP

host = '192.168.8.253'
port = 21
user = 'anonymous'
passwd = 'anonymous'
path = 'EdnsDial'

def upload(f, remote_path, local_path):
	fp = open(local_path, "rb")
	buf_size = 1024
	f.storbinary("STOR {}".format(remote_path), fp, buf_size)
	fp.close()


def get_rpm():
	l = os.listdir(os.getcwd())
	for i in l:
		if '.rpm' in i:
			return i
	return None

if __name__ == "__main__":
	ftp = FTP()
	ftp.connect(host, port)      # 第一个参数可以是ftp服务器的ip或者域名，第二个参数为ftp服务器的连接端口，默认为21
	ftp.login(user, passwd)     # 匿名登录直接使用ftp.login()
	ftp.cwd(path)                # 切换到tmp目录
	rpm_file = get_rpm()
	if rpm_file is not None:
		upload(ftp, rpm_file, rpm_file)   # 将当前目录下的rpm_file文件上传到ftp服务器path的目录，命名为rpm_file
	ftp.quit()
	print('upload {} success'.format(rpm_file))
	#os.remove(rpm_file)
