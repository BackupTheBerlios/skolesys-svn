import re
# SkoleSYS host types

MAINSERVER = 1
LTSPSERVER = 2
WORKSTATION = 3
LTSPCLIENT = 4
DYNAMIC = 5 # non-registered hosts

# tools, validation and sanitychecks

def iptoint(ipaddr):
	ipint = 0
	c = re.compile('^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$')
	m = c.match(ipaddr.strip())
	if m:
		for ipnum_idx in xrange(len(m.groups())):
			ipint += int(m.groups()[ipnum_idx])*(256**(3-ipnum_idx))
		return ipint
	return None
	
def inttoip(ipint):
	return '%d.%d.%d.%d' % ((ipint>>24)&255,(ipint>>16)&255,(ipint>>8)&255,ipint&255)




def check_subnet(subnet_str):
	c = re.compile('^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/(\d{1,2})$')
	subnet_str = subnet_str.strip()
	m = c.match(subnet_str)
	if m:
		return m.groups()
	return None


def check_hostname(hostname):
	c = re.compile('^[a-z0-9]+$')
	hostname = hostname.strip().lower()
	m = c.match(hostname)
	if m:
		return hostname
	return None
	
def check_hwaddr(hwaddr):
	if not hwaddr:
		return None
	c1 = re.compile('^[a-f0-9]{2}:[a-f0-9]{2}:[a-f0-9]{2}:[a-f0-9]{2}:[a-f0-9]{2}:[a-f0-9]{2}$')
	c2 = re.compile('^([a-f0-9]{2})([a-f0-9]{2})([a-f0-9]{2})([a-f0-9]{2})([a-f0-9]{2})([a-f0-9]{2})$')
	hwaddr = hwaddr.strip().lower()
	m = c1.match(hwaddr)
	if m:
		return hwaddr
	m = c2.match(hwaddr)
	if m:
		return ':'.join(m.groups())
	return None
	
def check_ipaddr(ipaddr):
	c = re.compile('^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$')
	ipaddr = ipaddr.strip().lower()
	m = c.match(ipaddr)
	if m:
		for num in m.groups():
			if int(num)<0 or int(num)>255:
				return None
		return ipaddr
	
def check_hosttype_text(hosttype_text):
	global MAINSERVER,LTSPSERVER,WORKSTATION,LTSPCLIENT
	hosttype_text = hosttype_text.strip().lower()
	if hosttype_text == 'mainserver':
		return MAINSERVER
	if hosttype_text == 'ltspserver':
		return LTSPSERVER
	if hosttype_text == 'workstation':
		return WORKSTATION
	if hosttype_text == 'ltspclient':
		return LTSPCLIENT
	return None


def translate_hosttype_id(hosttype_id):
	global MAINSERVER,LTSPSERVER,WORKSTATION,LTSPCLIENT
	if hosttype_id == MAINSERVER:
		return 'mainserver'
	if hosttype_id == LTSPSERVER:
		return 'ltspserver'
	if hosttype_id == WORKSTATION:
		return 'workstation'
	if hosttype_id == LTSPCLIENT:
		return 'ltspclient'
	return None
