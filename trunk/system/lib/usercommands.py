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

#	# Forced domain version
#	parts = username.split('@')
#	if len(parts)==1 and valid_characters(parts[0]):
#		return "%s@%s" % (parts[0],conf.get('DOMAIN','domain_name').lower())
#
#	if len(parts)==2 and valid_characters(parts[0]) and valid_characters(parts[1]):
#		return username
#	
#	return None


if __name__=='__main__':
	
	commands = {'createuser': 'Create a new system user and home directory',
		'removeuser': 'Remove a user from',
		'groupadd' :'Add a user to a group',
		'groupdel': 'Remove a user from a group',
		'listusers': 'Show a list of system users',
		'listusergroups': 'Show a list of groups a certain user is member of',
		'changeuser': 'Change a users details',
		'authenticate': 'Authenticate a user by username'}

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
		
	from usermanager import UserManager
	from conf import conf
	
	cmd = argv[1]
	
	parser = OptionParser(usage=usage)

	if cmd == "createuser":
		if os.getuid()!=0:
			print "You must be root to add users"
			exit(0)
		parser.set_usage("usage: %s %s [options] username" % (shell_cmd_name,cmd))
		parser.add_option("-g", "--givenName", dest="givenname",default=None,
		                  help="the user's given name/first name", metavar="GIVENNAME")
		parser.add_option("-f", "--familyName", dest="familyname",default=None,
		                  help="the user's family name/last name", metavar="FAMILYNAME")
		parser.add_option("-t", "--userType", dest="usertype",default=None,
		                  help="the user's account type (teacher,student,parent or other)", metavar="USERTYPE")
		parser.add_option("-y", "--firstSchoolYear", dest="firstyear",default=None,
		                  help="The first year this student went to school (students only)", metavar="FIRSTYEAR")
		parser.add_option("-G", "--primaryGroup", dest="primarygroup",default=None,
		                  help="the user's primary group", metavar="PRIMARYGROUP")
		parser.add_option("-p", "--password", dest="password",default=None,
		                  help="users password - avoid using this we dont like passwords in clear text!",
		                  metavar="PASSWORD")
		(options, args) = parser.parse_args()
		
		if len(args)<2:
			print "Missing username for createuser operation"
			exit(0)
		username = check_username(args[1])
		if not username:
			print "The given username is invalid."
			exit(0)
		
		um = UserManager()
		if um.user_exists(username):
			print "The user %s already exists" % username
			exit(0)
		
		if not options.givenname:
			options.givenname = raw_input("Input the user's given name (first name): ")
		if not options.familyname:
			options.familyname = raw_input("Input the user's family name (last name): ")
		if not options.usertype:
			options.usertype = raw_input("Input the user's account type (teacher,student,parent or other): ")
		
		options.usertype = userdef.usertype_as_id(options.usertype)
		if not options.usertype:
			print "Invalid usertype"
			exit(0)
		
		import groupmanager as groupman
		gm = groupman.GroupManager()
		gl = gm.list_groups(None)
		while not options.primarygroup:
			options.primarygroup = raw_input("Input the user's primary group (type \"?\" to view all groups): ")
			if options.primarygroup.strip() == '?':
				gl = gm.list_groups(None)
				for group in gl.keys():
					desc = ''
					if gl[group].has_key('description'):
						desc = gl[group]['description']
					print "%-7s %-24s %-40s" % (gl[group]['gidNumber'],group,desc)
				options.primarygroup = ''
		if gl.has_key(options.primarygroup):
			primarygroupname = options.primarygroup
			options.primarygroup = gl[options.primarygroup]['gidNumber']
		else:
			print "Group does not exist"
			exit(-1)
			
		while not options.password or len(options.password)<5:
			if options.password and len(options.password)<5:
				print "Password is too short - please retype."
				options.password = None
			
			try:
				options.password = getpass("User's password: ")
				again = getpass("Cornfirm password: ")
				print 
			except KeyboardInterrupt:
				exit(-1)
				
			if options.password != again:
				print "Passwords did not match"
				options.password = None
			
		
		try:
			useradd_res = um.createuser(username,options.givenname,options.familyname,options.password,\
				options.usertype,int(options.primarygroup),options.firstyear)
		except Exception, e:
			print e
			print "An error occured while writing to the user LDAP database"
			exit(0)
		
		if useradd_res==-10001:
			print "The user %s already exists" % username
			exit(0)
			
		if useradd_res==-10002:
			print "The system could not map the user to an uid (userid)"
			exit(0)
		
		if useradd_res==-10003:
			print "A problem occured while creating the user's home folder"
			exit(0)
		
		if useradd_res==-10004:
			print "The group \"%s\" does not exist" % primarygroupname
			exit(0)
		
		if useradd_res==-10007:
			print "Failed to pick an uidnumber for the new user"
			exit(0)
			
			
		print "User created..."

	if cmd == "changeuser":
		if os.getuid()!=0:
			print "You must be root to delete users"
			exit(0)
		
		parser.set_usage("usage: %s %s [options] username" % (shell_cmd_name,cmd))
		parser.add_option("-g", "--givenName", dest="givenname",default=None,
			help="the user's given name/first name", metavar="GIVENNAME")
		parser.add_option("-f", "--familyName", dest="familyname",default=None,
			help="the user's family name/last name", metavar="FAMILYNAME")
		parser.add_option("-y", "--firstSchoolYear", dest="firstyear",default=None,
			help="The first year this student went to school (students only)", metavar="FIRSTYEAR")
		parser.add_option("-G", "--primaryGroup", dest="primarygroup",default=None,
			help="the user's primary group", metavar="PRIMARYGROUP")
		parser.add_option("-m", "--mail", dest="mail",default=None,
			help="The mail address of this user", metavar="MAIL")
		parser.add_option("-p", "--password", dest="password",default=None,
			help="users password - avoid using this we dont like passwords in clear text!",
			metavar="PASSWORD")
		parser.add_option("-P", "--prompt-password",
			action="store_true", dest="prompt_password", default=False,
			help="Prompt for password change")
		
		(options, args) = parser.parse_args()

		if len(args)<2:
			print "Missing username for changeuser operation"
			exit(0)
		username = check_username(args[1])
		if not username:
			print "The given username is invalid."
			exit(0)

		if options.password!=None and len(options.password)<5:
			print "Password is too short."
			exit(1)

		while options.prompt_password==True and (not options.password or len(options.password)<5):
			options.password = getpass("New password: ")
			confirm = getpass("Confirm password: ")
			if not options.password==confirm:
				print "Confirmation failed: mismatch"
				options.password = ''
				continue
			if len(options.password)<5:
				print "Password is too short."


		primarygid=None
		if options.primarygroup:
			import groupmanager as groupman
			gm = groupman.GroupManager()
			gl = gm.list_groups('primary')
			if not gl.has_key(options.primarygroup):
				print 'Groupname "%s" is either non-existant or not a primary group type' % options.primarygroup
				exit(-1)
			else:
				primarygid = gl[options.primarygroup]['gidNumber']

		um = UserManager()
		try:
			res = um.changeuser(username,options.givenname,options.familyname,options.password,primarygid,options.firstyear,options.mail)
		except Exception, e:
			print "An error occured while writing to the user LDAP database"
			print e
			exit(0)

		if res == -10101:
			print 'The user "%s" does not exist' % username

		if res == -10104:
			print 'The group "%s" does not exist' % options.primarygroup


	if cmd == "removeuser":
		if os.getuid()!=0:
			print "You must be root to delete users"
			exit(0)
		
		parser.set_usage("usage: %s %s [options] username" % (shell_cmd_name,cmd))
		parser.add_option("-r", "--remove",
		                  action="store_true", dest="remove", default=False,
		                  help="remove the user's homefolder")
		parser.add_option("-b", "--backup",
		                  action="store_true", dest="backup", default=False,
		                  help="backup the user's homefolder")
		
		(options, args) = parser.parse_args()
		if len(args)<2:
			print "Missing username for adduser operation"
			exit(0)
		username = check_username(args[1])
		if not username:
			print "The given username is invalid."
			exit(0)
		
		um = UserManager()
		try:
			delres = um.deluser(username,options.backup,options.remove)
		except Exception, e:
			print "An error occured while writing to the user LDAP database"
			print e
			exit(0)
		
		if delres == -10201:
			print "The user \"%s\" does not exist " % username
			exit(0)
		if delres == -10202:
			print "It was not posible to remove the user \"%s\" from the LDAP service. Probably a permissional error" % username
			exit(0)
		if delres == -10203:
			print "A problem occurred while creating a backup of the user's home directory"
			exit(0)
		if delres == -10204:
			print "A problem occurred while removing the user's home directory"
			exit(0)
		
		print "User deleted..."

	if cmd == "groupadd":
		if os.getuid()!=0:
			print "You must be root to add users to groups"
			exit(0)
		
		parser.set_usage("usage: %s %s username groupname" % (shell_cmd_name,cmd))
		(options, args) = parser.parse_args()
		if len(args)<3:
			print "Missing username or groupname for groupadd operation"
			exit(0)
		username = check_username(args[1])
		groupname = args[2]
		if not username:
			print "The given username is invalid."
			exit(0)
		
		um = UserManager()
		try:
			groupadd_res = um.groupadd(username,groupname)
		except Exception, e:
			print "An error occured while writing to the user LDAP database"
			print e
			exit(0)
		
		if groupadd_res == -10301:
			print "The user \"%s\" does not exist " % username
			exit(0)
		if groupadd_res == -10302:
			print "The group \"%s\" does not exist " % groupname
			exit(0)
		if groupadd_res == -10303:
			print "User \"%s\" is already member of the \"%s\" group" % (username,groupname)
			exit(0)
		if groupadd_res == -10304:
			print "It was not posible to perform the groupadd operation. Probably a permissional error"
			exit(0)
			
		print "User %s added to group %s..." % (username,groupname)

	if cmd == "groupdel":
		if os.getuid()!=0:
			print "You must be root to remove users from groups"
			exit(0)
		
		parser.set_usage("usage: %s %s username groupname" % (shell_cmd_name,cmd))
		(options, args) = parser.parse_args()
		if len(args)<3:
			print "Missing username or groupname for groupadd operation"
			exit(0)
		username = check_username(args[1])
		groupname = args[2]
		if not username:
			print "The given username is invalid."
			exit(0)
		
		um = UserManager()
		try:
			groupdel_res = um.groupdel(username,groupname)
		except Exception, e:
			print "An error occured while writing to the user LDAP database"
			print e
			exit(0)
		
		if groupdel_res == -10401:
			print "The user \"%s\" does not exist " % username
			exit(0)
		if groupdel_res == -10402:
			print "The group \"%s\" does not exist " % groupname
			exit(0)
		if groupdel_res == -10403:
			print "User \"%s\" is not member of the \"%s\" group" % (username,groupname)
			exit(0)
		if groupdel_res == -10404:
			print "It was not posible to perform the groupadd operation. Probably a permissional error"
			exit(0)
		
		print "User %s removed from group %s..." % (username,groupname)
	
	if cmd == "listusers":
		if os.getuid()!=0:
			print "You must be root to add users"
			exit(0)
		
		parser.set_usage("usage: %s %s [options]" % (shell_cmd_name,cmd))
		parser.add_option("-t", "--userType", dest="usertype",default=None,
		                  help="only list users of a certain type (teacher,student,parent or other)", metavar="USERTYPE")
		
		(options, args) = parser.parse_args()
		if options.usertype:
			intxt = options.usertype
			options.usertype = userdef.usertype_as_id(options.usertype)
			if not options.usertype:
				print "User type \"%s\" is not recognized. Following are valid: teacher,student,parent or other" % intxt
				options.usertype = None
		um = UserManager()
		ul = um.list_users(options.usertype)
		for k in ul.keys():
			print k

	if cmd == "listusergroups":
		parser.set_usage("usage: %s %s username" % (shell_cmd_name,cmd))

		(options, args) = parser.parse_args()
		if len(args)<2:
			print "Missing username for %s operation" % cmd
			exit(0)

		username = check_username(args[1])
		if not username:
			print "The given username is invalid."
			exit(0)

		um = UserManager()
		res = um.list_usergroups(username)
		if res==-10501:
			print "User does not exist"
			exit(0)
		for group in res:
			print group

	if cmd == "authenticate":
		if os.getuid()!=0:
			print "You must be root to add users to groups"
			exit(0)
		
		parser.set_usage("usage: %s %s uid" % (shell_cmd_name,cmd))
		parser.add_option("-p", "--password", dest="password",default=None,
		                  help="users password - avoid using this we don't like passwords in clear text!",
		                  metavar="PASSWORD")
		(options, args) = parser.parse_args()
		if len(args)<2:
			print "Missing username for authentication"
			exit(0)
		
		# username (uid)
		username = check_username(args[1])
		if not username:
			print "The given username is invalid."
			exit(0)
		# password
		if not options.password:
			options.password = getpass("User's password: ")
						
		
		um = UserManager()
		try:
			res = um.authenticate(username,options.password)
		except Exception, e:
			print "An error occured while writing to the user LDAP database"
			print e
			exit(1)
		
		if res == -10601:
			print "The user \"%s\" does not exist " % username
			exit(res)
		if res == -10602:
			print "Authentication failed - unknown reason"
			exit(res)
		if res == -10603:
			print "Invalid credentials."
			exit(res)
			
		print 'User "%s" authenticated successfully.' % username
