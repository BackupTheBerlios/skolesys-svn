# coding=UTF-8

def system_nicefy_string(instr):
	replacemap = {
		'æ':'ae', 'ø': 'oe', 'å': 'aa',
		'Æ':'Ae', 'Ø': 'Oe', 'Å': 'Aa'}
	import re
	c=re.compile('[-\.\w]+')
	nice_chars = c.findall(instr)
	ugly_chars = c.split(instr)
	assemble = ''
	for idx in xrange(len(ugly_chars)):
		nicefied_ugly_chars = ugly_chars[idx]
		
		# nicefy some system viewed ugly characters
		for ugly,nicer in replacemap.items():
			nicefied_ugly_chars = nicefied_ugly_chars.replace(ugly,nicer)
		nice_chars2 = c.findall(nicefied_ugly_chars)
		nicefied_ugly_chars='_'.join(nice_chars2)
		
		# put an underscore if the ugly string was not null but no nicefication was performed
		if nicefied_ugly_chars == '' and len(ugly_chars[idx]) > 0:
			nicefied_ugly_chars = '_'
			
		assemble += nicefied_ugly_chars
		if len(nice_chars) > idx:
			assemble += nice_chars[idx]
			
	return assemble[:16]
