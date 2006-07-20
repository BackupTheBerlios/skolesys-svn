import ldap
import os.path

def trace_info(str):
	pass
	return
	#print str

class LDAPUtil:
	def __init__(self,host):
		try:
			self.l = ldap.open(host)
		except ldap.LDAPError, e:
			print e
			# handle error however you like
		self.l.protocol_version = ldap.VERSION3
		
	def bind(self,dn,passwd):
		try:
			self.l.simple_bind(dn, passwd)
		except ldap.LDAPError, e:
			print e
			# handle error however you like
		
	def delete(self,dn,allow_recursion=0):
		res = self.l.search(dn, ldap.SCOPE_ONELEVEL , 'objectClass=*' ,['dn'])
		while 1 and allow_recursion:
			sres = self.l.result(res, 0)
			if sres[1]==[]:
				break
			
			self.delete(sres[1][0][0],1)
		trace_info("deleting %s" % dn)
		self.l.delete_s(dn)
		
	def touch_by_dict(self,entry_dict):
		"""
		Touch some ldap entries. Touch meens try to add them if not existing otherwise
		modify entries that already exist.
		entry_dict {dn: attr_dict, dn2: attr2_dict ...}
		"""
		for dn,attr in entry_dict.items():
			try:
				res = self.l.search(dn, ldap.SCOPE_SUBTREE , 'objectClass=*' )
				sres = self.l.result(res,0)
				
			except Exception, e:
				# new entry - try to add
				attributes = [ (k,v) for k,v in attr.items() ]
				self.l.add_s(dn,attributes)
				return
			
			# Existing entry - try to modify
			# Make lowercase attribute dict
			lower_attr = {} 
			for k,v in sres[1][0][1].items():
				lower_attr[k.lower()] = v
			# create modify list
			modlist = []
			for k,v in attr.items():
				if lower_attr.has_key(k.lower()):
					if isinstance(v,list) or \
					   isinstance(v,tuple):
						v = list(v) 
					else:
						v = [v]
					trace_info(str(lower_attr[k.lower()]) + " => " + str(v))
					if lower_attr[k.lower()] != v:
						modlist += [(ldap.MOD_REPLACE,k,v)]
				else:
					modlist += [(ldap.MOD_ADD,k,v)]
			for mod in modlist:
				trace_info(mod)
			self.l.modify_s(dn,modlist)
			
	def max(self,fromdn,search,attr,start_at=0):
		res= self.l.search(fromdn,ldap.SCOPE_SUBTREE,search,[attr])
		max = start_at
		while 1:
			sres = self.l.result(res, 0)
			if sres[1] == []:
				break
			if int(sres[1][0][1][attr][0])>max:
				max = int(sres[1][0][1][attr][0])
		return max

#path = 'ou=People,dc=minskole,dc=lin4schools,dc=org'
#user_info = {'uid':'hans@minskole.dk',
#	'givenname':'Hans',
#	'cn':'Hans Simon-Gaarde',
#	'gidNumber':'1000',
#	#'uidnumber':'2002',
#	'homeDirectory':'/home/minskole.dk/hans@minskole.dk',
#	'sn':'Hans',
#	'telephonenumber':'86929622',
#	'objectclass':('inetOrgPerson','organizationalPerson','posixAccount','shadowAccount','person', 'Top'),
#	'mail':'hans@simon-gaarde.dk',
#	'title':'programmer',
#	'userPassword':mkpasswd('bdnprrfe',3,'crypt')}

#id='uid=%s,%s' % (user_info['uid'],path)
#attributes=[ (k,va) for k,v in user_info.items() ]
#l.add_s(id,attributes)

if __name__=='__main__':
	test = LDAPUtil('ldapserver')
	