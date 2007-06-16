#!/usr/bin/python
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

import re,grp,os,ldap
from sys import argv,exit

# Check root privilegdes
if not os.getuid()==0:
	print "This command requires root priviledges"
	exit(0)
	
	
from getpass import getpass,getuser
from optparse import OptionParser
from conf import conf
from groupmanager import GroupManager
import skolesys.definitions.groupdef as groupdef


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
	
	commands = {'creategroup': 'Create a new system group and a group directory',
		'changegroup': 'Change the details of a group',
		'removegroup': 'Remove a system group',
		'listgroups': 'Show a list of system groups',
		'listmembers': 'Show members of a certain group',
		'listservices': 'List all available group services or just services of a certain group',
		'listserviceoptions': 'List the options available for a certain service/group combination',
		'setserviceoption': "Set the value of a certain servicegroup's option",
		'attachservice': 'Attach a service to a group',
		'detachservice': 'Detach a service from a group',
		'restartservice': 'Restart a service contained by a certain group'}

	shell_cmd_name = os.path.split(argv[0])[-1:][0]
	
	usage = "usage: %s [command] [options] arg1, arg2" % shell_cmd_name
	if len(argv)<2 or not commands.has_key(argv[1]):
		print usage
		print 
		print "Commands:"
		for cmd,desc in commands.items():
			print '%s - %s' % (cmd,desc)
		exit(0)
		
	cmd = argv[1]
	
	parser = OptionParser(usage=usage)

	if cmd == "creategroup":
		if os.getuid()!=0:
			print "You must be root to add groups"
			exit(0)
			
		parser.set_usage("usage: %s %s [options] groupname" % (shell_cmd_name,cmd))
		parser.add_option("-n", "--diaplayed-name", dest="displayed_name",default=None,
			help="The groups public displayed name. Does not have to match the groupname.", metavar="DISPLAYEDNAME")
		parser.add_option("-t", "--grouptype", dest="grouptype",default=None,
			help="The type og group to be created", metavar="GROUPTYPE")
		parser.add_option("-d", "--description", dest="description",default=None,
			help="the group's description", metavar="DESCRIPTION")
		parser.add_option("-g", "--gid", dest="gid",default=None,
			help="Force the groups id", metavar="GID")
		(options, args) = parser.parse_args()
		
		if len(args)<2:
			print "Missing group name for creategroup operation"
			exit(0)
		
		groupname = args[1]
		print "Group name: %s" % groupname
		
		if not options.displayed_name:
			options.displayed_name = raw_input("Input the group's displayed name [%s]: " % groupname )
		if not options.displayed_name or len(options.displayed_name.strip())==0:
			options.displayed_name = groupname
		print "Displayed name: %s" % options.displayed_name
			
		if not options.grouptype:
			options.grouptype = raw_input("Input the group's type (%s): " % (','.join(groupdef.list_grouptypes_by_text())))
		
		options.grouptype = groupdef.grouptype_as_id(options.grouptype.strip())
		if not options.grouptype:
			print "Invalid grouptype"
			exit(0)

		gm = GroupManager()
		try:
			groupadd_res = gm.creategroup(groupname,options.displayed_name,options.grouptype,options.description,options.gid)
		except Exception, e:
			print "An error occured while writing to the user LDAP database"
			print e
			exit(0)
		if groupadd_res==-1:
			print "The group %s already exists" % groupname
			exit(0)
		if groupadd_res==-2:
			print "The system could not map the group to an gid (groupid)"
			exit(0)
		if groupadd_res==-3:
			print "A problem occured while creating the groups's home directory"
			exit(0)
		if groupadd_res==-5:
			print "Displayed name is not set, though it is mandetory"
			exit(0)

		print "Group created..."

	if cmd == "changegroup":
		if os.getuid()!=0:
			print "You must be root to remove groups"
			exit(0)
		parser.set_usage("usage: %s %s [options] groupname" % (shell_cmd_name,cmd))
		parser.add_option("-d", "--description", dest="description",default=None,
			help="Change the groups description", metavar="DESCRIPTION")
		(options, args) = parser.parse_args()
		
		if len(args)<2:
			print "Missing group name for changegroup operation"
			exit(0)
		
		groupname = args[1]
		print "Group name: %s" % groupname
		
		gm = GroupManager()
		try:
			changegrp_res = gm.changegroup(groupname,options.description)
		except Exception, e:
			print "An error occured while writing to the user LDAP database"
			print e
			exit(0)
		if changegrp_res==-1:
			print 'The group "%s" does not exist' % groupname

			

	if cmd == "removegroup":
		if os.getuid()!=0:
			print "You must be root to remove groups"
			exit(0)
			
		parser.set_usage("usage: %s %s [options] groupname" % (shell_cmd_name,cmd))
		parser.add_option("-r", "--remove",
		                  action="store_true", dest="remove", default=False,
		                  help="remove the group home folder")
		parser.add_option("-b", "--backup",
		                  action="store_true", dest="backup", default=False,
		                  help="backup the group home folder")
		(options, args) = parser.parse_args()
		
		if len(args)<2:
			print "Missing group name for creategroup operation"
			exit(0)
		
		groupname = args[1]
		print "Group name: %s" % groupname
		
		gm = GroupManager()
		try:
			groupdel_res = gm.removegroup(groupname,options.backup,options.remove)
		except Exception, e:
			print "An error occured while writing to the user LDAP database"
			print e
			exit(0)
		if groupdel_res==-1:
			print "The group %s does not exist" % groupname
			exit(0)
		if groupdel_res==-2:
			print "A problem occurred while creating a backup of the group's home folder."
			exit(0)
		if groupdel_res==-3:
			print "A problem occurred while removing the group's home folder."
			exit(0)
		
		print "Group removed..."

	if cmd == "listgroups":
		if os.getuid()!=0:
			print "You must be root list groups"
			exit(0)
		
		parser.set_usage("usage: %s %s [options]" % (shell_cmd_name,cmd))
		parser.add_option("-t", "--groupType", dest="grouptype",default=None,
		                  help="only list groups of a certain type (teacher,student,parent or other)", metavar="GROUPTYPE")
		parser.add_option("-n", "--groupname", dest="groupname",default=None,
				  help="Limit the result to a certain group",metavar="GROUPNAME")
		
		(options, args) = parser.parse_args()
		if options.grouptype:
			intxt = options.grouptype
			options.grouptype = groupdef.grouptype_as_id(options.grouptype)
			if not options.grouptype:
				print "User type \"%s\" is not recognized. Following are valid: teacher,student,parent or other" % intxt
				options.grouptype = None
		
		gm = GroupManager()
		gl = gm.list_groups(options.grouptype,options.groupname)
		for k in gl.keys():
			print k

	if cmd == "listmembers":
		parser.set_usage("usage: %s %s groupname" % (shell_cmd_name,cmd))

		(options, args) = parser.parse_args()
		if len(args)<2:
			print "Missing group name for listmembers operation"
			exit(0)

		gm = GroupManager()
		res = gm.list_members(args[1])
		if res==-1:
			print "Group does not exist"
			exit(0)
		for member in res:
			print member

	
	if cmd == "attachservice":
		parser.set_usage("usage: %s %s groupname servicename" % (shell_cmd_name,cmd))

		(options, args) = parser.parse_args()
		if len(args)<2:
			print "Missing group and service name for attachservice operation"
			exit(0)

		if len(args)<3:
			print "Missing service name for attachservice operation"
			exit(0)
		
		gm = GroupManager()
		res = gm.attach_service(args[1],args[2])
		if res==-1:
			print 'There is no service group by that name. NOTE! the group must be a service group.'
			exit(0)
		if res==-2:
			print 'The service "%s" does not exist' % args[2]
			exit(0)

		if res==-3:
			print 'The service "%s" failed to load' % args[2]
			exit(0)
		
		if res==-4:
			print 'The service "%s" is already attached to "%s"' % (args[2],args[1])
			exit(0)

	if cmd == "detachservice":
		parser.set_usage("usage: %s %s groupname servicename" % (shell_cmd_name,cmd))

		(options, args) = parser.parse_args()
		if len(args)<2:
			print "Missing group and service name for detachservice operation"
			exit(0)

		if len(args)<3:
			print "Missing service name for detachservice operation"
			exit(0)
		
		gm = GroupManager()
		res = gm.detach_service(args[1],args[2])
		if res==-1:
			print 'There is no service group by that name. NOTE! the group must be a service group.'
			exit(0)
		if res==-2:
			print 'The service "%s" does not exist' % args[2]
			exit(0)

		if res==-3:
			print 'The service "%s" failed to load' % args[2]
			exit(0)
		
		if res==-4:
			print 'The service "%s" is not attached to "%s"' % (args[2],args[1])
			exit(0)

	if cmd == "listservices":
		parser.set_usage("usage: %s %s groupname" % (shell_cmd_name,cmd))

		groupname = None
		(options, args) = parser.parse_args()
		if len(args)>=2:
			groupname = args[1]

		gm = GroupManager()
		res = gm.list_services(groupname)
		if type(res) == list:
			for s in res:
				print s
				
		if res==-1:
			print 'There is no service group by that name. NOTE! the group must be a service group.'
			exit(-1)
		
	if cmd == "listserviceoptions":
		def fish_dict_value(d,key,defval=""):
			# Safely fish out values from a dictionary
			if d.has_key(key):
				return d[key]
			return defval
		
		parser.set_usage("usage: %s %s servicename [groupname]" % (shell_cmd_name,cmd))

		groupname = None
		(options, args) = parser.parse_args()
		if len(args)>=3:
			groupname = args[2]
		if len(args)<2:
			print "Missing service name for listserviceoptions operation"
			exit(0)
		
		servicename = args[1]

		gm = GroupManager()
		res = gm.list_service_options_available(servicename,groupname)
		res = gm.list_service_options_available(servicename,groupname)
		if type(res) == dict:
			print "%-20.20s %-20.20s %-20.20s %-20.20s %-.50s" % \
				('VARIABLE','TYPE','SECTION','DEFAULT','CURRENT_VALUE')
			for var,details in res.items():
				typ = str(fish_dict_value(details,'type'))
				section = str(fish_dict_value(details,'section'))
				defval = str(fish_dict_value(details,'default'))
				curval = str(fish_dict_value(details,'value'))
				print "%-20.20s %-20.20s %-20.20s %-20.20s %-.50s" % (var,typ,section,defval,curval)
				
		if res==-1:
			print 'There is no service group by that name. NOTE! the group must be a service group.'
			exit(-1)
	
	if cmd == "setserviceoption":
		parser.set_usage("usage: %s %s groupname servicename option value" % (shell_cmd_name,cmd))

		(options, args) = parser.parse_args()
		if len(args)<5:
			print parser.usage
			exit(0)
		
		groupname,servicename,option,value = (args[1],args[2],args[3],args[4])

		gm = GroupManager()
		res = gm.set_service_option_value(groupname,servicename,option,value)
		
		if res==-1:
			print 'Group "%s" does not exist' % groupname
		if res==-2:
			print 'The service "%s" does not exist' % servicename
		if res==-3:
			print 'The service "%s" failed to load' % groupname
		if res==-4:
			print 'Group "%s" is not attached to the service "%s"' % (groupname,servicename)
			
		exit(res)

	if cmd == "restartservice":
		parser.set_usage("usage: %s %s groupname servicename" % (shell_cmd_name,cmd))

		(options, args) = parser.parse_args()
		if len(args)<3:
			print parser.usage
			exit(0)
		
		groupname,servicename = (args[1],args[2])

		gm = GroupManager()
		res = gm.restart_service(groupname,servicename)
		
		if res==-1:
			print 'Group "%s" does not exist' % groupname
		if res==-2:
			print 'The service "%s" does not exist' % servicename
		if res==-3:
			print 'The service "%s" failed to load' % groupname
		if res==-4:
			print 'Group "%s" is not attached to the service "%s"' % (groupname,servicename)
			
		exit(res)

