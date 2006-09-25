#! /usr/bin/python
from conf import conf
from ldaptools import LDAPUtil
from ldiftools import LDIFImporter
import re,os,ldap

# SkoleSYS host types

MAINSERVER = 1
LTSPSERVER = 2
WORKSTATION = 3

# tools, validation and sanitychecks
def check_hostname(hostname):
	c = re.compile('^[a-z0-9]+$')
	hostname = hostname.strip().lower()
	m = c.match(hostname)
	if m:
		return hostname
	return None
	
def check_hwaddr(hwaddr):
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
	
def check_hosttype(hosttype):
	global MAINSERVER,LTSPSERVER,WORKSTATION
	hosttype = hosttype.strip().lower()
	if hosttype == 'ltspserver':
		return LTSPSERVER
	if hosttype == 'workstation':
		return WORKSTATION
	return None


#-------------------------------------
#---------- HostManager -------------

class HostManager (LDAPUtil):
	def __init__(self):
		global conf
		LDAPUtil.__init__(self,conf.get('LDAPSERVER','host'))
		
	def fetch_next_ip(self,hosttype):
		return '10.1.0.56'
	
	def host_exists(self,hwaddr=None,hostname=None):
		"""
		check if the host is already registered either by hwaddr or hostname.
		"""
		hostspath = "%s,%s" % (conf.get('LDAPSERVER','hosts_ou'),conf.get('LDAPSERVER','basedn'))
		if hwaddr:
			res = self.l.search(hostspath,\
					ldap.SCOPE_ONELEVEL,'(& (macAddress=%s)(objectclass=skoleSysHost))'%hwaddr,['cn'])
			sres = self.l.result(res,0)
			if sres[1]==[]:
				return False
			return True	
		
		if hostname:
			res = self.l.search(hostspath,\
					ldap.SCOPE_ONELEVEL,'(& (hostName=%s)(objectclass=skoleSysHost))'%hostname,['cn'])
			sres = self.l.result(res,0)
			if sres[1]==[]:
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
		
		
	def registerHost(self,hwaddr,hostname,hosttype,ipaddr=None):
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
		if not check_hosttype(hosttype):
			return -3
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
			ipaddr = self.fetch_next_ip(hosttype)
		print hosttype
		path = "%s,%s,%s" % \
			('cn=%s'%hostname,\
			conf.get('LDAPSERVER','hosts_ou'),\
			conf.get('LDAPSERVER','basedn'))
		host_info = {'cn': hostname,
			'macAddress': hwaddr,
			'hostRole': hosttype,
			'hostName': hostname,
			'ipHostNumber': ipaddr,
			'objectclass':('skoleSysHost','top')}
		
		self.bind(conf.get('LDAPSERVER','admin'),conf.get('LDAPSERVER','passwd'))
		self.touch_by_dict({path:host_info})
		
		return 1		

