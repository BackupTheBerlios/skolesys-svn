#! /usr/bin/python
from conf import conf
from ldaptools import LDAPUtil
import grp,os,ldap,copy
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
	
	def creategroup(self,groupname,displayed_name,grouptype,description=None,force_gid=None):
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
		
		if not displayed_name or len(displayed_name.strip())==0:
			return -5
		
		if force_gid:
			gid = force_gid
		else:
			gid = self.max(conf.get('LDAPSERVER','basedn'),
				'objectclass=posixgroup','gidNumber',
				int(conf.get('DOMAIN','gid_start')))+1
		group_info = {'cn': groupname,
			'gidNumber':str(gid),
			'displayedName': str(displayed_name)
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
		
		return 0

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
		
		return 0
		
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


	def list_services(self,groupname=None):
		"""
		List groupservice names.
		If groupname is set the services attached to the particular group is returned,
		otherwise all all available groupservices are returned.
		"""
		if not groupname:
			import skolesys.services as s
			return s.groupservices()
		
		res = self.l.search(conf.get('LDAPSERVER','basedn'),\
			ldap.SCOPE_SUBTREE,'(& (cn=%s)(objectclass=skoleSysServiceGroup))'%groupname,['servicelist'])
		
		sres = self.l.result(res,0)
		if sres[1]==[]:
			return -1 # Group does not exist
		
		servicelist = []
		if sres[1][0][1].has_key('serviceList'):
			servicelist = sres[1][0][1]['serviceList']
		return servicelist

	
	def list_service_options_available(self,servicename,groupname=None):
		"""
		Fetch a dictionary describing the options available for a certain group service.
		It can only be used in combination with a groupname since it is legal to have options_available
		change dynamically i.e. as a function of the options already set. F.inst. if an option is "use_pop3"
		the options_available might change by adding options like "use_ssl" and "pop3_server".
		SkoleSYS UI is implemented with this in mind.
		"""
		if groupname:
			res = self.l.search(conf.get('LDAPSERVER','basedn'),\
				ldap.SCOPE_SUBTREE,'(& (cn=%s)(objectclass=skoleSysServiceGroup))'%groupname,['dn','memberuid','servicelist'])
		
			sres = self.l.result(res,0)
			if sres[1]==[]:
				return -1 # Group does not exist
		
			dn = sres[1][0][0]
			servicelist = []
			if sres[1][0][1].has_key('serviceList'):
				servicelist = sres[1][0][1]['serviceList']
			
			if not servicelist.count(servicename):
				return -4 # Group is not attached to the service
		else:
			groupname = "dummy"
			print "WARNING: No groupname to the list_service_options_available(). There is no garantee " + \
				"That this will work, som services build there options dynamically from options already set"
		
		import skolesys.services as s
		if not s.groupservices().count(servicename):
			return -2 # the service does not exist
		service_inst = s.create_groupserviceinterface(servicename,groupname)
		if not service_inst:
			return -3 # the service failed to load
		opts_avail = copy.deepcopy((service_inst.get_options_available()))
		cur_options = service_inst.get_options()
		if cur_options:
			for var,val in cur_options.items():
				if opts_avail.has_key(var):
					opts_avail[var]['value'] = val	
		return opts_avail


	def get_service_option_values(self,groupname,servicename):
		res = self.l.search(conf.get('LDAPSERVER','basedn'),\
			ldap.SCOPE_SUBTREE,'(& (cn=%s)(objectclass=skoleSysServiceGroup))'%groupname,['dn','memberuid','servicelist'])
	
		sres = self.l.result(res,0)
		if sres[1]==[]:
			return -1 # Group does not exist
	
		dn = sres[1][0][0]
		servicelist = []
		if sres[1][0][1].has_key('serviceList'):
			servicelist = sres[1][0][1]['serviceList']
		
		if not servicelist.count(servicename):
			return -4 # Group is not attached to the service
		
		import skolesys.services as s
		if not s.groupservices().count(servicename):
			return -2 # the service does not exist
		service_inst = s.create_groupserviceinterface(servicename,groupname)
		if not service_inst:
			return -3 # the service failed to load
		cur_options = dict(service_inst.get_options())
		return cur_options


	def set_service_option_value(self,groupname,servicename,variable,value):
		res = self.l.search(conf.get('LDAPSERVER','basedn'),\
			ldap.SCOPE_SUBTREE,'(& (cn=%s)(objectclass=skoleSysServiceGroup))'%groupname,['dn','memberuid','servicelist'])
	
		sres = self.l.result(res,0)
		if sres[1]==[]:
			return -1 # Group does not exist
	
		dn = sres[1][0][0]
		servicelist = []
		if sres[1][0][1].has_key('serviceList'):
			servicelist = sres[1][0][1]['serviceList']
		
		if not servicelist.count(servicename):
			return -4 # Group is not attached to the service
		
		import skolesys.services as s
		if not s.groupservices().count(servicename):
			return -2 # the service does not exist
		service_inst = s.create_groupserviceinterface(servicename,groupname)
		if not service_inst:
			return -3 # the service failed to load
		
		return service_inst.set_option(variable,value)


	def unset_service_option(self,groupname,servicename,variable):
		res = self.l.search(conf.get('LDAPSERVER','basedn'),\
			ldap.SCOPE_SUBTREE,'(& (cn=%s)(objectclass=skoleSysServiceGroup))'%groupname,['dn','memberuid','servicelist'])
	
		sres = self.l.result(res,0)
		if sres[1]==[]:
			return -1 # Group does not exist
	
		dn = sres[1][0][0]
		servicelist = []
		if sres[1][0][1].has_key('serviceList'):
			servicelist = sres[1][0][1]['serviceList']
		
		if not servicelist.count(servicename):
			return -4 # Group is not attached to the service
		
		import skolesys.services as s
		if not s.groupservices().count(servicename):
			return -2 # the service does not exist
		service_inst = s.create_groupserviceinterface(servicename,groupname)
		if not service_inst:
			return -3 # the service failed to load
		
		return service_inst.unset_option(variable)


	def attach_service(self,groupname,servicename):
		"""
		Attach the groupservice servicename to the group groupname
		"""
		res = self.l.search(conf.get('LDAPSERVER','basedn'),\
			ldap.SCOPE_SUBTREE,'(& (cn=%s)(objectclass=skoleSysServiceGroup))'%groupname,['dn','memberuid','servicelist'])
		
		sres = self.l.result(res,0)
		if sres[1]==[]:
			return -1 # Group does not exist
		
		memberlist = []
		if sres[1][0][1].has_key('memberUid'):
			memberlist = sres[1][0][1]['memberUid']
		
		dn = sres[1][0][0]
		servicelist = []
		if sres[1][0][1].has_key('serviceList'):
			servicelist = sres[1][0][1]['serviceList']
		if servicelist.count(servicename):
			return -4 # service is already enabled
		
		import skolesys.services as s
		if not s.groupservices().count(servicename):
			return -2 # the service does not exist
		service_inst = s.create_groupserviceinterface(servicename,groupname)
		if not service_inst:
			return -3 # the service failed to load
		
		print "Attach service %s\non group %s\naffecting users: %s" % (servicename,groupname,','.join(memberlist))
		res = service_inst.hook_attachservice(memberlist)
		if not res==0:
			# Service hook failed
			print "The service attachment did not succeed"
			return res
		
		servicelist += [servicename]
		self.bind(conf.get('LDAPSERVER','admin'),conf.get('LDAPSERVER','passwd'))
		self.touch_by_dict({dn:{'serviceList': servicelist}})
		return 0

	def detach_service(self,groupname,servicename):
		"""
		Detach the groupservice servicename from the group groupname
		"""
		res = self.l.search(conf.get('LDAPSERVER','basedn'),\
			ldap.SCOPE_SUBTREE,'(& (cn=%s)(objectclass=skoleSysServiceGroup))'%groupname,['dn','memberuid','servicelist'])
		
		sres = self.l.result(res,0)
		if sres[1]==[]:
			return -1 # Group does not exist
		
		memberlist = []
		if sres[1][0][1].has_key('memberUid'):
			memberlist = sres[1][0][1]['memberUid']
		
		dn = sres[1][0][0]
		servicelist = []
		if sres[1][0][1].has_key('serviceList'):
			servicelist = sres[1][0][1]['serviceList']
		if not servicelist.count(servicename):
			return -4 # service is not enabled
			
		import skolesys.services as s
		if not s.groupservices().count(servicename):
			return -2 # the service does not exist
		
		service_inst = s.create_groupserviceinterface(servicename,groupname)
		if not service_inst:
			return -3 # the service failed to load
		
		print "Detach service %s\non group %s\naffecting users: %s" % (servicename,groupname,','.join(memberlist))
		service_inst.hook_detachservice(memberlist)
		servicelist.remove(servicename)
		self.bind(conf.get('LDAPSERVER','admin'),conf.get('LDAPSERVER','passwd'))
		self.touch_by_dict({dn:{'serviceList': servicelist}})
		return 0
