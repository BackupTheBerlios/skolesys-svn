#! /usr/bin/python
from conf import conf
from ldaptools import LDAPUtil
from ldiftools import LDIFImporter
import re,grp,pwd,os,ldap
from skolesys.tools.mkpasswd import mkpasswd
import skolesys.definitions.userdef as userdef
import skolesys.definitions.ldapdef as ldapdef

#-------------------------------------
#---------- GroupManager -------------

class GroupManager (LDAPUtil):
	def __init__(self):
		global conf
		LDAPUtil.__init__(self,conf.get('LDAPSERVER','host'))
	
	def list_groups(self,grouptype):
		
		path = conf.get('LDAPSERVER','basedn')
		if grouptype:
			path = ldapdef.basedn_by_grouptype(grouptype)
			if not path:
				return {}
			
		
		res = self.l.search(path,ldap.SCOPE_SUBTREE,'(& (cn=*) (objectclass=posixgroup))',\
			['cn','description','gidNumber'])

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
	
	def creategroup(self,groupname,grouptype,description=None,force_gid=None):
		"""
		Add a user to the schools authentication directory service.
		The grouptype must be one of the constants PRIMARY, SYSTEM or COMBI
		"""
		if description=='':
			description=None
		# check if the group exists already
		if self.group_exists(groupname):
			return -1
	
		path = "cn=%s,%s" % (groupname,ldapdef.basedn_by_grouptype(grouptype))
		if not path:
			return -4	# invalid grouptype
		
		if force_gid:
			gid = force_gid
		else:
			gid = self.max(conf.get('LDAPSERVER','basedn'),
				'objectclass=posixgroup','gidNumber',
				int(conf.get('DOMAIN','gid_start')))+1
		group_info = {'cn': groupname,
			'gidNumber':str(gid),
			'objectclass':ldapdef.objectclass_by_grouptype(grouptype)}
		
		if description:
			group_info['description'] = description
		
		self.bind(conf.get('LDAPSERVER','admin'),conf.get('LDAPSERVER','passwd'))
		self.touch_by_dict({path:group_info})
		
		try:
			gid = grp.getgrnam(groupname)[2]
		except Exception, e:
			print e
			return -2
		
		try:
			home_path = "%s/%s/groups/%s" % (conf.get('DOMAIN','domain_root'),conf.get('DOMAIN','domain_name'),groupname)
			if not os.path.exists(os.path.normpath(home_path)):
				os.mkdir(os.path.normpath(home_path))
			
			os.system('chgrp %d %s -R -f' % (gid,os.path.normpath(home_path)))
			os.system('chmod g+wrs,o-rwx %s -R -f' % (os.path.normpath(home_path)))
		except Exception, e:
			print e
			return -3
		
		return 1

	def removegroup(self,groupname,backup_home,remove_home):
		"""
		Remove a group 
		Setting backup_home to True will create a tarball backup of the group's homedir
		Setting remove_home to True truncate the gruop's homedir
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
		
		group_path = "%s/%s/groups/%s" % (conf.get('DOMAIN','domain_root'),conf.get('DOMAIN','domain_name'),groupname)
		if os.path.exists(os.path.normpath(group_path)):
			# The group has a homedir, maybe do stuff...
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



#---------------------------------
#--------- UserManager -----------

class UserManager (LDAPUtil):
	"""
	UserManager handles all operations related to user management. The class is also
	responsible for creating and user home directories and creating links in user home
	directories to connected groups.
	This includes:
		* Creating/modifying users
		* Removing users
		* Listing users
		* Connecting users and groups
	"""
	def __init__(self):
		global conf
		LDAPUtil.__init__(self,conf.get('LDAPSERVER','host'))
	
	def list_users(self,usertype):
		path = conf.get('LDAPSERVER','basedn')
		if usertype:
			path = ldapdef.basedn_by_usertype(usertype)
			if not path:
				return {}
				
		res = self.l.search(path,ldap.SCOPE_SUBTREE,'(& (uid=*)(objectclass=posixaccount)(objectclass=person))',[])
			
		user_dict = {}
		while 1:
			sres = self.l.result(res,0)
			if sres[1]==[]:
				break
			if not sres[1][0][1].has_key('uid'):
				continue
			
			uid = sres[1][0][1]['uid'][0]
			user_dict[uid] = {}
			user_dict[uid]['dn'] = sres[1][0][0]
			for (k,v) in sres[1][0][1].items():
				if len(v)==1:
					user_dict[uid][k] = v[0]
				else:
					user_dict[uid][k] = v
		return user_dict
	
	def user_exists(self,uid):
		res = self.l.search(conf.get('LDAPSERVER','basedn'),\
		                   ldap.SCOPE_SUBTREE,'(& (uid=%s)(objectclass=posixaccount)(objectclass=person))'%uid,['dn'])
		
		sres = self.l.result(res,0)
		
		if sres[1]==[]:
			return False
		return True

	
	def createuser(self,uid,givenname,familyname,passwd,usertype,primarygid=1000,firstyear=None):
		"""
		Add a user to the schools authentication directory service.
		The usertype must be one of the constants TEACHER,STUDENT,PARENT or OTHER
		"""
		# check if the group exists already
		if self.user_exists(uid):
			return -1
		
		title = userdef.usertype_as_text(usertype)
		if not title:
			return -5	# invalid usertype id
		usertype_ou = ldapdef.ou_confkey_by_usertype(usertype)
		objectclass = ldapdef.objectclass_by_usertype(usertype)
		if not objectclass:
			return -6	# Object classes have not been defined for this usertype
			
		path = "uid=%s,%s" % (uid,ldapdef.basedn_by_usertype(usertype))
		
		# Check the group for existance
		gm = GroupManager()
		gl = gm.list_groups(None)
		glgid = {}
		for groupname in gl.keys():
			glgid[gl[groupname]['gidNumber']]=groupname
		if not glgid.has_key(primarygid):
			return -4
		
		user_info = {'uid':uid,
			'givenname':'%s' % givenname,
			'cn':'%s %s' % (givenname,familyname),
			'gidNumber': str(primarygid),
			'uidnumber': str(self.max(conf.get('LDAPSERVER','basedn'),
				'objectclass=posixaccount','uidNumber',
				int(conf.get('DOMAIN','uid_start')))+1),
			'homeDirectory':'%s/%s/users/%s/.linux' % (conf.get('DOMAIN','domain_root'),conf.get('DOMAIN','domain_name'),uid),
			'sn':'%s' % givenname,
			'objectclass':objectclass,
			'mail': uid,
			'title':title,
			'userPassword':mkpasswd(passwd,3,'crypt')}
		if userdef.usertype_as_id(usertype) == userdef.usertype_as_id('student') and firstyear != None:
			user_info['firstSchoolYear'] = str(firstyear)
			
		
		self.bind(conf.get('LDAPSERVER','admin'),conf.get('LDAPSERVER','passwd'))
		self.touch_by_dict({path:user_info})
		
		try:
			posix_uid = pwd.getpwnam(uid)[2]
		except Exception, e:
			print e
			return -2
		
		try:
			# Home directory
			home_path = "%s/%s/users/%s" % (conf.get('DOMAIN','domain_root'),conf.get('DOMAIN','domain_name'),uid)
			if not os.path.exists(os.path.normpath(home_path)):
				# Copy the user skel
				os.system('cp /etc/skolesys/skel/ %s -Rf' % os.path.normpath(home_path))

			# Prepare for windows roaming profiles
			profile_path = "%s/%s/profiles/%s" % (conf.get('DOMAIN','domain_root'),conf.get('DOMAIN','domain_name'),uid)
			if not os.path.exists(os.path.normpath(profile_path)):
				# Create profile directory
				os.makedirs(profile_path)

			# Deliver ownership
			os.system('chown %d.%d %s -R -f' % (posix_uid,int(primarygid),os.path.normpath(home_path)))
			os.system('chown %d.%d %s -R -f' % (posix_uid,int(primarygid),os.path.normpath(profile_path)))

		except Exception,e:
			print e
			return -3
		w,r = os.popen2('smbpasswd -a %s -s' % uid)
		w.write('%s\n' % passwd)
		w.write('%s\n' % passwd)
		w.close()
		r.close()
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
		home_path = "%s/%s/users/%s" % (conf.get('DOMAIN','domain_root'),conf.get('DOMAIN','domain_name'),uid)
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
		res = self.l.search(conf.get('LDAPSERVER','basedn'),ldap.SCOPE_SUBTREE,'(& (uid=%s) (objectclass=posixaccount)(objectclass=person))'%uid,['dn'])
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
		user_group_dir = '%s/%s/users/%s/groups' % (conf.get('DOMAIN','domain_root'),conf.get('DOMAIN','domain_name'),uid)
		if not os.path.exists(user_group_dir):
			os.makedirs(user_group_dir)
		if not os.path.exists('%s/%s' % (user_group_dir,groupname)):
			os.symlink('%s/%s/groups/%s' % (conf.get('DOMAIN','domain_root'),conf.get('DOMAIN','domain_name'),groupname),
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
			else: return -3
		else: return -3
			
		try:
			self.bind(conf.get('LDAPSERVER','admin'),conf.get('LDAPSERVER','passwd'))
			self.touch_by_dict({path:{'memberuid':memberuid}})
		except Exception, e:
			print e
			return -4
		
		# Remove user symlink to the group
		user_group_dir = '%s/%s/users/%s/groups' % (conf.get('DOMAIN','domain_root'),conf.get('DOMAIN','domain_name'),uid)
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

