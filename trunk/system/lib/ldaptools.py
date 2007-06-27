# This file is part of the SkoleSYS libraries
# Copyright (C) 2007 Jakob Simon-Gaarde <info at skolesys.dk>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License version 2 as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public License
# along with this library; see the file COPYING.LIB.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301, USA.

import ldap
import os.path

def trace_info(str):
	pass
	return
	#print str

class LDAPUtil:
	def __init__(self,host):
		try:
			self.l = ldap.open(host)
		except ldap.LDAPError, e:
			print e
			# handle error however you like
		self.l.protocol_version = ldap.VERSION3
		
	def bind(self,dn,passwd):
		try:
			self.l.simple_bind(dn, passwd)
		except ldap.LDAPError, e:
			print e
			# handle error however you like
		
	def delete(self,dn,allow_recursion=0):
		res = self.l.search(dn, ldap.SCOPE_ONELEVEL , 'objectClass=*' ,['dn'])
		while 1 and allow_recursion:
			sres = self.l.result(res, 0)
			if sres[1]==[]:
				break
			
			self.delete(sres[1][0][0],1)
		trace_info("deleting %s" % dn)
		self.l.delete_s(dn)
		
	def touch_by_dict(self,entry_dict):
		"""
		Touch some ldap entries. Touch meens try to add them if not existing otherwise
		modify entries that already exist.
		entry_dict {dn: attr_dict, dn2: attr2_dict ...}
		"""
		for dn,attr in entry_dict.items():
			try:
				res = self.l.search(dn, ldap.SCOPE_SUBTREE , 'objectClass=*' )
				sres = self.l.result(res,0)
				
			except Exception, e:
				# new entry - try to add
				attributes = [ (k,v) for k,v in attr.items() ]
				self.l.add_s(dn,attributes)
				return
			
			# Existing entry - try to modify
			# Make lowercase attribute dict
			lower_attr = {} 
			for k,v in sres[1][0][1].items():
				lower_attr[k.lower()] = v
			# create modify list
			modlist = []
			for k,v in attr.items():
				if lower_attr.has_key(k.lower()):
					if isinstance(v,list) or \
					   isinstance(v,tuple):
						v = list(v) 
					else:
						v = [v]
					trace_info(str(lower_attr[k.lower()]) + " => " + str(v))
					if v == [None]:
						modlist += [(ldap.MOD_DELETE,k,lower_attr[k.lower()])]
					elif lower_attr[k.lower()] != v:
						modlist += [(ldap.MOD_REPLACE,k,v)]
				else:
					modlist += [(ldap.MOD_ADD,k,v)]
			for mod in modlist:
				trace_info(mod)
			self.l.modify_s(dn,modlist)
			
	def max(self,fromdn,search,attr,start_at=0):
		res= self.l.search(fromdn,ldap.SCOPE_SUBTREE,search,[attr])
		max = start_at
		while 1:
			sres = self.l.result(res, 0)
			if sres[1] == []:
				break
			if int(sres[1][0][1][attr][0])>max:
				max = int(sres[1][0][1][attr][0])
		return max


if __name__=='__main__':
	test = LDAPUtil('ldapserver')
	
