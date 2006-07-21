import SOAPpy
import pickle
from p2 import p2_encrypt
from marshall import pdump,pload
import sys

class L4S_Client:
	def __init__(self,host,port=None,log=sys.stderr):
		self.logfile = log
		if port:
			self.server = SOAPpy.SOAPProxy("%s:%d/" % (host,port))
		else:
			self.server = SOAPpy.SOAPProxy(host)
		self._get_id()

	def logtext(self,txt):
		if self.logfile:
			self.logfile.write("%s\n" % txt)

	def _get_id(self):
		self.session_id = pload(self.server.get_id())
		if self.session_id:
			self.logtext("RECIEVED SESSIONID: %s" % self.session_id)
		else:
			self.logtext("(!!) NO SESSIONID RECIEVED")

	def bind(self,plain_passwd):
		nonce = pload(self.server.challenge_response_key(pdump(self.session_id)))
		if nonce:
			self.logtext("BIND-CHALLENGE NONCE: %s" % nonce)
		else:
			self.logtext("(!!) NO BIND-CHALLENGE NONCE RECIEVED")
			return False
		passwd_encrypted = p2_encrypt(plain_passwd,nonce)
		return pload(self.server.bind(pdump(self.session_id),pdump(passwd_encrypted)))

	def test_session_id(self):
		"Test if the proxy has a valid session id"
		return pload(self.server.test_session_id(pdump(self.session_id)))

	def test_binded(self):
		"Test if the proxy is still binded"
		return pload(self.server.test_binded(pdump(self.session_id)))

	def domain_name(self):
		"""
		Get the domain name of the mainserver which is also the primary
		suffix of LDAP posixusers uid.
		"""
		return pload(self.server.domain_name(pdump(self.session_id)))

	def list_users(self,type=None):
		"""
		Get a list of LDAP posixusers located on the mainserver. Optionally the
		list can be filtered by the user type.
		"""
		return pload(self.server.list_users(pdump(self.session_id),pdump(type)))

	def user_exists(self,uid):
		"""
		Do a quick lookup in the mainserver LDAP to see if a 
		certain uid exists.
		"""
		return pload(self.server.user_exists(pdump(self.session_id),pdump(uid)))
	
	
	def createuser(self,uid,givenname,familyname,passwd,usertype):
		return pload(self.server.createuser(pdump(self.session_id),pdump(uid),pdump(givenname),\
			pdump(familyname),pdump(passwd),pdump(usertype)))

	def removeuser(self,uid,backup_home=False,remove_home=False):
		return pload(self.server.removeuser(pdump(self.session_id),pdump(uid),pdump(backup_home),pdump(remove_home)))

	def test(self,str):
		self.server.test(pdump(str))

if __name__=='__main__':
    c=L4S_Client('https://127.0.0.1',8443)
    print c.bind('secret')
    userdict = c.list_users(4)
    for user in userdict.keys():
        print user
