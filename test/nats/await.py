

async def test1():
	r = await test2()
	print(r)

async def test2():
	print('test2')
	return 1

test1()
