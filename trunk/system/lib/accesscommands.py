#!/usr/bin/python

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

import re,grp,os,ldap
from sys import argv,exit

from getpass import getpass,getuser
from optparse import OptionParser
import skolesys.definitions.userdef as userdef

def check_username(username):
	"Check the user name syntax"
	# lowercase the username nicely
	username = username.lower()
	
	def valid_characters(str):
		c=re.compile('[-_@.0-9a-zA-Z]+')
		m=c.match(str)
		if m and m.group()==str:
			return 1
		return 0
	
	# Free username
	if valid_characters(username):
		return username

if __name__=='__main__':
	
	commands = {'grant_access': 'Grant user access',
		'revoke_access': 'Revoke user access',
		'check_permission' :'Check if a user has permission to access a service or resource',
		'list_permissions': 'List a users permissions',
		'list_access_identifiers': 'List access identifiers available on this domain',
		'add_access_identifier': 'Add an access identifier to the domain',
		'remove_access_identifier': 'Remove an access identifier to the domain'}

	shell_cmd_name = os.path.split(argv[0])[-1:][0]
	
	usage = "usage: %s [command] [options] arg1, arg2" % shell_cmd_name
	if len(argv)<2 or not commands.has_key(argv[1]):
		print usage
		print 
		print "Commands:"
		for cmd,desc in commands.items():
			print '%s - %s' % (cmd,desc)
		exit(0)
		
	# Check root privilegdes
	if not os.getuid()==0:
		print "This command requires root priviledges"
		exit(0)
		
	from accessmanager import AccessManager
	from conf import conf
	
	cmd = argv[1]
	
	parser = OptionParser(usage=usage)

	if cmd == "grant_access":
		if os.getuid()!=0:
			print "You must be root to add users"
			exit(0)
		parser.set_usage("usage: %s %s username accessident" % (shell_cmd_name,cmd))

		(options, args) = parser.parse_args()
		
		if len(args)<3:
			print "Missing username access identifier"
			exit(0)
		username = check_username(args[1])
		if not username:
			print "The given username is invalid."
			exit(0)
		
		access_ident = args[2]

		am = AccessManager()
		try:
			res = am.grant_access(username,access_ident)
		except Exception, e:
			print e
			print "An error occured while writing to the user LDAP database"
			exit(res)
		
		if res==-13100:
			print 'The access identifier "%s" does not exist' % access_ident
			exit(res)
			
		if res==-13101:
			print 'User "%s" does not exist' % username
			exit(res)

		if res==-13102:
			print 'User "%s" already as access to "%s"' % (username,access_ident)
			exit(res)
		
		if res==-13102:
			print 'User already granted this permission'
			exit(res)

		print "Access granted..."
		exit(0)

	if cmd == "revoke_access":
		if os.getuid()!=0:
			print "You must be root to add users"
			exit(0)
		parser.set_usage("usage: %s %s username accessident" % (shell_cmd_name,cmd))

		(options, args) = parser.parse_args()
		
		if len(args)<3:
			print "Missing username access identifier"
			exit(0)
		username = check_username(args[1])
		if not username:
			print "The given username is invalid."
			exit(0)
		
		access_ident = args[2]

		am = AccessManager()
		try:
			res = am.revoke_access(username,access_ident)
		except Exception, e:
			print e
			print "An error occured while writing to the user LDAP database"
			exit(res)
				
		if res==-13201:
			print 'User "%s" does not exist' % username
			exit(res)

		if res==-13202:
			print 'User does not have any permissions'
			exit(res)

		if res==-13203:
			print 'User does not have that permission to be revoked'
			exit(res)
	
		if res==-13204:
			print 'Undefined error communicating with LDAP'
			exit(res)
		
		print "Access revoked..."
		exit(0)

	if cmd == "check_permission":
		if os.getuid()!=0:
			print "You must be root to add users"
			exit(0)
		parser.set_usage("usage: %s %s username accessident" % (shell_cmd_name,cmd))

		(options, args) = parser.parse_args()
		
		if len(args)<3:
			print "Missing username access identifier"
			exit(0)
		username = check_username(args[1])
		if not username:
			print "The given username is invalid."
			exit(0)
		
		access_ident = args[2]

		am = AccessManager()
		try:
			res = am.check_permission(username,access_ident)
		except Exception, e:
			print e
			print "An error occured while writing to the user LDAP database"
			exit(res)
				
		if res==-13301:
			print 'User "%s" does not exist' % username
			exit(res)
		if res==1:
			print "User has permission."
		if res==0:
			print "User does not have permission."
		exit(res)

	if cmd == "list_permissions":
		if os.getuid()!=0:
			print "You must be root to add users"
			exit(0)
		parser.set_usage("usage: %s %s username" % (shell_cmd_name,cmd))

		(options, args) = parser.parse_args()
		
		if len(args)<2:
			print "Missing username argument"
			exit(0)
		username = check_username(args[1])
		if not username:
			print "The given username is invalid."
			exit(0)
		
		am = AccessManager()
		try:
			res = am.list_permissions(username)
		except Exception, e:
			print e
			print "An error occured while writing to the user LDAP database"
			exit(res)
				
		if res==-13401:
			print 'User "%s" does not exist' % username
			exit(res)
		if type(res) == list:
			for perm in res:
				print perm
		exit(0)

	if cmd == "add_access_identifier":
		if os.getuid()!=0:
			print "You must be root to add users"
			exit(0)
		parser.set_usage("usage: %s %s accessident" % (shell_cmd_name,cmd))

		(options, args) = parser.parse_args()
		
		if len(args)<2:
			print "Missing username argument"
			exit(0)
		access_ident = args[1]
		
		am = AccessManager()
		try:
			res = am.add_access_identifier(access_ident)
		except Exception, e:
			print e
			print "An error occured while writing to the user LDAP database"
			exit(res)
				
		if res==-13501:
			print 'Domain does not exist probably missing the skoleSysDomain objectClass'
			exit(res)

		if res==-13502:
			print 'Access identifier "%s" already exists on this domain' % access_ident
			exit(res)

		if res==-13503:
			print 'Undefined error communicating with LDAP'
			exit(res)

		print "Access identifier added."

		exit(0)

	
	if cmd == "remove_access_identifier":
		if os.getuid()!=0:
			print "You must be root to add users"
			exit(0)
		parser.set_usage("usage: %s %s accessident" % (shell_cmd_name,cmd))

		(options, args) = parser.parse_args()
		
		if len(args)<2:
			print "Missing username argument"
			exit(0)

		access_ident = args[1]
		
		am = AccessManager()
		try:
			res = am.remove_access_identifier(access_ident)
		except Exception, e:
			print e
			print "An error occured while writing to the user LDAP database"
			exit(res)

		if res==-13601:
			print 'Access identifier "%s" does not exist on the domain' % access_ident
			exit(res)

		if res==-13602:
			print 'Undefined error communicating with LDAP'
			exit(res)
		print "Access identifier removed."

		exit(0)

	if cmd == "list_access_identifiers":
		parser.set_usage("usage: %s %s" % (shell_cmd_name,cmd))

		(options, args) = parser.parse_args()

		um = AccessManager()
		res = um.list_access_identifiers()
		if res==-13701:
			print "Domain does not exist probably missing the skoleSysDomain objectClass"
			exit(0)

		if type(res) == list:
			for access_ident in res:
				print access_ident
		exit(0)


