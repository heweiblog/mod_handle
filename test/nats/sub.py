import asyncio,time
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers
import time 

async def run(loop):
    nc = NATS()

    await nc.connect("192.168.66.151:4222", loop=loop,connect_timeout=3)

    async def message_handler(msg):
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()
        print("Received a message on '{subject} {reply}': {data}".format(
            subject=subject, reply=reply, data=data))

    # Simple publisher and async subscriber via coroutine.
    sid1 = await nc.subscribe("foo", cb=message_handler)
    await nc.auto_unsubscribe(sid1, 1)

    async def help_request(msg):
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()
        print("Received a message on '{subject} {reply}': {data}".format(
            subject=subject, reply=reply, data=data))
        await nc.publish(reply, b'I can help')

    # Use queue named 'workers' for distributing requests
    # among subscribers.
    #sid2 = await nc.subscribe("fun", "workers", help_request)
    sid2 = await nc.subscribe("fun", cb=help_request)
    await nc.auto_unsubscribe(sid2, 1)
	
    #await nc.unsubscribe(sid1)
    #await nc.unsubscribe(sid2)
    while True:
        time.sleep(5)		
    loop.close()

    await nc.close()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
