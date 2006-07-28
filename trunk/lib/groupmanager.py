#! /usr/bin/python

from sys import argv,exit
import re,grp,os,ldap
from getpass import getpass,getuser
from usermanager import UserManager


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

class GroupManager (LDAPUtil):
	def __init__(self):
		global conf
		LDAPUtil.__init__(self,conf.get('LDAPSERVER','host'))
	
	def list_groups(self,usertype):
		
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
				(conf.get('LDAPSERVER','groups_ou'),\
				conf.get('LDAPSERVER',usertype_ou),\
				conf.get('LDAPSERVER','basedn'))
		
		res = self.l.search(path,ldap.SCOPE_SUBTREE,'(& (cn=*) (objectclass=posixgroup))',\
			['cn','description'])

		group_dict = {}
		while 1:
			sres = self.l.result(res,0)
			if sres[1]==[]:
				break
			if not sres[1][0][1].has_key('cn'):
				continue
			
			cn = sres[1][0][1]['cn'][0]
			group_dict[cn] = {}
			for (k,v) in sres[1][0][1].items():
				if len(v)==1:
					group_dict[cn][k] = v[0]
				else:
					group_dict[cn][k] = v
		return group_dict
	
	def group_exists(self,groupname):
		# check if the group exists already
		print "Groupname: %s" % groupname
		res = self.l.search(conf.get('LDAPSERVER','basedn'),\
		                   ldap.SCOPE_SUBTREE,'(& (cn=%s)(objectclass=posixgroup))'%groupname,['cn'])
		sres = self.l.result(res,0)
		print sres
		if sres[1]==[]:
			return False
		return True
	
	def creategroup(self,groupname,usertype):
		"""
		Add a user to the schools authentication directory service.
		The usertype must be one of the constants TEACHER,STUDENT,PARENT or OTHER
		"""
		# check if the group exists already
		if group_exists(groupname):
			return -1
		
		if (usertype==TEACHER):
			usertype_ou = "teachers_ou"
		if (usertype==STUDENT):
			usertype_ou = "students_ou"
		if (usertype==PARENT):
			usertype_ou = "parents_ou"
		if (usertype==OTHER):
			usertype_ou = "others_ou"
		path = "%s,%s,%s,%s" % \
		  ('cn=%s'%groupname,\
		   conf.get('LDAPSERVER','groups_ou'),\
		   conf.get('LDAPSERVER',usertype_ou),\
		   conf.get('LDAPSERVER','basedn'))
		group_info = {'cn': groupname,
			'gidNumber':str(self.max(conf.get('LDAPSERVER','basedn'),
			                 'objectclass=posixgroup','gidNumber',
			                  int(conf.get('DOMAIN','gid_start')))+1),
			'objectclass':('posixGroup','top')}
		
		self.bind(conf.get('LDAPSERVER','admin'),conf.get('LDAPSERVER','passwd'))
		self.touch_by_dict({path:group_info})
		return 1

	def removegroup(self,groupname,backup_home,remove_home):
		"""
		Add a user to the schools authentication directory service.
		The usertype must be one of the constants TEACHER,STUDENT,PARENT or OTHER
		"""
		# check if the group exists
		res = self.l.search(conf.get('LDAPSERVER','basedn'),\
			ldap.SCOPE_SUBTREE,'(& (cn=%s)(objectclass=posixgroup))'%groupname,['dn','memberuid'])
		sres = self.l.result(res,0)
		if sres[1]==[]:
			return -1
		
		if sres[1][0][1].has_key('memberUid'):
			um = UserManager()
			for uid in sres[1][0][1]['memberUid']:
				um.groupdel(uid,groupname)
		
		path = sres[1][0][0]
		self.bind(conf.get('LDAPSERVER','admin'),conf.get('LDAPSERVER','passwd'))
		self.delete(path)
		
		group_path = "%s/%s/%s" % (conf.get('DOMAIN','homes_root'),conf.get('DOMAIN','domain_name'),groupname)
		if os.path.exists(os.path.normpath(group_path)):
			if backup_home:
				try:
					print "Backing up the group home folder of \"%s\"..." % groupname
					cnt = 0
					cnt_str = ''
					backup_path = "%s.bz2" % (os.path.normpath(group_path))
					while os.path.exists(backup_path):
						cnt+=1
						cnt_str = str(cnt)
						backup_path = "%s_%s.bz2" % (os.path.normpath(group_path),cnt_str)
						
					os.system('tar cjpf %s %s' % (backup_path,os.path.normpath(group_path)))
				except Exception, e:
					print e
					return -2
			if remove_home:
				try:
					print "Deleting the group home folder of \"%s\"..." % groupname
					os.system('rm %s -R -f' % (os.path.normpath(group_path)))
				except Exception, e:
					print e
					return -3
		
		return 1
		


if __name__=='__main__':
	# Commandline implementation
	commands = {'creategroup': 'Create a new system group and a group directory',
	            'removegroup': 'Remove a system group',
	            'listgroups': 'Show a list of system groups'}
	
	usage = "usage: groupmanager [command] [options] args"
	if len(argv)<2 or not commands.has_key(argv[1]):
		print usage
		print 
		print "Commands:"
		for cmd,desc in commands.items():
			print '%s - %s' % (cmd,desc)
		exit(0)
		
	cmd = argv[1]
	
	parser = OptionParser(usage=usage)

	#commands = ['creategroup','delgroup']
	#parser = OptionParser()
	
	#if len(argv)<2:
		#parser.print_help()
		#exit(0)
	#if not commands.count(argv[1]):
		#print "Commands should be one of following: "
		#for cmd in commands:
			#print cmd
		#exit(0)
		
	#cmd = argv[1]
	
	#print "Command: %s" % cmd
	
	if cmd == "creategroup":
		if os.getuid()!=0:
			print "You must be root to add groups"
			exit(0)
			
		parser.set_usage("usage: groupmanager %s [options] groupname" % cmd)
		parser.add_option("-r", "--groupRelation", dest="grouprelation",default=None,
		                  help="the group's relationship (teacher,student,parent or other)", metavar="GROUPRELATION")
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
			groupadd_res = gm.creategroup(groupname,options.grouprelation)
		except Exception, e:
			print "An error occured while writing to the user LDAP database"
			print e
			exit(0)
		if groupadd_res==-1:
			print "The group %s already exists" % groupname
			exit(0)
		
		try:
			gid = grp.getgrnam(groupname)[2]
		except Exception, e:
			print "The system could not map the group to an gid (groupid)"
			print e
			exit(0)
			
		home_path = "%s/%s/%s" % (conf.get('DOMAIN','homes_root'),conf.get('DOMAIN','domain_name'),groupname)
		if not os.path.exists(os.path.normpath(home_path)):
			os.mkdir(os.path.normpath(home_path))
		
		os.system('chgrp %d %s -R -f' % (gid,os.path.normpath(home_path)))
		os.system('chmod g+wrx %s -R -f' % (os.path.normpath(home_path)))
		print "Group created..."


	if cmd == "removegroup":
		if os.getuid()!=0:
			print "You must be root to remove groups"
			exit(0)
			
		parser.set_usage("usage: groupmanager %s [options] groupname" % cmd)
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
		
		parser.set_usage("usage: groupmanager %s [options]" % cmd)
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
