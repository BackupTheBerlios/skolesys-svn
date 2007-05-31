'''
This file is part of the SkoleSYS libraries
Copyright (C) 2007 Jakob Simon-Gaarde <info at skolesys.dk>

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Library General Public
License version 2 as published by the Free Software Foundation.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Library General Public License for more details.

You should have received a copy of the GNU Library General Public License
along with this library; see the file COPYING.LIB.  If not, write to
the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
Boston, MA 02110-1301, USA.
'''
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


