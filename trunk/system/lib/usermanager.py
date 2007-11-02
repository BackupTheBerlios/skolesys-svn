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

from conf import conf
from ldaptools import LDAPUtil
import hooks
import pwd,os,ldap
from skolesys.tools.mkpasswd import mkpasswd
import skolesys.definitions.userdef as userdef
import skolesys.definitions.ldapdef as ldapdef


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
	
	def list_users(self,usertype,uid=None):
		if uid==None:
			uid = '*'
		usertype_ids = userdef.list_usertypes_by_id()
		usertype_objectclasses = {}
		for id in usertype_ids:
			usertype_objectclasses[id] = ldapdef.objectclass_by_usertype(id) + ['sambaSamAccount']
			
		path = conf.get('LDAPSERVER','basedn')
		if usertype:
			path = ldapdef.basedn_by_usertype(usertype)
			if not path:
				return {}
				
		res = self.l.search(path,ldap.SCOPE_SUBTREE,'(& (uid=%s)(objectclass=posixaccount)(objectclass=person))' % uid ,[])
			
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
				if k=='objectClass':
					for usertype_id,objectclasses in usertype_objectclasses.items():
						had_all_classes = True
						for objcls in objectclasses:
							if not v.count(objcls):
								had_all_classes = False
								break
						if had_all_classes == True:
							user_dict[uid]['usertype_id'] = usertype_id
							break
					continue
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
			return -10001
		
		title = userdef.usertype_as_text(usertype)
		if not title:
			return -10005	# invalid usertype id
		usertype_ou = ldapdef.ou_confkey_by_usertype(usertype)
		objectclass = ldapdef.objectclass_by_usertype(usertype)
		if not objectclass:
			return -10006	# Object classes have not been defined for this usertype
			
		path = "uid=%s,%s" % (uid,ldapdef.basedn_by_usertype(usertype))
		
		# Check the group for existance
		import groupmanager as gman
		gm = gman.GroupManager()
		gl = gm.list_groups(None)
		glgid = {}
		for groupname in gl.keys():
			glgid[int(gl[groupname]['gidNumber'])]=groupname
		if not glgid.has_key(primarygid):
			return -10004
		
		
		#uidnumber = self.max(conf.get('LDAPSERVER','basedn'),
		#		'objectclass=posixaccount','uidNumber',
		#		int(conf.get('DOMAIN','uid_start')))+1
		
		uidnumber = None
		uidnumbers = []
		for pw in pwd.getpwall():
			if int(pw[2]) >= int(conf.get('DOMAIN','uid_start')):
				uidnumbers += [int(pw[2])]
		uidnumbers.sort()
		expect_uidnumber = int(conf.get('DOMAIN','uid_start'))
		for i in range(100000):
			if expect_uidnumber != uidnumbers[i]:
				uidnumber = expect_uidnumber
				break
			expect_uidnumber += 1
		
		if uidnumber == None:
			return -10007 # failed to pick an uidnumber
		
		cn = '%s %s' % (givenname,familyname)

		user_info = {'uid':uid,
			'givenname':'%s' % givenname,
			'cn':cn,
			'gidNumber': str(primarygid),
			'uidnumber': str(uidnumber),
			'homeDirectory':'%s/%s/users/%s/.linux' % (conf.get('DOMAIN','domain_root'),conf.get('DOMAIN','domain_name'),uid),
			'sn':'%s' % familyname,
			'objectclass':objectclass,
			'mail': uid,
			'title':title,
			'loginShell': '/bin/zsh',
			'userPassword':mkpasswd(passwd,3,'ssha')}
		if userdef.usertype_as_id(usertype) == userdef.usertype_as_id('student') and firstyear != None:
			user_info['firstSchoolYear'] = str(firstyear)
			
		
		self.bind(conf.get('LDAPSERVER','admin'),conf.get('LDAPSERVER','passwd'))
		self.touch_by_dict({path:user_info})
		
		try:
			posix_uid = pwd.getpwnam(uid)[2]
		except Exception, e:
			print e
			return -10002
		
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

		except Exception,e:
			print e
			return -10003
		w,r = os.popen2('smbpasswd -a %s -s' % uid)
		w.write('%s\n' % passwd)
		w.write('%s\n' % passwd)
		w.close()
		r.close()
		
		## Generate an SSH2 DSA private/public keypair and a putty ppk version
		linux_home_path = home_path + '/.linux'
		if not os.path.exists(os.path.normpath('%s/.ssh/' % linux_home_path)):
			# Create profile directory
			os.makedirs('%s/.ssh/' % linux_home_path)

		os.system('cp /etc/skolesys/ssh/id_dsa* %s/.ssh/' % linux_home_path)
		os.system('ssh-keygen -p -N %s -f %s/.ssh/id_dsa' % (passwd,linux_home_path))

		f=open('%s/.ssh/id_dsa.pub' % linux_home_path,'r')
		pubkey = f.read()
		f.close()

		f=open('%s/.ssh/authorized_keys' % linux_home_path,'w')
		f.write('no-port-forwarding,no-X11-forwarding,no-agent-forwarding,permitopen="%s:22",command="sleep 10000" %s' % (conf.get('TERMINAL_SERVICE','freenx'),pubkey))
		f.close()

		os.system('chmod 600 %s/.ssh/*' % linux_home_path)
		
		# Deliver ownership
		os.system('chown %d.%d %s -R -f' % (posix_uid,int(primarygid),os.path.normpath(home_path)))
		os.system('chown %d.%d %s -R -f' % (posix_uid,int(primarygid),os.path.normpath(profile_path)))

		hooks.Hooks().call_hooks('lib.usermanager.createuser',
			uid=uid, givenname=givenname, familyname=familyname,
			passwd=passwd, primarygid=primarygid, firstyear=firstyear,
			cn=cn,title=title,usertype=usertype,dn=path)

		return 0	
		
	def changeuser(self,uid,givenname=None,familyname=None,passwd=None,primarygid=None,firstyear=None,mail=None):
		"""
		Add a user to the schools authentication directory service.
		The usertype must be one of the constants TEACHER,STUDENT,PARENT or OTHER
		"""
		# check if the group exists already

		change_dict = {}
		user_info = self.list_users(None,uid)
		if not user_info.has_key(uid):
			return -10101 # user does not exist
		user_info = user_info[uid]
		
		path = user_info['dn']
		
		# Check the group for existance
		if primarygid:
			import groupmanager as gman
			gm = gman.GroupManager()
			gl = gm.list_groups(None)
			glgid = {}
			for groupname in gl.keys():
				glgid[gl[groupname]['gidNumber']]=groupname
			if not glgid.has_key(primarygid):
				return -10104
			change_dict['gidNumber'] = str(primarygid)
		cur_givenname,cur_sn = user_info['givenName'],user_info['sn']
		if givenname:
			cur_givenname = givenname
			change_dict['givenname'] = givenname
		if familyname:
			cur_sn = familyname
			change_dict['sn'] = familyname
		
		cn = cur_givenname + " " + cur_sn
		change_dict['cn'] = cn
		change_dict['displayName'] = cn
		
		if mail:
			change_dict['mail'] = mail
		if passwd:
			try:
				user_info = pwd.getpwnam(uid)
			except Exception, e:
				print e
				return -10102 # user not in accessable through nsswitch
			
			change_dict['userPassword'] = mkpasswd(passwd,3,'ssha')

			home_path = "%s/%s/users/%s" % (conf.get('DOMAIN','domain_root'),conf.get('DOMAIN','domain_name'),uid)
			linux_home_path = home_path + '/.linux'
			if not os.path.exists(os.path.normpath('%s/.ssh/' % linux_home_path)):
				# Create profile directory
				os.makedirs('%s/.ssh/' % linux_home_path)

			os.system('cp /etc/skolesys/ssh/id_dsa* %s/.ssh/' % linux_home_path)
			os.system('ssh-keygen -p -N %s -f %s/.ssh/id_dsa' % (passwd,linux_home_path))

			f=open('%s/.ssh/id_dsa.pub' % linux_home_path,'r')
			pubkey = f.read()
			f.close()

			f=open('%s/.ssh/authorized_keys' % linux_home_path,'w')
			f.write('no-port-forwarding,no-X11-forwarding,no-agent-forwarding,permitopen="%s:22",command="sleep 10000" %s' % (conf.get('TERMINAL_SERVICE','freenx'),pubkey))
			f.close()
			
			# Generate an SSH2 DSA private/public keypair and a putty ppk version
			
			os.system('chmod 600 %s/.ssh/*' % linux_home_path)
	
			# Deliver ownership
			os.system('chown %d.%d %s/.ssh -R -f' % (user_info[2],user_info[3],os.path.normpath(linux_home_path)))
				
		#if userdef.usertype_as_id(usertype) == userdef.usertype_as_id('student') and firstyear != None:
		#	change_dict['firstSchoolYear'] = str(firstyear)
		
		self.bind(conf.get('LDAPSERVER','admin'),conf.get('LDAPSERVER','passwd'))
		self.touch_by_dict({path:change_dict})
		if passwd:
			w,r = os.popen2('smbpasswd %s -s' % uid)
			w.write('%s\n' % passwd)
			w.write('%s\n' % passwd)
			w.close()
			r.close()

		hooks.Hooks().call_hooks('lib.usermanager.changeuser',
			uid=uid, givenname=givenname, familyname=familyname,
			passwd=passwd, primarygid=primarygid, firstyear=firstyear,
			mail=mail,cn=cn, displayname=cn, dn=path)
		
		return 0

		
	def deluser(self,uid,backup_home,remove_home):
		res = self.l.search(conf.get('LDAPSERVER','basedn'),ldap.SCOPE_SUBTREE,'uid=%s'%uid,['dn'])
		sres = self.l.result(res,0)
		if sres[1]==[]:
			return -10201
		try:
			self.bind(conf.get('LDAPSERVER','admin'),conf.get('LDAPSERVER','passwd'))
			self.delete(sres[1][0][0])
		except Exception, e:
			print e
			return -10202
		
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
					return -10203
			if remove_home:
				try:
					print "Deleting the homefolder of \"%s\"..." % uid
					os.system('rm %s -R -f' % (os.path.normpath(home_path)))
				except Exception, e:
					print e
					return -10204
		
		return 0

	def groupadd(self,uid,groupname):
		res = self.l.search(conf.get('LDAPSERVER','basedn'),ldap.SCOPE_SUBTREE,'(& (uid=%s) (objectclass=posixaccount)(objectclass=person))'%uid,['dn'])
		sres = self.l.result(res,0)
		if sres[1]==[]:
			return -10301
		res = self.l.search(conf.get('LDAPSERVER','basedn'),ldap.SCOPE_SUBTREE,'(& (cn=%s) (objectclass=posixgroup))'%groupname,['memberuid'])
		sres = self.l.result(res,0)
		if sres[1]==[]:
			return -10302
		attribs = sres[1][0][1]
		path = sres[1][0][0]
		memberuid = [uid]
		if attribs.has_key('memberUid'):
			if attribs['memberUid'].count(uid):
				return -10303
			memberuid += attribs['memberUid']
			
		try:
			self.bind(conf.get('LDAPSERVER','admin'),conf.get('LDAPSERVER','passwd'))
			self.touch_by_dict({path:{'memberuid':memberuid}})
		except Exception, e:
			print e
			return -10304
		
		# Create user symlink to the group
		user_group_dir = '%s/%s/users/%s/groups' % (conf.get('DOMAIN','domain_root'),conf.get('DOMAIN','domain_name'),uid)
		if not os.path.exists(user_group_dir):
			os.makedirs(user_group_dir)
		if not os.path.exists('%s/%s' % (user_group_dir,groupname)):
			os.symlink('%s/%s/groups/%s' % (conf.get('DOMAIN','domain_root'),conf.get('DOMAIN','domain_name'),groupname),
				'%s/%s' % (user_group_dir,groupname))
		
		return 0

	def groupdel(self,uid,groupname):
		# Do not check if the user exists, just remove the uid
		#res = self.l.search(conf.get('LDAPSERVER','basedn'),ldap.SCOPE_SUBTREE,'(& (uid=%s) (objectclass=posixaccount))'%uid,['dn'])
		#sres = self.l.result(res,0)
		#if sres[1]==[]:
		#	return -10401
		res = self.l.search(conf.get('LDAPSERVER','basedn'),ldap.SCOPE_SUBTREE,'(& (cn=%s) (objectclass=posixgroup))'%groupname,['memberuid'])
		sres = self.l.result(res,0)
		if sres[1]==[]:
			return -10402
		attribs = sres[1][0][1]
		path = sres[1][0][0]
		if attribs.has_key('memberUid'):
			if attribs['memberUid'].count(uid):
				memberuid = attribs['memberUid']
				memberuid.remove(uid)
			else: return -10403
		else: return -10403
			
		try:
			self.bind(conf.get('LDAPSERVER','admin'),conf.get('LDAPSERVER','passwd'))
			self.touch_by_dict({path:{'memberuid':memberuid}})
		except Exception, e:
			print e
			return -10404
		
		# Remove user symlink to the group
		user_group_dir = '%s/%s/users/%s/groups' % (conf.get('DOMAIN','domain_root'),conf.get('DOMAIN','domain_name'),uid)
		if os.path.exists(user_group_dir):
			if os.path.exists('%s/%s' % (user_group_dir,groupname)):
				os.remove('%s/%s' % (user_group_dir,groupname))
		
		return 0
	
	def list_usergroups(self,uid):
		"""
		List the groups of a certain user "uid"
		"""
		if not self.user_exists(uid):
			return -10501 # User does not exist
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

	
	def authenticate(self,uid,passwd):
		userinfo = self.list_users(None,uid)
		if not userinfo.has_key(uid):
			# User does not exist
			return -10601
		
		res_id = self.l.simple_bind(userinfo[uid]['dn'],passwd)
		try:
			res = self.l.result(res_id)
		except ldap.LDAPError, e:
			# Invalid credentials
			return -10603
		
		if res[0]==97:
			return 0

		# Other undefined error
		return -10602


