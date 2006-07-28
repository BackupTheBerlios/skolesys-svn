#! /usr/bin/python

from sys import argv,exit
import re,pwd,os
from getpass import getpass,getuser
import ldap

from conf import conf
from ldaptools import LDAPUtil
from ldiftools import LDIFImporter
from optparse import OptionParser
from mkpasswd import mkpasswd

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
	

class UserManager (LDAPUtil):
	def __init__(self):
		global conf
		LDAPUtil.__init__(self,conf.get('LDAPSERVER','host'))
	
	def list_users(self,usertype):
		if not usertype:
			path = conf.get('LDAPSERVER','basedn')
		else:
			if (usertype==TEACHER):
				usertype_ou = "teachers_ou"
			if (usertype==STUDENT):
				usertype_ou = "students_ou"
			if (usertype==PARENT):
				usertype_ou = "parents_ou"
			if (usertype==OTHER):
				usertype_ou = "others_ou"
			path = "%s,%s,%s" % \
				(conf.get('LDAPSERVER','logins_ou'),\
				conf.get('LDAPSERVER',usertype_ou),\
				conf.get('LDAPSERVER','basedn'))
				
		res = self.l.search(path,ldap.SCOPE_SUBTREE,'(& (uid=*)(objectclass=posixaccount))',\
			['dn','cn','mail','uid','title'])
			
		user_dict = {}
		while 1:
			sres = self.l.result(res,0)
			if sres[1]==[]:
				break
			if not sres[1][0][1].has_key('uid'):
				continue
			
			uid = sres[1][0][1]['uid'][0]
			user_dict[uid] = {}
			for (k,v) in sres[1][0][1].items():
				if len(v)==1:
					user_dict[uid][k] = v[0]
				else:
					user_dict[uid][k] = v
		return user_dict
	
	def user_exists(self,uid):
		res = self.l.search(conf.get('LDAPSERVER','basedn'),\
		                   ldap.SCOPE_SUBTREE,'(& (uid=%s)(objectclass=posixaccount))'%uid,['dn'])
		
		sres = self.l.result(res,0)
		
		if sres[1]==[]:
			return False
		return True

	
	def createuser(self,uid,givenname,familyname,passwd,usertype):
		"""
		Add a user to the schools authentication directory service.
		The usertype must be one of the constants TEACHER,STUDENT,PARENT or OTHER
		"""
		# check if the group exists already
		if self.user_exists(uid):
			return -1
		
		if (usertype==TEACHER):
			usertype_ou = "teachers_ou"
			title = "Teacher"
		if (usertype==STUDENT):
			usertype_ou = "students_ou"
			title = "Student"
		if (usertype==PARENT):
			usertype_ou = "parents_ou"
			title = "Parent"
		if (usertype==OTHER):
			usertype_ou = "others_ou"
			title = "Other"
			
		path = "%s,%s,%s,%s" % \
		  ('uid=%s'%uid,\
		   conf.get('LDAPSERVER','logins_ou'),\
		   conf.get('LDAPSERVER',usertype_ou),\
		   conf.get('LDAPSERVER','basedn'))
		user_info = {'uid':uid,
			'givenname':'%s' % givenname,
			'cn':'%s %s' % (givenname,familyname),
			'gidNumber':'1000',
			'uidnumber': str(self.max(conf.get('LDAPSERVER','basedn'),
				'objectclass=posixaccount','uidNumber',
				int(conf.get('DOMAIN','uid_start')))+1),
			'homeDirectory':'/home/%s/%s' % (conf.get('DOMAIN','domain_name'),uid),
			'sn':'%s' % givenname,
			'objectclass':('inetOrgPerson','organizationalPerson','posixAccount','shadowAccount','person', 'top'),
			'mail': uid,
			'title':title,
			'userPassword':mkpasswd(passwd,3,'crypt')}
		
		self.bind(conf.get('LDAPSERVER','admin'),conf.get('LDAPSERVER','passwd'))
		self.touch_by_dict({path:user_info})
		
		try:
			posix_uid = pwd.getpwnam(uid)[2]
		except Exception, e:
			print e
			return -2
		
		try:
			home_path = "%s/%s/%s" % (conf.get('DOMAIN','homes_root'),conf.get('DOMAIN','domain_name'),uid)
			if not os.path.exists(os.path.normpath(home_path)):
				os.mkdir(os.path.normpath(home_path))
		
			os.system('chown %d %s -R -f' % (posix_uid,os.path.normpath(home_path)))
		except Exception,e:
			print e
			return -3
		return 1	
		
	def deluser(self,uid,backup_home,remove_home):
		res = self.l.search(conf.get('LDAPSERVER','basedn'),ldap.SCOPE_SUBTREE,'uid=%s'%uid,['dn'])
		sres = self.l.result(res,0)
		if sres[1]==[]:
			return -1
		try:
			self.bind(conf.get('LDAPSERVER','admin'),conf.get('LDAPSERVER','passwd'))
			self.delete(sres[1][0][0])
		except Exception, e:
			print e
			return -2
		
		res = self.l.search(conf.get('LDAPSERVER','basedn'),ldap.SCOPE_SUBTREE,
			'(& (objectclass=posixgroup) (memberuid=%s))'%uid,['cn'])
		
		rm_groups = []
		while 1:
			sres = self.l.result(res,0)
			if sres[1] == []:
				break
			rm_groups += [sres[1][0][1]['cn'][0]]
			
		for group in rm_groups:
			self.groupdel(uid,group)
		
		# backup and remove home directory
		home_path = "%s/%s/%s" % (conf.get('DOMAIN','homes_root'),conf.get('DOMAIN','domain_name'),uid)
		if os.path.exists(os.path.normpath(home_path)):
			if backup_home:
				try:
					print "Backing up the homefolder of \"%s\"..." % uid
					cnt = 0
					cnt_str = ''
					backup_path = "%s%s.bz2" % (os.path.normpath(home_path),cnt_str)
					while os.path.exists(backup_path):
						cnt+=1
						cnt_str = str(cnt)
						backup_path = "%s_%s.bz2" % (os.path.normpath(home_path),cnt_str)
						
					os.system('tar cjpf %s %s' % (backup_path,os.path.normpath(home_path)))
				except Exception,e:
					print e
					return -3
			if remove_home:
				try:
					print "Deleting the homefolder of \"%s\"..." % uid
					os.system('rm %s -R -f' % (os.path.normpath(home_path)))
				except Exception, e:
					print e
					return -4
		
		return 1

	def groupadd(self,uid,groupname):
		res = self.l.search(conf.get('LDAPSERVER','basedn'),ldap.SCOPE_SUBTREE,'(& (uid=%s) (objectclass=posixaccount))'%uid,['dn'])
		sres = self.l.result(res,0)
		if sres[1]==[]:
			return -1
		res = self.l.search(conf.get('LDAPSERVER','basedn'),ldap.SCOPE_SUBTREE,'(& (cn=%s) (objectclass=posixgroup))'%groupname,['memberuid'])
		sres = self.l.result(res,0)
		if sres[1]==[]:
			return -2
		attribs = sres[1][0][1]
		path = sres[1][0][0]
		memberuid = [uid]
		if attribs.has_key('memberUid'):
			if attribs['memberUid'].count(uid):
				return -3
			memberuid += attribs['memberUid']
			
		try:
			self.bind(conf.get('LDAPSERVER','admin'),conf.get('LDAPSERVER','passwd'))
			self.touch_by_dict({path:{'memberuid':memberuid}})
		except Exception, e:
			print e
			return -4
		
		# Create user symlink to the group
		user_group_dir = '%s/%s/%s/groups' % (conf.get('DOMAIN','homes_root'),conf.get('DOMAIN','domain_name'),uid)
		if not os.path.exists(user_group_dir):
			os.makedirs(user_group_dir)
		if not os.path.exists('%s/%s' % (user_group_dir,groupname)):
			os.symlink('%s/%s/%s' % (conf.get('DOMAIN','homes_root'),conf.get('DOMAIN','domain_name'),groupname),
				'%s/%s' % (user_group_dir,groupname))
		
		return 1

	def groupdel(self,uid,groupname):
		# Do not check if the user exists, just remove the uid
		#res = self.l.search(conf.get('LDAPSERVER','basedn'),ldap.SCOPE_SUBTREE,'(& (uid=%s) (objectclass=posixaccount))'%uid,['dn'])
		#sres = self.l.result(res,0)
		#if sres[1]==[]:
		#	return -1
		res = self.l.search(conf.get('LDAPSERVER','basedn'),ldap.SCOPE_SUBTREE,'(& (cn=%s) (objectclass=posixgroup))'%groupname,['memberuid'])
		sres = self.l.result(res,0)
		if sres[1]==[]:
			return -2
		attribs = sres[1][0][1]
		path = sres[1][0][0]
		if attribs.has_key('memberUid'):
			if attribs['memberUid'].count(uid):
				memberuid = attribs['memberUid']
				memberuid.remove(uid)
			else:
				return -3
			
		try:
			self.bind(conf.get('LDAPSERVER','admin'),conf.get('LDAPSERVER','passwd'))
			self.touch_by_dict({path:{'memberuid':memberuid}})
		except Exception, e:
			print e
			return -4
		
		# Remove user symlink to the group
		user_group_dir = '%s/%s/%s/groups' % (conf.get('DOMAIN','homes_root'),conf.get('DOMAIN','domain_name'),uid)
		if os.path.exists(user_group_dir):
			if os.path.exists('%s/%s' % (user_group_dir,groupname)):
				os.remove('%s/%s' % (user_group_dir,groupname))
		
		return 1
	
	def list_usergroups(self,uid):
		if self.user_exists(uid):
			return -1 # User does not exist
		path =	conf.get('LDAPSERVER','basedn')
		res = self.l.search(path,ldap.SCOPE_SUBTREE,'(& (objectClass=posixGroup) (memberUid=%s))' % uid,['cn'])

		grouplist = []
		while 1:
			sres = self.l.result(res,0)
			if sres[1]==[]:
				break
			if not sres[1][0][1].has_key('cn'):
				continue
			cn = sres[1][0][1]['cn'][0]
			grouplist += [cn]
		
		return grouplist

if __name__=='__main__':
	
	commands = {'createuser': 'Create a new system user and home directory',
	            'removeuser': 'Remove a user from',
	            'groupadd' :'Add a user to a group',
	            'groupdel': 'Remove a user to a group',
	            'listusers': 'Show a list of system users',
	            'listusergroups': 'Show a list of groups a certain user is member of'}
	
	usage = "usage: usermanager [command] [options] arg1, arg2"
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
		parser.set_usage("usage: usermanager %s [options] username" % cmd)
		parser.add_option("-g", "--givenName", dest="givenname",default=None,
		                  help="the user's given name/first name", metavar="GIVENNAME")
		parser.add_option("-f", "--familyName", dest="familyname",default=None,
		                  help="the user's family name/last name", metavar="FAMILYNAME")
		parser.add_option("-t", "--userType", dest="usertype",default=None,
		                  help="the user's account type (teacher,student,parent or other)", metavar="USERTYPE")
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
		
		parser.set_usage("usage: usermanager %s [options] username" % cmd)
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
		
		parser.set_usage("usage: usermanager %s username groupname" % cmd)
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
		
		parser.set_usage("usage: usermanager %s username groupname" % cmd)
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
		
		parser.set_usage("usage: usermanager %s [options]" % cmd)
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
		parser.set_usage("usage: usermanager %s username" % cmd)

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
