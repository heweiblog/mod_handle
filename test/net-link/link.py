from pyroute2 import IPRoute

with IPRoute() as ipr:
	print([x.get_attr('IFLA_IFNAME') for x in ipr.get_links()])

# create RTNL socket
ipr = IPRoute()

# subscribe to broadcast messages
ipr.bind()

n = ipr.sendto([1,2],{'1':1,'2':2})

print(n)

# wait for data (do not parse it)
data = ipr.recv(65535)

# parse received data
messages = ipr.marshal.parse(data)

# shortcut: recv() + parse()
#
# (under the hood is much more, but for
# simplicity it's enough to say so)
#
messages = ipr.get()
