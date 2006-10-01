	#! /usr/bin/python
from conf import conf
from ldaptools import LDAPUtil
from ldiftools import LDIFImporter
import re,os,ldap

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

#-------------------------------------
#---------- HostManager -------------

class HostManager (LDAPUtil):
	def __init__(self):
		global conf
		LDAPUtil.__init__(self,conf.get('LDAPSERVER','host'))
		
	def fetch_next_ip(self,hosttype_id):
		"""
		Fetch the first available ip address for a hosttype. The ip range
		is defined in skolesys.conf and the ip addresses already assigned
		are read in the ldap database
		"""
	
		hosttype_text = translate_hosttype_id(hosttype_id)
		if not hosttype_text:
			return None
		iprange_str = conf.get('DOMAIN','%s_iprange' % hosttype_text)
		if not iprange_str:
			return None
		
		# Parse the iprange string
		c = re.compile('^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})\s*(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$')
		m = c.match(iprange_str.strip())
		if m:
			ipstart = iptoint('.'.join(m.groups()[:4]))
			ipend = iptoint('.'.join(m.groups()[4:]))
			
			# Get already assigned ip addresses
			hostspath = "%s,%s" % (conf.get('LDAPSERVER','hosts_ou'),conf.get('LDAPSERVER','basedn'))
			res = self.l.search(hostspath,\
				ldap.SCOPE_ONELEVEL,'(objectclass=skoleSysHost)',['ipHostNumber'])
			sres = self.l.result(res)
			
			already_assigned = []
			for hidx in xrange(len(sres[1])):
				ipint = iptoint(sres[1][hidx][1]['ipHostNumber'][0])
				if ipint!=None:
					already_assigned += [ipint]
					
			newip = None
			for tryip in xrange(ipstart,ipend+1):
				if already_assigned.count(tryip):
					continue
				newip = tryip
				break
			if newip:
				return inttoip(newip)
		return None
		
	def fetch_ip_range(self,hosttype_id):
		"""
		Query skolesys.conf and return an ip range as a tuple eg. ("10.1.1.1","10.3.3.254")
		"""
		hosttype_text = translate_hosttype_id(hosttype_id)
		iprange_str = conf.get('DOMAIN','%s_iprange' % hosttype_text)
		if not iprange_str:
			print "XXX make default ip ranges here"
			return None
		# Parse the iprange string
		c = re.compile('^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$')
		m = c.match(iprange_str.strip())
		if m:
			return m.groups()
	
	def host_exists(self,hwaddr=None,hostname=None):
		"""
		check if the host is already registered either by hwaddr or hostname.
		"""
		if not self.host_info(hwaddr=hwaddr,hostname=hostname):
			return False
		return True
		
	def ipaddr_exists(self,ipaddr):
		"""
		check if a ip address is already statically reserved to a certain host
		"""
		hostspath = "%s,%s" % (conf.get('LDAPSERVER','hosts_ou'),conf.get('LDAPSERVER','basedn'))
		res = self.l.search(hostspath,\
				ldap.SCOPE_ONELEVEL,'(& (ipHostNumber=%s)(objectclass=skoleSysHost))'%ipaddr,['cn'])
		sres = self.l.result(res,0)
		if sres[1]==[]:
			return False
		return True	
		
		
	def register_host(self,hwaddr,hostname,hosttype_id,ipaddr=None):
		"""
		Register a new host to the SkoleSYS network. The registrationid is the hwaddr
		but the hostname must be unique aswell. If no ipaddr is given or the given ipaddr 
		is in use the system will pick one for the host.
		"""
		
		# check sanity
		if not check_hwaddr(hwaddr):
			return -1
		if not check_hostname(hostname):
			return -2
		if not translate_hosttype_id(hosttype_id):
			return -3
		hosttype = translate_hosttype_id(hosttype_id)
		
		if ipaddr and not check_ipaddr(ipaddr):
			return -4
				
		# check if the hwaddr is already registered.
		if self.host_exists(hwaddr=hwaddr):
			return -5
		
		# check if the hostname is already registered.
		if self.host_exists(hostname=hostname):
			return -6
		
		if ipaddr and self.ipaddr_exists(ipaddr):
			return -7
		
		if not ipaddr:
			ipaddr = self.fetch_next_ip(hosttype_id)
		
		# If still no ip address, there are no more ip addresses in the
		# ip range of the host type (expand the range in skolesys.conf)
		if not ipaddr:
			return -8
		
		path = "%s,%s,%s" % \
			('cn=%s'%hostname,\
			conf.get('LDAPSERVER','hosts_ou'),\
			conf.get('LDAPSERVER','basedn'))
		host_info = {'cn': hostname,
			'macAddress': hwaddr,
			'hostType': hosttype,
			'hostName': hostname,
			'ipHostNumber': ipaddr,
			'objectclass':('skoleSysHost','top')}
		
		print host_info
		self.bind(conf.get('LDAPSERVER','admin'),conf.get('LDAPSERVER','passwd'))
		self.touch_by_dict({path:host_info})
		
		return 1		

	def host_info(self,hwaddr=None,hostname=None):
		hostspath = "%s,%s" % (conf.get('LDAPSERVER','hosts_ou'),conf.get('LDAPSERVER','basedn'))
		if hwaddr:
			res = self.l.search(hostspath,\
					ldap.SCOPE_ONELEVEL,'(& (macAddress=%s)(objectclass=skoleSysHost))'%hwaddr,['hostType','hostName','ipHostNumber','macAddress'])
			sres = self.l.result(res,0)
			if sres[1]==[]:
				return None
			return sres[1][0][1]
		
		if hostname:
			res = self.l.search(hostspath,\
					ldap.SCOPE_ONELEVEL,'(& (hostName=%s)(objectclass=skoleSysHost))'%hostname,['hostType','hostName','ipHostNumber','macAddress'])
			sres = self.l.result(res,0)
			if sres[1]==[]:
				return None
			return sres[1][0][1]
		
	def list_hosts(self,hosttype_id=None):
			# Get registered hosts
			if hosttype_id==None:
				search_claus = '(objectclass=skoleSysHost)'
			else:
				hosttype = translate_hosttype_id(hosttype_id)
				if hosttype:
					search_claus = '(& (objectclass=skoleSysHost) (hostType=%s) )' % hosttype
				else:
					return -1
					
			hostspath = "%s,%s" % (conf.get('LDAPSERVER','hosts_ou'),conf.get('LDAPSERVER','basedn'))
			res = self.l.search(hostspath,\
				ldap.SCOPE_ONELEVEL,search_claus)
			sres = self.l.result(res)
			
			hostlist = []
			for hidx in xrange(len(sres[1])):
				hostlist += [sres[1][hidx][1]]
			
			return hostlist
			

