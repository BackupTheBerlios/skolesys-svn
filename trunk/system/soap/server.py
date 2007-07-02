#!/usr/bin/python

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

import os
import sys
import inspect
import os.path
import SOAPpy
import md5
import pickle
import skolesys
import skolesys.lib.usermanager as userman
import skolesys.lib.groupmanager as groupman
import skolesys.lib.filemanager as fileman
from skolesys.lib.hostmanager import HostManager
import skolesys.definitions.hostdef as hostdef
from skolesys.cfmachine.configbuilder import ConfigBuilder
from M2Crypto import SSL
from p2 import p2_decrypt
import time
import random
from marshall import pdump,pload
from netinfo import if2ip,ip2hwaddr
import sessionhandler

sessions = None

def print_sessions():
	global sessions
	return pdump(str(sessions.sessions))

def session_valid(session_id):
	global sessions
	if sessions.session_exists(session_id):
		if sessions.has_session_variable(session_id,'authenticated'):
			return sessions.get_session_variable(session_id,'authenticated')[1]
	return False

def test_session_id(session_id):
	"""
	Test if the given session ID is still valid
	"""
	global sessions
	session_id=pload(session_id)
	if sessions.session_exists(session_id):
		return pdump(True)
	return pdump(False)

def test_binded(session_id):
	global sessions
	session_id=pload(session_id)
	if sessions.session_exists(session_id):
		if sessions.has_session_variable(session_id,'authenticated'):
			return pdump(sessions.get_session_variable(session_id,'authenticated')[1])
	return pdump(False)

def bind(session_id,encrypted_passwd):
	global sessions
	session_id=pload(session_id)
	encrypted_passwd=pload(encrypted_passwd)

	if not sessions.session_exists(session_id):
		return pdump(False)
	if not sessions.has_session_variable(session_id,'nonce'):
		return pdump(False)
	
	nonce = sessions.get_session_variable(session_id,'nonce')[1]
	sessions.unset_session_variable(session_id,'nonce')
	plain = p2_decrypt(encrypted_passwd,nonce)
	if plain==conf.get('SOAP_SERVICE','passwd'):
		sessions.set_session_variable(session_id,'authenticated',True)
		return pdump(True)
	sessions.set_session_variable(session_id,'authenticated',False)
	return pdump(False)

def get_id():
	global sessions
	new_id = md5.new(str(time.time())*random.randint(0,100000)).hexdigest()
	if sessions.create_session(new_id):
		sessions.set_session_variable(new_id,'authenticated',False)
	return pdump(new_id)

def challenge_response_key(session_id):
	global sessions
	session_id=pload(session_id)
	if not sessions.session_exists(session_id):
		return pdump(None)
	
	if not sessions.has_session_variable(session_id,'challenge_count'):
		sessions.set_session_variable(session_id,'challenge_count',0)
	challenge_count = sessions.get_session_variable(session_id,'challenge_count')[1]
	if challenge_count >= 3:
		return pdump(False)
	
	nonce = md5.new(str(str(time.time())*random.randint(0,100000))+session_id).hexdigest()
	sessions.set_session_variable(session_id,'nonce',nonce)
	challenge_count+=1
	sessions.set_session_variable(session_id,'challenge_count',challenge_count)
	return pdump(nonce)

def kill_session(session_id):
	global sessions
	session_id=pload(session_id)
	if not sessions.session_exists(session_id):
		return pdump(None)
	sessions.remove_session(session_id)
	return pdump(True)


# The real functionality starts here

def domain_name(session_id):
	if not session_valid(pload(session_id)):
		return pdump(False)
	domain_name = conf.get('DOMAIN','domain_name')
	return pdump(domain_name)

# Users
def list_users(session_id,usertype_id,uid):
	if not session_valid(pload(session_id)):
		return pdump(False)
	usertype_id = pload(usertype_id)
	uid = pload(uid)
	um = userman.UserManager()
	return pdump(um.list_users(usertype_id,uid))

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

def changeuser(session_id,uid,givenname,familyname,passwd,primarygroup,firstyear):
	"""
	Add a new user. firstyear defines the students first year in school.
	"""
	if not session_valid(pload(session_id)):
		return pdump(False)
	uid=pload(uid)
	givenname=pload(givenname)
	familyname=pload(familyname)
	passwd=pload(passwd)
	primarygroup=pload(primarygroup)
	firstyear=pload(firstyear)
	
	um = userman.UserManager()
	return pdump(um.changeuser(uid,givenname,familyname,passwd,primarygroup,firstyear))


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
def list_groups(session_id,usertype_id,groupname):
	if not session_valid(pload(session_id)):
		return pdump(False)
	usertype_id = pload(usertype_id)
	groupname = pload(groupname)
	gm = groupman.GroupManager()
	return pdump(gm.list_groups(usertype_id,groupname))

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

def creategroup(session_id,groupname,displayed_name,usertype_id,description):
	if not session_valid(pload(session_id)):
		return pdump(False)
	groupname=pload(groupname)
	displayed_name=pload(displayed_name)
	usertype_id=pload(usertype_id)
	description=pload(description)
	
	gm = groupman.GroupManager()
	return pdump(gm.creategroup(groupname,displayed_name,usertype_id,description))

def changegroup(session_id,groupname,description):
	if not session_valid(pload(session_id)):
		return pdump(False)
	groupname=pload(groupname)
	description=pload(description)

	gm = groupman.GroupManager()
	return pdump(gm.changegroup(groupname,description))

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

def getconf(session_id,dist_codename,hwaddr,context,context_only):
	dist_codename = pload(dist_codename)
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
	cb = ConfigBuilder(hosttype_id,dist_codename,hwaddr,context,context_only)
	f = open('%s/conf.tgz' % cb.tempdir ,'rb')
	o = f.read()
	f.close()
	
	return pdump([1,o])


def attach_groupservice(session_id,groupname,servicename):
	"""
	Attach group to a group service
	"""
	if not session_valid(pload(session_id)):
		return pdump(False)

	groupname = pload(groupname)
	servicename = pload(servicename)

	gm = groupman.GroupManager()
	return pdump(gm.attach_service(groupname,servicename))


def restart_groupservice(session_id,groupname,servicename):
	"""
	Attach group to a group service
	"""
	if not session_valid(pload(session_id)):
		return pdump(False)

	groupname = pload(groupname)
	servicename = pload(servicename)

	gm = groupman.GroupManager()
	return pdump(gm.restart_service(groupname,servicename))


def detach_groupservice(session_id,groupname,servicename):
	"""
	Detach group from a group service
	"""
	if not session_valid(pload(session_id)):
		return pdump(False)

	groupname = pload(groupname)
	servicename = pload(servicename)

	gm = groupman.GroupManager()
	return pdump(gm.detach_service(groupname,servicename))


def list_groupservices(session_id,groupname):
	"""
	Fetch a simple list of group service names.
	"""
	if not session_valid(pload(session_id)):
		return pdump(False)
	
	groupname = pload(groupname)

	gm = groupman.GroupManager()
	return pdump(gm.list_services(groupname))

def list_groupservice_options_available(session_id,groupname,servicename):
	"""
	Fetch a dictionary describing the options available for a certain group service.
	It can only be used in combination with a groupname since it is legal to have options_available
	change dynamically i.e. as a function of the options already set. F.inst. if an option is "use_pop3"
	the options_available might change by adding options like "use_ssl" and "pop3_server".
	SkoleSYS UI is implemented with this in mind.
	"""
	if not session_valid(pload(session_id)):
		return pdump(False)

	groupname = pload(groupname)
	servicename = pload(servicename)
	
	gm = groupman.GroupManager()
	return pdump(gm.list_service_options_available(servicename,groupname))


def get_groupservice_option_values(session_id,groupname,servicename):
	if not session_valid(pload(session_id)):
		return pdump(False)

	groupname = pload(groupname)
	servicename = pload(servicename)
	
	gm = groupman.GroupManager()
	return pdump(gm.get_service_option_values(groupname,servicename))


def set_groupservice_option_value(session_id,groupname,servicename,variable,value):
	if not session_valid(pload(session_id)):
		return pdump(False)

	groupname = pload(groupname)
	servicename = pload(servicename)
	variable = pload(variable)
	value = pload(value)
	
	gm = groupman.GroupManager()
	return pdump(gm.set_service_option_value(groupname,servicename,variable,value))

def unset_groupservice_option(session_id,groupname,servicename,variable):
	if not session_valid(pload(session_id)):
		return pdump(False)

	groupname = pload(groupname)
	servicename = pload(servicename)
	variable = pload(variable)
	
	gm = groupman.GroupManager()
	return pdump(gm.unset_service_option(groupname,servicename,variable))


def findfiles(session_id,username,groupname,minsize,regex,order):
	if not session_valid(pload(session_id)):
		return pdump(False)

	username = pload(username)
	groupname = pload(groupname)
	minsize = pload(minsize)
	regex = pload(regex)
	order = pload(order)
	
	fm = fileman.FileManager()
	return pdump(fm.find(user=username,group=groupname,minsize=minsize,regex=regex,order=order))

def removefiles(session_id,files):
	if not session_valid(pload(session_id)):
		return pdump(False)

	files = pload(files)
	fm = fileman.FileManager()
	return pdump(fm.removefiles(files))


class MyServer(SOAPpy.SOAPServer):
    def __init__(self,addr=('localhost', 8000), ssl_context=None):
        SOAPpy.SOAPServer.__init__(self,addr,ssl_context=ssl_context)

    def verify_request(self,request,clientaddr):
        #print request.get_session().as_text()
        #print ip2hwaddr(clientaddr[0])
        return True



def startserver():
	global sessions
	# Check root privilegdes
	if not os.getuid()==0:
		print "This command requires root priviledges"
		sys.exit(1)
	
	from skolesys.lib.conf import conf
	
	session_timeout = int(conf.get("SOAP_SERVICE","session_timeout"))
	sessions = sessionhandler.SessionHandler(session_timeout)
	
	certfile = None
	keyfile = None
	
	# Old style filenames before SkoleSYS ver 0.8.1
	oldstyle_cert_filename = os.path.join('/etc/skolesys/cert',"cert_%s.pem" % conf.get("DOMAIN","domain_name"))
	if os.path.exists(oldstyle_cert_filename):
		certfile = oldstyle_cert_filename
	oldstyle_key_filename = os.path.join('/etc/skolesys/cert',"key_%s.pem" % conf.get("DOMAIN","domain_name"))
	if os.path.exists(oldstyle_key_filename):
		keyfile = oldstyle_key_filename
	
	# New style filenames from SkoleSYS ver 0.8.1 and after
	newstyle_cert_filename = os.path.join('/etc/skolesys/cert',"%s.cert" % conf.get("DOMAIN","domain_name"))
	if os.path.exists(newstyle_cert_filename):
		certfile = newstyle_cert_filename
	newstyle_key_filename = os.path.join('/etc/skolesys/cert',"%s.key" % conf.get("DOMAIN","domain_name"))
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
	server.registerFunction(print_sessions)
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
	server.registerFunction(changeuser)
	server.registerFunction(removeuser)
	server.registerFunction(groupadd)
	server.registerFunction(groupdel)
	
	# Group Management
	server.registerFunction(group_exists)
	server.registerFunction(list_groups)
	server.registerFunction(list_members)
	server.registerFunction(creategroup)
	server.registerFunction(changegroup)
	server.registerFunction(removegroup)
	
	# Group Services
	server.registerFunction(attach_groupservice)
	server.registerFunction(detach_groupservice)
	server.registerFunction(restart_groupservice)
	server.registerFunction(list_groupservices)
	server.registerFunction(list_groupservice_options_available)
	server.registerFunction(get_groupservice_option_values)
	server.registerFunction(set_groupservice_option_value)
	server.registerFunction(unset_groupservice_option)
	
	# Host Management
	server.registerFunction(register_host)
	server.registerFunction(hostname_exists)
	server.registerFunction(hwaddr_exists)
	server.registerFunction(hostinfo_by_hwaddr)
	server.registerFunction(hostinfo_by_hostname)
	server.registerFunction(listhosts)
	server.registerFunction(getconf)
	
	# File Management
	server.registerFunction(findfiles)
	server.registerFunction(removefiles)

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
	# Check root privilegdes
	if not os.getuid()==0:
		print "This command requires root priviledges"
		sys.exit(0)
	from skolesys.lib.conf import conf
	
	startserver()
	sys.exit(0)
