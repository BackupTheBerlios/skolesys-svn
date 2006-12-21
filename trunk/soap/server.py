#!/usr/bin/python

# Check root privilegdes
import os
import sys
if not os.getuid()==0:
	print "This command requires root priviledges"
	sys.exit(0)

import inspect
import os.path
import SOAPpy
import md5
import pickle
import skolesys
import skolesys.lib.usermanager as userman
import skolesys.lib.groupmanager as groupman
from skolesys.lib.conf import conf
from skolesys.lib.hostmanager import HostManager
import skolesys.definitions.hostdef as hostdef
from skolesys.cfmachine.configbuilder import ConfigBuilder
from M2Crypto import SSL
from p2 import p2_decrypt
import time
import random
from marshall import pdump,pload
from netinfo import if2ip,ip2hwaddr

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
def list_users(session_id,usertype_id):
	if not session_valid(pload(session_id)):
		return pdump(False)
	usertype_id = pload(usertype_id)
	um = userman.UserManager()
	return pdump(um.list_users(usertype_id))

def list_usergroups(session_id,uid):
	"""
	List groups of a certain user "uid"
	"""
	if not session_valid(pload(session_id)):
		return pdump(False)
	uid = pload(uid)
	um = userman.UserManager()
	return pdump(um.list_usergroups(uid))

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

def createuser(session_id,uid,givenname,familyname,passwd,usertype_id,primarygroup,firstyear):
	"""
	Add a new user. firstyear defines the students first year in school.
	"""
	if not session_valid(pload(session_id)):
		return pdump(False)
	uid=pload(uid)
	givenname=pload(givenname)
	familyname=pload(familyname)
	passwd=pload(passwd)
	usertype_id=pload(usertype_id)
	primarygroup=pload(primarygroup)
	firstyear=pload(firstyear)
	
	um = userman.UserManager()
	return pdump(um.createuser(uid,givenname,familyname,passwd,usertype_id,primarygroup,firstyear))

def removeuser(session_id,uid,backup_home,remove_home):
	if not session_valid(pload(session_id)):
		return pdump(False)
	uid=pload(uid)
	backup_home=pload(backup_home)
	remove_home=pload(remove_home)
	
	um = userman.UserManager()
	return pdump(um.deluser(uid,backup_home,remove_home))

def groupadd(session_id,uid,groupname):
	if not session_valid(pload(session_id)):
		return pdump(False)
	uid=pload(uid)
	groupname=pload(groupname)

	um = userman.UserManager()
	return pdump(um.groupadd(uid,groupname))

def groupdel(session_id,uid,groupname):
	if not session_valid(pload(session_id)):
		return pdump(False)
	uid=pload(uid)
	groupname=pload(groupname)

	um = userman.UserManager()
	return pdump(um.groupdel(uid,groupname))

# Groups
def list_groups(session_id,usertype_id):
	if not session_valid(pload(session_id)):
		return pdump(False)
	usertype_id = pload(usertype_id)
	gm = groupman.GroupManager()
	return pdump(gm.list_groups(usertype_id))

def list_members(session_id,groupname):
	"""
	List members of a certain group "groupname"
	"""
	if not session_valid(pload(session_id)):
		return pdump(False)
	groupname = pload(groupname)
	gm = groupman.GroupManager()
	return pdump(gm.list_members(groupname))

def group_exists(session_id,groupname):
	"""
	Do a quick lookup in the mainserver LDAP to see if a 
	certain groupname exists.
	"""
	if not session_valid(pload(session_id)):
		return pdump(False)
	groupname=pload(groupname)
	gm = groupman.GroupManager()
	return pdump(gm.group_exists(groupname))

def creategroup(session_id,groupname,usertype_id,description):
	if not session_valid(pload(session_id)):
		return pdump(False)
	groupname=pload(groupname)
	usertype_id=pload(usertype_id)
	description=pload(description)
	
	gm = groupman.GroupManager()
	return pdump(gm.creategroup(groupname,usertype_id,description))

def removegroup(session_id,groupname,backup_home,remove_home):
	if not session_valid(pload(session_id)):
		return pdump(False)
	groupname=pload(groupname)
	backup_home=pload(backup_home)
	remove_home=pload(remove_home)
	
	gm = groupman.GroupManager()
	return pdump(gm.removegroup(groupname,backup_home,remove_home))

def register_host(session_id,hostname,hosttype_id,hwaddr):
	if not session_valid(pload(session_id)):
		return pdump(False)

	hostname = pload(hostname)
	hosttype_id = pload(hosttype_id)
	hwaddr = pload(hwaddr)

	hm = HostManager()
	return pdump(hm.register_host(hwaddr,hostname,hosttype_id))

def hostname_exists(session_id,hostname):
	"""
	Check if a certain hostname is already registered
	"""
	if not session_valid(pload(session_id)):
		return pdump(False)

	hostname = pload(hostname)

	hm = HostManager()
	return pdump(hm.host_exists(hostname=hostname))

def hwaddr_exists(session_id,hwaddr):
	"""
	Check if a certain hwaddr (mac-address) is already registered
	"""
	if not session_valid(pload(session_id)):
		return pdump(False)

	hwaddr = pload(hwaddr)

	hm = HostManager()
	return pdump(hm.host_exists(hwaddr=hwaddr))

def hostinfo_by_hwaddr(session_id,hwaddr):
	"""
	Fetch the registration info of a certain host by hwaddr
	"""
	if not session_valid(pload(session_id)):
		return pdump(False)

	hwaddr = pload(hwaddr)

	hm = HostManager()
	return pdump(hm.host_info(hwaddr=hwaddr))

def hostinfo_by_hostname(session_id,hostname):
	"""
	Fetch the registration info of a certain host by hwaddr
	"""
	if not session_valid(pload(session_id)):
		return pdump(False)

	hostname = pload(hostname)

	hm = HostManager()
	return pdump(hm.host_info(hostname=hostname))

def listhosts(session_id,hosttype_id):
	"""
	Fetch a list og registered hosts
	"""
	if not session_valid(pload(session_id)):
		return pdump(False)

	hosttype_id = pload(hosttype_id)

	hm = HostManager()
	return pdump(hm.list_hosts(hosttype_id))

def getconf(session_id,hwaddr,context,context_only):
	context = pload(context)
	context_only = pload(context_only)
	
	if context == 'update-hosts' and context_only:
		pass
	elif not session_valid(pload(session_id)):
		return pdump(False)
	
	hwaddr = pload(hwaddr)
	hm = HostManager()
	hinfo = hm.host_info(hwaddr)
	if not hinfo:
		return pdump([-1,'']) # Only registered hosts can ask for configurations
	
	hosttype_id = hostdef.hosttype_as_text(hinfo['hostType'][0])
	if not hosttype_id:
		return pdump([-2,'']) # The host is registered with an invalid host type id
	
	print "Configuration requested by host: %s" % hwaddr
	cb = ConfigBuilder(hosttype_id,hwaddr,context,context_only)
	f = open('%s/conf.tgz' % cb.tempdir ,'rb')
	o = f.read()
	f.close()
	
	return pdump([1,o])

class MyServer(SOAPpy.SOAPServer):
    def __init__(self,addr=('localhost', 8000), ssl_context=None):
        SOAPpy.SOAPServer.__init__(self,addr,ssl_context=ssl_context)

    def verify_request(self,request,clientaddr):
        #print request.get_session().as_text()
        #print ip2hwaddr(clientaddr[0])
        return True



def startserver():
	# Check root privilegdes
	if not os.getuid()==0:
		print "This command requires root priviledges"
        	sys.exit(1)
	
	skolesys_basepath = os.path.split(inspect.getsourcefile(skolesys))[0]
	
	certfile = None
	keyfile = None
	
	# Old style filenames before SkoleSYS ver 0.8.1
	oldstyle_cert_filename = os.path.join(skolesys_basepath,'cert',"cert_%s.pem" % conf.get("DOMAIN","domain_name"))
	if os.path.exists(oldstyle_cert_filename):
		certfile = oldstyle_cert_filename
	oldstyle_key_filename = os.path.join(skolesys_basepath,'cert',"key_%s.pem" % conf.get("DOMAIN","domain_name"))
	if os.path.exists(oldstyle_key_filename):
		keyfile = oldstyle_key_filename
	
	# New style filenames from SkoleSYS ver 0.8.1 and after
	newstyle_cert_filename = os.path.join(skolesys_basepath,'cert',"%s.cert" % conf.get("DOMAIN","domain_name"))
	if os.path.exists(newstyle_cert_filename):
		certfile = newstyle_cert_filename
	newstyle_key_filename = os.path.join(skolesys_basepath,'cert',"%s.key" % conf.get("DOMAIN","domain_name"))
	if os.path.exists(newstyle_key_filename):
		keyfile = newstyle_key_filename
		
	if certfile == None or keyfile == None:
		print "Missing a certificate file"
		print "cert-file shold be: %s ot %s" % (oldstyle_cert_filename,newstyle_cert_filename)
		print "key-file shold be: %s ot %s" % (oldstyle_key_filename,newstyle_key_filename)
		sys.exit(1)
	
	netif = conf.get("SOAP_SERVICE","interface")
	addr = if2ip(netif)
	if not addr:
		print "Interface %s has not been configured. No SOAP service started" % netif
		sys.exit(0)
	ssl_context = SSL.Context()
	ssl_context.load_cert(certfile,keyfile=keyfile)
	server = MyServer((addr, 8443),ssl_context = ssl_context)
	print "Starting SOAP service on interface %s (%s)" % (netif,addr)
	
	# Security
	server.registerFunction(get_id)
	server.registerFunction(challenge_response_key)
	server.registerFunction(bind)
	server.registerFunction(test_session_id)
	server.registerFunction(test_binded)

	# Real functionality
	# ------------------
	# User Management
	server.registerFunction(domain_name)
	server.registerFunction(user_exists)
	server.registerFunction(list_users)
	server.registerFunction(list_usergroups)
	server.registerFunction(createuser)
	server.registerFunction(removeuser)
	server.registerFunction(groupadd)
	server.registerFunction(groupdel)
	
	# Group Management
	server.registerFunction(group_exists)
	server.registerFunction(list_groups)
	server.registerFunction(list_members)
	server.registerFunction(creategroup)
	server.registerFunction(removegroup)
	
	# Host Management
	server.registerFunction(register_host)
	server.registerFunction(hostname_exists)
	server.registerFunction(hwaddr_exists)
	server.registerFunction(hostinfo_by_hwaddr)
	server.registerFunction(hostinfo_by_hostname)
	server.registerFunction(listhosts)
	server.registerFunction(getconf)

	if os.fork()==0:
		os.setsid()
		sys.stdout=open("/dev/null", 'w')
		sys.stdin=open("/dev/null", 'r')
		while 1:
			try:
				server.serve_forever()
			except:
				print "SOAP Service malfunctioned - Reenaging..."


if __name__ == '__main__':
	startserver()
	sys.exit(0)
