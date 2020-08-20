import re

def is_domain_tag(t):
	if t == '*':
		return True
	elif len(t) > 0:
		r = re.match(r'[0-9a-zd_d-]{0,63}',t)
		if r is not None and r.span()[1] == len(t):
			return True
	return False


def is_domain(domain):
	if len(domain) > 253:
		return False
	if '--' in domain or '__' in domain:
		return False
	if '-' == domain[:1] or '-' == domain[-1:]:
		return False

	l = domain.split('.')
	if len(l) == 1:
		if '-' in domain or '_' in domain:
			return False
		if is_domain_tag(domain):
			return True
	elif len(l) > 1:
		if '-' in l[-1] or '_' in l[-1]:
			return False
		for i in l:
			if is_domain_tag(i) is False:
				return False
		return True
	return False


print(is_domain('_la.g'))
