
import socket
		# 1.创建套接字
tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# 2.绑定端口
addr = ("", 33331)
tcp_server_socket.bind(addr)

		# 3.监听链接
tcp_server_socket.listen(128)

		# 4.接收别人的连接
		# client_socket用来为这个客户端服务
while True:
	client_socket, client_addr = tcp_server_socket.accept() 
	print(client_socket, client_addr)

		# 5.接收对方发送的数据
	recv_data = client_socket.recv(1024)   
	print("接收到的数据：",recv_data)

		# 6.给对方发送数据
	client_socket.send("hahaha".encode("utf-8"))    

		# 7.关闭套接字 
	client_socket.close()
tcp_server_socket.close()

