import userdef

_ldap_struct = {}

_ldap_struct['ou_confkey'] = {
	userdef.usertype_as_id('teacher') : 'teachers_ou',
	userdef.usertype_as_id('student') : 'students_ou',
	userdef.usertype_as_id('parent') : 'parents_ou',
	userdef.usertype_as_id('other') : 'others_ou',
	None : 'undefined_ou' }

_ldap_struct['objectclass'] = {
	userdef.usertype_as_id('teacher') : ('inetOrgPerson','organizationalPerson','posixAccount','shadowAccount','person', 'top', 'skoleSysTeacher'),
	userdef.usertype_as_id('student') : ('inetOrgPerson','organizationalPerson','posixAccount','shadowAccount','person', 'top', 'skoleSysStudent'),
	userdef.usertype_as_id('parent') : ('inetOrgPerson','organizationalPerson','posixAccount','shadowAccount','person', 'top', 'skoleSysParent'),
	userdef.usertype_as_id('other') : ('inetOrgPerson','organizationalPerson','posixAccount','shadowAccount','person', 'top', 'skoleSysOther'),
	None : ('inetOrgPerson','organizationalPerson','posixAccount','shadowAccount','person', 'top')}


def objectclass_by_usertype(usertype=None):
	global _ldap_struct
	
	if _ldap_struct['objectclass'].has_key(userdef.usertype_as_id(usertype)):
		return _ldap_struct['objectclass'][userdef.usertype_as_id(usertype)]
	
	return None

def ou_confkey_by_usertype(usertype=None):
	global _ldap_struct
	
	if _ldap_struct['ou_confkey'].has_key(userdef.usertype_as_id(usertype)):
		return _ldap_struct['ou_confkey'][userdef.usertype_as_id(usertype)]
	
	return None
