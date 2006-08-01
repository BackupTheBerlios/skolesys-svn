#! /usr/bin/python
from conf import conf
from ldaptools import LDAPUtil
from ldiftools import LDIFImporter
import re,grp,os,ldap
from usermanager import UserManager

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
		res = self.l.search(conf.get('LDAPSERVER','basedn'),\
		                   ldap.SCOPE_SUBTREE,'(& (cn=%s)(objectclass=posixgroup))'%groupname,['cn'])
		sres = self.l.result(res,0)
		if sres[1]==[]:
			return False
		return True
	
	def creategroup(self,groupname,usertype,description=None):
		"""
		Add a user to the schools authentication directory service.
		The usertype must be one of the constants TEACHER,STUDENT,PARENT or OTHER
		"""
		# check if the group exists already
		if self.group_exists(groupname):
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
			'objectclass':('posixGroup','top'),
			'description':description}
		
		self.bind(conf.get('LDAPSERVER','admin'),conf.get('LDAPSERVER','passwd'))
		self.touch_by_dict({path:group_info})
		
		try:
			gid = grp.getgrnam(groupname)[2]
		except Exception, e:
			print e
			return -2
		
		try:
			home_path = "%s/%s/%s" % (conf.get('DOMAIN','homes_root'),conf.get('DOMAIN','domain_name'),groupname)
			if not os.path.exists(os.path.normpath(home_path)):
				os.mkdir(os.path.normpath(home_path))
			
			os.system('chgrp %d %s -R -f' % (gid,os.path.normpath(home_path)))
			os.system('chmod g+wrx %s -R -f' % (os.path.normpath(home_path)))
		except Exception, e:
			print e
			return -3
		
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
		
	def list_members(self,groupname):
		"""
		List the members of a certain group "groupname"
		"""
		res = self.l.search(conf.get('LDAPSERVER','basedn'),\
			ldap.SCOPE_SUBTREE,'(& (cn=%s)(objectclass=posixgroup))'%groupname,['memberuid'])
		
		members = []
		sres = self.l.result(res,0)
		if sres[1]==[]:
			return -1 # Group does not exist
		if not sres[1][0][1].has_key('memberUid'):
			return [] # no members
		return sres[1][0][1]['memberUid']
	


