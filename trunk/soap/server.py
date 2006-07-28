import inspect
import os.path
import SOAPpy
import md5
import pickle
import lin4schools
import lin4schools.lib.usermanager as userman
import lin4schools.lib.groupmanager as grpman
from lin4schools.lib.conf import conf
from M2Crypto import SSL
from p2 import p2_decrypt
import time
import random
from marshall import pdump,pload
from netinfo import get_ip_address
from sys import exit

random.seed(time.time())

sessions = {}

def session_valid(session_id):
	if sessions.has_key(session_id):
		if sessions[session_id].has_key('authenticated'):
			return sessions[session_id]['authenticated']
	return False

def test_session_id(session_id):
	"""
	Test if the given session ID is still valid
	"""
	session_id=pload(session_id)
	if sessions.has_key(session_id):
		return pdump(True)
	return pdump(False)

def test_binded(session_id):
	session_id=pload(session_id)
	if sessions.has_key(session_id):
		if sessions[session_id].has_key('authenticated'):
			return pdump(sessions[session_id]['authenticated'])
	return pdump(False)

def bind(session_id,encrypted_passwd):
	session_id=pload(session_id)
	encrypted_passwd=pload(encrypted_passwd)

	if not sessions.has_key(session_id):
		return pdump(False)
	if not sessions[session_id].has_key('nonce'):
		return pdump(False)
	
	um = userman.UserManager()
	plain = p2_decrypt(encrypted_passwd,sessions[session_id].pop('nonce'))
	if plain==conf.get('SOAP_SERVICE','passwd'):
		sessions[session_id]['authenticated'] = True
		return pdump(True)
	sessions[session_id]['authenticated'] = False
	return pdump(False)

def get_id():
	new_id = md5.new(str(time.time())*random.randint(0,100000)).hexdigest()
	sessions[new_id] = {'authenticated': False}
	return pdump(new_id)

def challenge_response_key(session_id):
	session_id=pload(session_id)
	if not sessions.has_key(session_id):
		return pdump(None)
	if not sessions[session_id].has_key('challenge_count'):
		sessions[session_id]['challenge_count']=0
	if sessions[session_id]['challenge_count'] >= 3:
		return pdump(False)
	nonce = md5.new(str(str(time.time())*random.randint(0,100000))+session_id).hexdigest()
	sessions[session_id]['nonce'] = nonce
	sessions[session_id]['challenge_count']+=1
	return pdump(nonce)


# The real functionality starts here
def domain_name(session_id):
	if not session_valid(pload(session_id)):
		return pdump(False)
	domain_name = conf.get('DOMAIN','domain_name')
	return pdump(domain_name)

# Users
def list_users(session_id,usertype):
	if not session_valid(pload(session_id)):
		return pdump(False)
	usertype = pload(usertype)
	um = userman.UserManager()
	return pdump(um.list_users(usertype))

def user_exists(session_id,uid):
	"""
	Do a quick lookup in the mainserver LDAP to see if a 
	certain uid exists.
	"""
	if not session_valid(pload(session_id)):
		return pdump(False)
	uid=pload(uid)
	um = userman.UserManager()
	return pdump(um.user_exists(uid))

def createuser(session_id,uid,givenname,familyname,passwd,usertype):
	if not session_valid(pload(session_id)):
		return pdump(False)
	uid=pload(uid)
	givenname=pload(givenname)
	familyname=pload(familyname)
	passwd=pload(passwd)
	usertype=pload(usertype)
	
	um = userman.UserManager()
	return pdump(um.createuser(uid,givenname,familyname,passwd,usertype))

def removeuser(session_id,uid,backup_home,remove_home):
	if not session_valid(pload(session_id)):
		return pdump(False)
	uid=pload(uid)
	backup_home=pload(backup_home)
	remove_home=pload(remove_home)
	
	um = userman.UserManager()
	return pdump(um.deluser(uid,backup_home,remove_home))

# Groups
def list_groups(session_id,grouptype):
	if not session_valid(pload(session_id)):
		return pdump(False)
	usertype = pload(usertype)
	gm = grpman.GroupManager()
	return pdump(gm.list_groups(usertype))

def group_exists(session_id,groupname):
	"""
	Do a quick lookup in the mainserver LDAP to see if a 
	certain groupname exists.
	"""
	if not session_valid(pload(session_id)):
		return pdump(False)
	uid=pload(groupname)
	gm = grpman.GroupManager()
	return pdump(gm.group_exists(groupname))

def creategroup(session_id,uid,givenname,familyname,passwd,usertype):
	if not session_valid(pload(session_id)):
		return pdump(False)
	uid=pload(uid)
	givenname=pload(givenname)
	familyname=pload(familyname)
	passwd=pload(passwd)
	usertype=pload(usertype)
	
	um = userman.UserManager()
	return pdump(um.createuser(uid,givenname,familyname,passwd,usertype))

def removeuser(session_id,uid,backup_home,remove_home):
	if not session_valid(pload(session_id)):
		return pdump(False)
	uid=pload(uid)
	backup_home=pload(backup_home)
	remove_home=pload(remove_home)
	
	um = userman.UserManager()
	return pdump(um.deluser(uid,backup_home,remove_home))


class MyServer(SOAPpy.SOAPServer):
    def __init__(self,addr=('localhost', 8000), ssl_context=None):
        SOAPpy.SOAPServer.__init__(self,addr,ssl_context=ssl_context)

    def verify_request(self,request,clientaddr):
        #print request.get_session().as_text()
        #print clientaddr
        return True

def startserver():
	l4s_basepath = os.path.split(inspect.getsourcefile(lin4schools))[0]
	certfile = os.path.join(l4s_basepath,'cert',"l4s_cert_%s.pem" % conf.get("DOMAIN","domain_name"))
	keyfile = os.path.join(l4s_basepath,'cert',"l4s_key_%s.pem" % conf.get("DOMAIN","domain_name"))
	netif = conf.get("SOAP_SERVICE","interface")
	addr = get_ip_address(netif)
	if not addr:
		print "Interface %s has not been configured. No SOAP service started" % netif
		exit(0)
	ssl_context = SSL.Context()
	ssl_context.load_cert(certfile,keyfile=keyfile)
	server = MyServer((addr, 8443),ssl_context = ssl_context)
	print "Starting SOAP service on interface %s (%s)" % (netif,addr)
	
	# Securitty
	server.registerFunction(get_id)
	server.registerFunction(challenge_response_key)
	server.registerFunction(bind)
	server.registerFunction(test_session_id)
	server.registerFunction(test_binded)

	# Real functionality
	server.registerFunction(domain_name)
	server.registerFunction(user_exists)
	server.registerFunction(list_users)
	server.registerFunction(createuser)
	server.registerFunction(removeuser)
	
	# Test
	server.registerFunction(test)

	server.serve_forever()

