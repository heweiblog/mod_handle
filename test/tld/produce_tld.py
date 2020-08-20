

with open('tld.txt','r') as f:
	l = f.readlines()
	print(l)
	with open('all_tld.py','w') as fp:
		for i in l:
			#if '.' not in i:
				#fp.write('\''+i[:-1]+'\',\n')
			fp.write('\''+i[:-1]+'\',\n')
