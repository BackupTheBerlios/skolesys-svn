#! /usr/bin/python
from conf import conf
from ldaptools import LDAPUtil
import grp,os,ldap
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
		The grouptype must be one of the constants PRIMARY, SYSTEM or SERVICE
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
			import usermanager as uman
			um = uman.UserManager()
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


	def attach_service(self,groupname,servicename):
		"""
		Attach the groupservice servicename to the group groupname
		"""
		res = self.l.search(conf.get('LDAPSERVER','basedn'),\
			ldap.SCOPE_SUBTREE,'(& (cn=%s)(objectclass=skoleSysServiceGroup))'%groupname,['dn','memberuid','servicelist'])
		
		sres = self.l.result(res,0)
		if sres[1]==[]:
			return -1 # Group does not exist
		
		print sres[1][0][1]['dn']
		memberlist = []
		if sres[1][0][1].has_key('memberUid'):
			memberlist = sres[1][0][1]['memberUid']
			
		servicelist = []
		if sres[1][0][1].has_key('serviceList'):
			if sres[1][0][1]['serviceList'].count(servicename):
				return -4 # service is already enabled
		import skolesys.services as s
		if not s.groupservices().count(servicename):
			return -2 # the service does not exist
		service_inst = s.get_serviceinterface(servicename)
		if not service_inst:
			return -3 # the service failed to load
		
		print "Attach service %s\non group %s\naffecting users: %s" % (servicename,groupname,','.join(memberlist))
		service_inst.hook_attachservice(groupname,memberlist)
		touch_by_dict

	def detach_service(self,groupname,servicename):
		"""
		Attach the groupservice servicename to the group groupname
		"""
		res = self.l.search(conf.get('LDAPSERVER','basedn'),\
			ldap.SCOPE_SUBTREE,'(& (cn=%s)(objectclass=skoleSysServiceGroup))'%groupname,['dn','memberuid','servicelist'])
		
		sres = self.l.result(res,0)
		if sres[1]==[]:
			return -1 # Group does not exist
		memberlist = sres[1][0][1]['memberUid']
		import skolesys.services as s
		if not s.groupservices().count(servicename):
			return -2 # the service does not exist
		service_inst = s.get_serviceinterface(servicename)
		if not service_inst:
			return -3 # the service failed to load
		
		print "Attach service %s\non group %s\naffecting users: %s" % (servicename,groupname,','.join(memberlist))
		service_inst.hook_detachservice(groupname,memberlist)
