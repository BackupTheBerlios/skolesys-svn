#! /usr/bin/python
from conf import conf
from ldaptools import LDAPUtil
from ldiftools import LDIFImporter
import skolesys.definitions.hostdef as hostdef
import re,os,ldap

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
	
		hosttype_text = hostdef.hosttype_as_text(hosttype_id)
		if not hosttype_text:
			return None
		iprange_str = conf.get('DOMAIN','%s_iprange' % hosttype_text)
		if not iprange_str:
			return None
		
		# Parse the iprange string
		c = re.compile('^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})\s*(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$')
		m = c.match(iprange_str.strip())
		if m:
			ipstart = hostdef.iptoint('.'.join(m.groups()[:4]))
			ipend = hostdef.iptoint('.'.join(m.groups()[4:]))
			
			# Get already assigned ip addresses
			hostspath = "%s,%s" % (conf.get('LDAPSERVER','hosts_ou'),conf.get('LDAPSERVER','basedn'))
			res = self.l.search(hostspath,\
				ldap.SCOPE_ONELEVEL,'(objectclass=skoleSysHost)',['ipHostNumber'])
			sres = self.l.result(res)
			
			already_assigned = []
			for hidx in xrange(len(sres[1])):
				ipint = hostdef.iptoint(sres[1][hidx][1]['ipHostNumber'][0])
				if ipint!=None:
					already_assigned += [ipint]
					
			newip = None
			for tryip in range(ipstart,ipend+1):
				if already_assigned.count(tryip):
					continue
				newip = tryip
				break
			if newip:
				return hostdef.inttoip(newip)
		return None
		
	def fetch_ip_range(self,hosttype_id):
		"""
		Query skolesys.conf and return an ip range as a tuple eg. ("10.1.1.1","10.3.3.254")
		"""
		hosttype_text = hostdef.hosttype_as_text(hosttype_id)
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
		hwaddr = hostdef.check_hwaddr(hwaddr)
		if not hwaddr:
			return -1
		hostname = hostdef.check_hostname(hostname)
		if not hostname:
			return -2
		if not hostdef.hosttype_as_text(hosttype_id):
			return -3
		hosttype = hostdef.hosttype_as_text(hosttype_id)
		if ipaddr and not hostdef.check_ipaddr(ipaddr):
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
		
		self.bind(conf.get('LDAPSERVER','admin'),conf.get('LDAPSERVER','passwd'))
		self.touch_by_dict({path:host_info})
		
		return 1		
	
	def host_info(self,hwaddr=None,hostname=None):
		hostspath = "%s,%s" % (conf.get('LDAPSERVER','hosts_ou'),conf.get('LDAPSERVER','basedn'))
		if hwaddr:
			hwaddr = hostdef.check_hwaddr(hwaddr)
			if not hwaddr:
				return None
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
				hosttype = hostdef.hosttype_as_text(hosttype_id)
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
			

