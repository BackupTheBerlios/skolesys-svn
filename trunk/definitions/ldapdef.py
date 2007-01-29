import userdef
import groupdef

_ldap_userstruct = {}

_ldap_userstruct['ou_confkey'] = {
	userdef.usertype_as_id('teacher') : 'teachers_ou',
	userdef.usertype_as_id('student') : 'students_ou',
	userdef.usertype_as_id('parent') : 'parents_ou',
	userdef.usertype_as_id('other') : 'others_ou',
	None : 'undefined_ou' }

_ldap_userstruct['objectclass'] = {
	userdef.usertype_as_id('teacher') : ['inetOrgPerson','organizationalPerson','posixAccount','shadowAccount','person', 'top', 'skoleSysTeacher'],
	userdef.usertype_as_id('student') : ['inetOrgPerson','organizationalPerson','posixAccount','shadowAccount','person', 'top', 'skoleSysStudent'],
	userdef.usertype_as_id('parent') : ['inetOrgPerson','organizationalPerson','posixAccount','shadowAccount','person', 'top', 'skoleSysParent'],
	userdef.usertype_as_id('other') : ['inetOrgPerson','organizationalPerson','posixAccount','shadowAccount','person', 'top', 'skoleSysOther'],
	None : ['inetOrgPerson','organizationalPerson','posixAccount','shadowAccount','person', 'top']}


def objectclass_by_usertype(usertype=None):
	global _ldap_userstruct
	
	if _ldap_userstruct['objectclass'].has_key(userdef.usertype_as_id(usertype)):
		return _ldap_userstruct['objectclass'][userdef.usertype_as_id(usertype)]
	
	return None

def ou_confkey_by_usertype(usertype=None):
	global _ldap_userstruct
	
	if _ldap_userstruct['ou_confkey'].has_key(userdef.usertype_as_id(usertype)):
		return _ldap_userstruct['ou_confkey'][userdef.usertype_as_id(usertype)]
	
	return None

def basedn_by_usertype(usertype=None):
	confkey = ou_confkey_by_usertype(usertype)
	if not confkey:
		return None
	
	from skolesys.lib.conf import conf
	try:
		basedn = conf.get('LDAPSERVER','basedn')
		user_ou = conf.get('LDAPSERVER','logins_ou')
		usertype_ou = conf.get('LDAPSERVER',confkey)
	except:
		return None
	return "%s,%s,%s" % (usertype_ou,user_ou,basedn)


_ldap_groupstruct = {}

_ldap_groupstruct['ou_confkey'] = {
	groupdef.grouptype_as_id('primary') : 'primary_ou',
	groupdef.grouptype_as_id('system') : 'system_ou',
	groupdef.grouptype_as_id('service') : 'service_ou',
	None : 'undefined_ou' }

_ldap_groupstruct['objectclass'] = {
	groupdef.grouptype_as_id('primary') : ['top', 'skoleSysPrimaryGroup'],
	groupdef.grouptype_as_id('system') : ['top', 'skoleSysSystemGroup'],
	groupdef.grouptype_as_id('service') : ['top', 'skoleSysServiceGroup'],
	None : ['top','posixGroup']}


def objectclass_by_grouptype(grouptype=None):
	global _ldap_groupstruct
	
	if _ldap_groupstruct['objectclass'].has_key(groupdef.grouptype_as_id(grouptype)):
		return _ldap_groupstruct['objectclass'][groupdef.grouptype_as_id(grouptype)]
	
	return None

def ou_confkey_by_grouptype(grouptype=None):
	global _ldap_groupstruct
	
	if _ldap_groupstruct['ou_confkey'].has_key(groupdef.grouptype_as_id(grouptype)):
		return _ldap_groupstruct['ou_confkey'][groupdef.grouptype_as_id(grouptype)]
	
	return None

def basedn_by_grouptype(grouptype=None):
	confkey = ou_confkey_by_grouptype(grouptype)
	if not confkey:
		return None
	
	from skolesys.lib.conf import conf
	try:
		basedn = conf.get('LDAPSERVER','basedn')
		group_ou = conf.get('LDAPSERVER','groups_ou')
		grouptype_ou = conf.get('LDAPSERVER',confkey)
	except:
		return None
	return "%s,%s,%s" % (grouptype_ou,group_ou,basedn)

