#! /usr/bin/python

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

"""
Manage user access rights (Only deployed on the mainserver).
Access is controlled through LDAP therefore most functions
in this file are LDAP related.
"""

from conf import conf
from ldaptools import LDAPUtil
import pwd,os,ldap
from skolesys.tools.mkpasswd import mkpasswd
import skolesys.definitions.userdef as userdef
import skolesys.definitions.ldapdef as ldapdef


#---------------------------------
#--------- UserManager -----------

class AccessManager (LDAPUtil):
	"""
	AccessManager handles all operations related to access rights for users.
	Besides granting and revoking access for users it is also here services
	should ask if users have permission.
	 * Grant access
	 * Revoke access
	 * Query user permissions
	"""
	def __init__(self):
		global conf
		LDAPUtil.__init__(self,conf.get('LDAPSERVER','host'))
	
	def grant_access(self,uid,access_ident):
		"""
		Grant access rights to a service, mode or resource by adding the
		access-string to the users LDAP access attribute.
		1. Fetch userinfo
		2. Check if the user already has the access right in question
		3. Add it to the access attribute (1.3.6.1.4.1.27410.1.1.3)

		Return value: 0 = Success, <0 = Failed
		"""
		if not self.access_identifier_exists(access_ident):
			# The given access identifier is not valid on this domain
			return -13100

		import skolesys.lib.usermanager as userman
		um = userman.UserManager()
		userinfo = um.list_users(None,uid)
		if not userinfo.has_key(uid):
			# user does not exist
			return -13101
		attribs = userinfo[uid]
		path = attribs['dn']
		access = [access_ident]
		if attribs.has_key('accessIdentifier'):
			if type(attribs['accessIdentifier']) == str:
				# Hack to force value into list
				attribs['accessIdentifier'] = [attribs['accessIdentifier']]
			if attribs['accessIdentifier'].count(access_ident):
				# Access already granted
				return -13102
			access += attribs['accessIdentifier']
		try:
			self.bind(conf.get('LDAPSERVER','admin'),conf.get('LDAPSERVER','passwd'))
			self.touch_by_dict({path:{'accessIdentifier':access}})
		except Exception, e:
			print e
			return -13103
		
		return 0


	def revoke_access(self,uid,access_ident):
		"""
		Revoke access rights to a service, mode or resource by removing the
		access-string from the users LDAP access attribute.
		1. Fetch userinfo
		2. Check if the user has the access right in question
		3. Remove it from the access attribute (1.3.6.1.4.1.27410.1.1.3)

		Return value: 0 = Success, <0 = Failed
		"""
		import skolesys.lib.usermanager as userman
		um = userman.UserManager()
		userinfo = um.list_users(None,uid)
		if not userinfo.has_key(uid):
			# user does not exist
			return -13201
		attribs = userinfo[uid]
		path = attribs['dn']
		if not attribs.has_key('accessIdentifier'):
			# User has no access rights to anything
			return -13202

		if type(attribs['accessIdentifier']) == str:
			# Hack to force value into list
			attribs['accessIdentifier'] = [attribs['accessIdentifier']]

		if not attribs['accessIdentifier'].count(access_ident):
			# The user does not have permission to the access right in question 
			return -13203
		access = attribs['accessIdentifier']
		access.remove(access_ident)
		if not len(access):
			access = None
		try:
			self.bind(conf.get('LDAPSERVER','admin'),conf.get('LDAPSERVER','passwd'))
			self.touch_by_dict({path:{'accessIdentifier':access}})
		except Exception, e:
			print e
			return -13204
		
		return 0

	
	def check_permission(self,uid,access_ident):
		"""
		Check if the user uid has permission to access a certain service,
		mode or resource.
		1. Fetch userinfo
		2. Check if the user has the access right in question

		Return value: 0 = Not permitted, 1 = Permitted, <0 failed
		"""
		import skolesys.lib.usermanager as userman
		um = userman.UserManager()
		userinfo = um.list_users(None,uid)
		if not userinfo.has_key(uid):
			# user does not exist
			return -13301

		attribs = userinfo[uid]
		path = attribs['dn']
		if not attribs.has_key('accessIdentifier'):
			# User has no access rights to anything - return "Not permitted"
			return 0

		if type(attribs['accessIdentifier']) == str:
			# Hack to force value into list
			attribs['accessIdentifier'] = [attribs['accessIdentifier']]

		if attribs['accessIdentifier'].count(access_ident):
			# The user does have permission to the access right in question - return "Permitted"
			return 1
		else:
			# The user does not have permission to the access right in question - return "Not permitted"
			return 0


	def list_permissions(self,uid):
		"""
		Query LDAP for a given user and return the permissions as a list
		
		Return value: list, <0 failed
		"""
		import skolesys.lib.usermanager as userman
		um = userman.UserManager()
		userinfo = um.list_users(None,uid)
		if not userinfo.has_key(uid):
			# user does not exist
			return -13401

		attribs = userinfo[uid]
		path = attribs['dn']
		if not attribs.has_key('accessIdentifier'):
			# User has no access rights to anything - return an empty list
			return []

		if type(attribs['accessIdentifier']) == str:
			# Hack to force value into list
			attribs['accessIdentifier'] = [attribs['accessIdentifier']]

		return attribs['accessIdentifier']


	def add_access_identifier(self,access_ident):
		"""
		Add an accessIdentifier to the domain.
		1. Check if it exists already
		2. Add it
		
		Return value: 0 = Succes, <0 = failure
		"""
		res = self.l.search(conf.get('LDAPSERVER','basedn'),\
		                   ldap.SCOPE_BASE,'(objectClass=skoleSysDomain)',['accessIdentifier'])
		sres = self.l.result(res,0)
		if sres[1]==[]:
			# The domain entry does not exist probably missing the skoleSysDomain objectClass
			return -13501

		attribs = sres[1][0][1]
		path = sres[1][0][0]

		access = [access_ident]
		if attribs.has_key('accessIdentifier'):
			if attribs['accessIdentifier'].count(access_ident):
				# Access identifier already exists on this domain
				return -13502
			access += attribs['accessIdentifier']
		# Add it
		try:
			self.bind(conf.get('LDAPSERVER','admin'),conf.get('LDAPSERVER','passwd'))
			self.touch_by_dict({path:{'accessIdentifier':access}})
		except Exception, e:
			print e
			return -13503		
		

	def remove_access_identifier(self,access_ident):
		"""
		Remove an accessIdentifier from the domain. This method will also remove
		the accessIdentifier from any user who has it granted.
		1. Check if it exists
		2. Remove it from domain
		3. Remove it from users
		
		Return value: 0 = Succes, <0 = failure
		"""		
		res = self.l.search(conf.get('LDAPSERVER','basedn'),\
			ldap.SCOPE_SUBTREE,'(accessIdentifier=%s)' % access_ident,['dn','accessIdentifier'])
		
		sres = self.l.result(res,1)
		self.bind(conf.get('LDAPSERVER','admin'),conf.get('LDAPSERVER','passwd'))
		if not len(sres[1]):
			# Access identifer does not exist on the domain
			return -13601

		for entry in sres[1]:
			path = entry[0]
			attribs = entry[1]

			access = attribs['accessIdentifier']
			access.remove(access_ident)
			if not len(access):
				access = None
			try:
				self.touch_by_dict({path:{'accessIdentifier':access}})
			except Exception, e:
				print e
				return -13602
			

	def list_access_identifiers(self):
		"""
		List all access identifiers registered on this domain.
		"""
		res = self.l.search(conf.get('LDAPSERVER','basedn'),\
		                   ldap.SCOPE_BASE,'(objectclass=skoleSysDomain)',['accessIdentifier'])
		
		sres = self.l.result(res,0)
		if sres[1]==[]:
			# The domain entry does not exist probably missing the skoleSysDomain objectClass
			return -13701

		attribs = sres[1][0][1]

		if attribs.has_key('accessIdentifier'):
			return attribs['accessIdentifier']
		return []

	def access_identifier_exists(self,access_ident):
		"""
		Check if a access identifier is present on the domain
		"""
		res = self.l.search(conf.get('LDAPSERVER','basedn'),\
		                   ldap.SCOPE_BASE,'objectClass=skoleSysDomain',['accessIdentifier'])
		sres = self.l.result(res,0)
		if sres[1]==[]:
			# The domain entry does not exist probably missing the skoleSysDomain objectClass
			return -13801
		attribs = sres[1][0][1]
		if not attribs.has_key('accessIdentifier'):
			# The domain does not have any access identifiers registered - Return 0
			return 0
		if attribs['accessIdentifier'].count(access_ident):
			# The access identifier does not exists - return 1
			return 1
		else:
			# The access identifier does not exist on the domain - return 0
			return 0
		
		

