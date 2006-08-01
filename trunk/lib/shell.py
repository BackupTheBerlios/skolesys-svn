#!/usr/bin/python
from sys import argv,exit
import re,grp,os,ldap
from getpass import getpass,getuser
from optparse import OptionParser

from usermanager import UserManager
from groupmanager import GroupManager

# User types
TEACHER = 1
STUDENT = 2
PARENT = 3
OTHER = 4

def check_username(username):
	"Check the user name syntax"
	# lowercase the username nicely
	username = username.lower()
	def valid_characters(str):
		c=re.compile('[-_.0-9a-zA-Z]+')
		m=c.match(str)
		if m and m.group()==str:
			return 1
		return 0

	parts = username.split('@')
	if len(parts)==1 and valid_characters(parts[0]):
		return "%s@%s" % (parts[0],conf.get('DOMAIN','domain_name').lower())

	if len(parts)==2 and valid_characters(parts[0]) and valid_characters(parts[1]):
		return username
	
	return None


if __name__=='__main__':
	
	commands = {'createuser': 'Create a new system user and home directory',
		'removeuser': 'Remove a user from',
		'groupadd' :'Add a user to a group',
		'groupdel': 'Remove a user to a group',
		'listusers': 'Show a list of system users',
		'listusergroups': 'Show a list of groups a certain user is member of',
		'creategroup': 'Create a new system group and a group directory',
		'removegroup': 'Remove a system group',
		'listgroups': 'Show a list of system groups',
		'listmembers': 'Show members of a certain group'}

	
	usage = "usage: l4sadmin [command] [options] arg1, arg2"
	if len(argv)<2 or not commands.has_key(argv[1]):
		print usage
		print 
		print "Commands:"
		for cmd,desc in commands.items():
			print '%s - %s' % (cmd,desc)
		exit(0)
		
	cmd = argv[1]
	
	parser = OptionParser(usage=usage)

	if cmd == "createuser":
		if os.getuid()!=0:
			print "You must be root to add users"
			exit(0)
		parser.set_usage("usage: l4sadmin %s [options] username" % cmd)
		parser.add_option("-g", "--givenName", dest="givenname",default=None,
		                  help="the user's given name/first name", metavar="GIVENNAME")
		parser.add_option("-f", "--familyName", dest="familyname",default=None,
		                  help="the user's family name/last name", metavar="FAMILYNAME")
		parser.add_option("-t", "--userType", dest="usertype",default=None,
		                  help="the user's account type (teacher,student,parent or other)", metavar="USERTYPE")
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
		
		print "Username: %s" % username
		
		if not options.givenname:
			options.givenname = raw_input("Input the user's given name (first name): ")
		if not options.familyname:
			options.familyname = raw_input("Input the user's family name (last name): ")
		if not options.usertype:
			options.usertype = raw_input("Input the user's account type (teacher,student,parent or other): ")
		if options.usertype.strip().lower() == 'teacher':
			options.usertype = TEACHER
		elif options.usertype.strip().lower() == 'student':
			options.usertype = STUDENT
		elif options.usertype.strip().lower() == 'parent':
			options.usertype = PARENT
		elif options.usertype.strip().lower() == 'other':
			options.usertype = OTHER
		else:
			print "Invalid usertype"
			exit(0)
		
		gl = gm.list_groups(None)
		while not options.primarygroup:
			options.primarygroup = raw_input("Input the user's primary group (type \"?\" to view all groups): ")
			if options.primarygroup.strip() == '?':
				gm = GroupManager()
				gl = gm.list_groups(None)
				for group in gl.keys():
					desc = ''
					if gl[group].has_key('description'):
						desc = gl[group]['description']
					print "%-7s %-24s %-40s" % (gl[group]['gidNumber'],group,desc)
				options.primarygroup = ''
		if gl.has_key(options.primarygroup):
			options.primarygroup = gl[options.primarygroup]['gidNumber']
		else:
			print "Group does not exist"
			exit(0)
			
		if not options.password:
			options.password = getpass("User's password: ")
			again = getpass("Cornfirm password: ")
			if options.password != again:
				print "Passwords did not match"
				exit(0)
		
		try:
			useradd_res = um.createuser(username,options.givenname,options.familyname,options.password,options.usertype)
		except Exception, e:
			print "An error occured while writing to the user LDAP database"
			print e
			exit(0)
		
		if useradd_res==-1:
			print "The user %s already exists" % username
			exit(0)
			
		if useradd_res==-2:
			print "The system could not map the user to an uid (userid)"
			exit(0)
		
		if useradd_res==-3:
			print "A problem occured while creating the user's home folder"
			exit(0)
		
		print "User created..."

	if cmd == "removeuser":
		if os.getuid()!=0:
			print "You must be root to delete users"
			exit(0)
		
		parser.set_usage("usage: l4sadmin %s [options] username" % cmd)
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
		print "Username: %s" % username
		
		um = UserManager()
		try:
			delres = um.deluser(username,options.backup,options.remove)
		except Exception, e:
			print "An error occured while writing to the user LDAP database"
			print e
			exit(0)
		
		if delres == -1:
			print "The user \"%s\" does not exist " % username
			exit(0)
		if delres == -2:
			print "It was not posible to remove the user \"%s\" from the LDAP service. Probably a permissional error" % username
			exit(0)
		if delres == -3:
			print "A problem occurred while creating a backup of the user's home directory"
			exit(0)
		if delres == -4:
			print "A problem occurred while removing the user's home directory"
			exit(0)
		
		print "User deleted..."

	if cmd == "groupadd":
		if os.getuid()!=0:
			print "You must be root to add users to groups"
			exit(0)
		
		parser.set_usage("usage: l4sadmin %s username groupname" % cmd)
		(options, args) = parser.parse_args()
		if len(args)<3:
			print "Missing username or groupname for groupadd operation"
			exit(0)
		username = check_username(args[1])
		groupname = args[2]
		if not username:
			print "The given username is invalid."
			exit(0)
		print "Username: %s" % username
		print "Groupname: %s" % groupname
		
		um = UserManager()
		try:
			groupadd_res = um.groupadd(username,groupname)
		except Exception, e:
			print "An error occured while writing to the user LDAP database"
			print e
			exit(0)
		
		if groupadd_res == -1:
			print "The user \"%s\" does not exist " % username
			exit(0)
		if groupadd_res == -2:
			print "The group \"%s\" does not exist " % groupname
			exit(0)
		if groupadd_res == -3:
			print "User \"%s\" is already member of the \"%s\" group" % (username,groupname)
			exit(0)
		if groupadd_res == -4:
			print "It was not posible to perform the groupadd operation. Probably a permissional error"
			exit(0)
			
		print "User %s added to group %s..." % (username,groupname)

	if cmd == "groupdel":
		if os.getuid()!=0:
			print "You must be root to remove users from groups"
			exit(0)
		
		parser.set_usage("usage: l4sadmin %s username groupname" % cmd)
		(options, args) = parser.parse_args()
		if len(args)<3:
			print "Missing username or groupname for groupadd operation"
			exit(0)
		username = check_username(args[1])
		groupname = args[2]
		if not username:
			print "The given username is invalid."
			exit(0)
		print "Username: %s" % username
		print "Groupname: %s" % groupname
		
		um = UserManager()
		try:
			groupdel_res = um.groupdel(username,groupname)
		except Exception, e:
			print "An error occured while writing to the user LDAP database"
			print e
			exit(0)
		
		if groupdel_res == -1:
			print "The user \"%s\" does not exist " % username
			exit(0)
		if groupdel_res == -2:
			print "The group \"%s\" does not exist " % groupname
			exit(0)
		if groupdel_res == -3:
			print "User \"%s\" is not member of the \"%s\" group" % (username,groupname)
			exit(0)
		if groupdel_res == -4:
			print "It was not posible to perform the groupadd operation. Probably a permissional error"
			exit(0)
		
		print "User %s removed from group %s..." % (username,groupname)
	
	if cmd == "listusers":
		if os.getuid()!=0:
			print "You must be root to add users"
			exit(0)
		
		parser.set_usage("usage: l4sadmin %s [options]" % cmd)
		parser.add_option("-t", "--userType", dest="usertype",default=None,
		                  help="only list users of a certain type (teacher,student,parent or other)", metavar="USERTYPE")
		
		(options, args) = parser.parse_args()
		if options.usertype:
			if options.usertype.strip().lower() == 'teacher':
				options.usertype = TEACHER
			elif options.usertype.strip().lower() == 'student':
				options.usertype = STUDENT
			elif options.usertype.strip().lower() == 'parent':
				options.usertype = PARENT
			elif options.usertype.strip().lower() == 'other':
				options.usertype = OTHER
			else:
				print "User type \"%s\" is not recognized. Following are valid: teacher,student,parent or other" % options.usertype
				options.usertype = None
		um = UserManager()
		ul = um.list_users(options.usertype)
		for k in ul.keys():
			print k

	if cmd == "listusergroups":
		parser.set_usage("usage: l4sadmin %s username" % cmd)

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
		if res==-1:
			print "User does not exist"
			exit(0)
		for group in res:
			print group

	if cmd == "creategroup":
		if os.getuid()!=0:
			print "You must be root to add groups"
			exit(0)
			
		parser.set_usage("usage: l4sadmin %s [options] groupname" % cmd)
		parser.add_option("-r", "--groupRelation", dest="grouprelation",default=None,
			help="the group's relationship (teacher,student,parent or other)", metavar="GROUPRELATION")
		parser.add_option("-d", "--description", dest="description",default=None,
			help="the group's description", metavar="DESCRIPTION")
		(options, args) = parser.parse_args()
		
		if len(args)<2:
			print "Missing group name for creategroup operation"
			exit(0)
		
		groupname = args[1]
		print "Group name: %s" % groupname
		
		if not options.grouprelation:
			options.grouprelation = raw_input("Input the user's account type (teacher,student,parent or other): ")
		if options.grouprelation.strip().lower() == 'teacher':
			options.grouprelation = TEACHER
		elif options.grouprelation.strip().lower() == 'student':
			options.grouprelation = STUDENT
		elif options.grouprelation.strip().lower() == 'parent':
			options.grouprelation = PARENT
		elif options.grouprelation.strip().lower() == 'other':
			options.grouprelation = OTHER
		else:
			print "Invalid relationship"
			exit(0)

		gm = GroupManager()
		try:
			groupadd_res = gm.creategroup(groupname,options.grouprelation,options.description)
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
			
		print "Group created..."
			

	if cmd == "removegroup":
		if os.getuid()!=0:
			print "You must be root to remove groups"
			exit(0)
			
		parser.set_usage("usage: l4sadmin %s [options] groupname" % cmd)
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
			print "You must be root to add users"
			exit(0)
		
		parser.set_usage("usage: l4sadmin %s [options]" % cmd)
		parser.add_option("-t", "--userType", dest="usertype",default=None,
		                  help="only list groups of a certain type (teacher,student,parent or other)", metavar="GROUPTYPE")
		
		(options, args) = parser.parse_args()
		if options.usertype:
			if options.usertype.strip().lower() == 'teacher':
				options.usertype = TEACHER
			elif options.usertype.strip().lower() == 'student':
				options.usertype = STUDENT
			elif options.usertype.strip().lower() == 'parent':
				options.usertype = PARENT
			elif options.usertype.strip().lower() == 'other':
				options.usertype = OTHER
			else:
				print "User type \"%s\" is not recognized. Following are valid: teacher,student,parent or other" % options.usertype
				options.usertype = None
		
		gm = GroupManager()
		gl = gm.list_groups(options.usertype)
		for k in gl.keys():
			print k

	if cmd == "listmembers":
		parser.set_usage("usage: l4sadmin %s groupname" % cmd)

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
