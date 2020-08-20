
import sys
from gnlpy.netlink import NetlinkSocket
from gnlpy import netlink

def main():
	c = NetlinkSocket()
	print(c.sock)
	print(c.port_id)
	print(c.seq)
	
	ListA = netlink.create_attr_list_type('ListA',('SOME_SHORT', netlink.U16Type),('SOME_STRING', netlink.NulStringType),)
	ListB = netlink.create_attr_list_type('ListB',('ANOTHER_STRING', netlink.NulStringType),('ANOTHER_SHORT', netlink.U16Type),('LIST_A', ListA),)
	msg = netlink.create_genl_message_type('Msg', 'SPECIFIED_KERNEL_NAME',('COMMAND_1', ListA),('COMMAND_2', None),('COMMAND_3', ListB),)
	print(msg)

	c._send(msg)
	recv = c._recv()
	print(recv)


def test():
	ListA = netlink.create_attr_list_type('ListA',('SOME_SHORT', netlink.U16Type),('SOME_STRING', netlink.NulStringType),)
	ListB = netlink.create_attr_list_type('ListB',('ANOTHER_STRING', netlink.NulStringType),('ANOTHER_SHORT', netlink.U16Type),('LIST_A', ListA),)
	Msg = netlink.create_genl_message_type('Msg', 'SPECIFIED_KERNEL_NAME',('COMMAND_1', ListA),('COMMAND_2', None),('COMMAND_3', ListB),)
	print(Msg)	
	sock = netlink.NetlinkSocket()
	#sock = NetlinkSocket()
	print(sock)
	sock.send(Msg('command_1', attr_list=ListA(another_string='foo', another_short=10)))
	reply = sock.recv()[0]
	reply.get_attr_list().get('some_short') 


if __name__ == '__main__':
	#main()
	test()


