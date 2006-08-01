#! /usr/bin/python
from conf import conf
from ldaptools import LDAPUtil
from ldiftools import LDIFImporter
from mkpasswd import mkpasswd
import re,pwd,os,ldap

# User types
TEACHER = 1
STUDENT = 2
PARENT = 3
OTHER = 4

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
		"""
		List the groups of a certain user "uid"
		"""
		if not self.user_exists(uid):
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

