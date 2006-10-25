from conf import conf
from ldaptools import LDAPUtil
import re,os,ldap


class SambaController(LDAPUtil):
	def __init__(self):
		global conf
		LDAPUtil.__init__(self,conf.get('LDAPSERVER','host'))
		
	def add_machine(self,netbiosname,ntdomain):
		hostspath = conf.get('LDAPSERVER','basedn')
		res = self.l.search(hostspath,\
				ldap.SCOPE_ONELEVEL,'(&(objectclass=sambaDomain)(sambaDomainName=%s))'% ntdomain ,['sambaSID'])
		sres = self.l.result(res,0)
		if sres[1]==[]:
			return -1 # Domain does not exist
		machine_info = {
			'sambaSID': '%s-' % sres[1][0][1]['sambaSID'][0],
			'uid': netbiosname,
			'cn': netbiosname,
			'gidNumber': '2005',
			'homeDirectory': '/dev/null',
			'sambaAcctFlags': '[W]',
			'objectClass': ['sambaSamAccount','posixAccount','account','top'],
			'uidNumber':str(self.max(conf.get('LDAPSERVER','basedn'),
				'objectclass=posixaccount','uidNumber',
				int(conf.get('DOMAIN','uid_start')))+1)}
				
		path = "%s,%s,%s,%s" % \
		  ('uid=%s'%netbiosname,\
		   conf.get('LDAPSERVER','smb_machines_ou'),\
		   conf.get('LDAPSERVER','samba_ou'),\
		   conf.get('LDAPSERVER','basedn'))
		
		self.bind(conf.get('LDAPSERVER','admin'),conf.get('LDAPSERVER','passwd'))
		self.touch_by_dict({path:machine_info})


