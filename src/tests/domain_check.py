import re
from tld import is_tld

def is_domain_tag(t):
	if t == '*': 
		return True 
	elif len(t) > 0: 
		r = re.match(r'[0-9a-zd-]{0,63}',t)
		if r is not None and r.span()[1] == len(t):
			return True 
	return False


def is_domain(domain):
	if len(domain) > 253: 
		return False
	l = domain.split('.')
	if len(l) == 1:
		if l[0] == '*' or is_tld(l[0]):
			return True 
	elif len(l) > 1: 
		if is_tld(l[-1]) is False:
			return False
		for i in l[:-1]:
			if is_domain_tag(i) is False:
				return False
		return True 
	return False




print(is_domain('www.qq.com'))
print(is_domain('*.qq.com'))
print(is_domain('www.qqxx.com'))
print(is_domain('*'))
print(is_domain('*.com'))
print(is_domain('*com'))
print(is_domain('www.qq.comvv'))
print(is_domain('.....'))
print(is_domain('wwaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaawasdddddddddddddddddddddddddddddddddddddddddddddddddddddd.qq.com'))
print(is_domain('www.aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.ccccccccccccccccccccccccccccccccccc.bbbbbbbbbbbbbbbbbbbbbbbbb--123.34444444422222asfasd.cvbsfdfawed2304523452.asjfhgggggggggggggggg.32894593275rasashjfcjkashjfcas.asjdhfgasjgbfhjasghjfghjasguw.ajkfhgajksgfkaghskjhhgfkjahskjfhf.com'))
print(is_domain('www.aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.ccccccccccccccccccccccccccccccccccc.bbbbbbbbbbbbbbbbbbbbbbbbb--123.34444444422222asfasd.cvbsfdfawed2304523452.asjfhgggggggggggggggg.32894593275rasashjfcjkashjfcas.asjdhfgasjgbfhjasghjfghjasguw.ajkfhgfkjahskjfhf.com'))
print(is_domain('www.aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.ccccccccccccccccccccccccccccccccccc.bbbbbbbbbbbbbbbbbbbbbbbbb--123.34444444422222asfasd.cvbsfdfawed2304523452.asjfhgggggggggggggggg.32894593275rasashjfcjkashjfcas.asjdhfgasjgbfhjasghjfghjasguw.ajkfhgajksgfkaghs.ccc'))
