import SOAPpy
import pickle
from p2 import p2_encrypt
from marshall import pdump,pload
import sys,httplib
from netinfo import ip2hwaddr, ip2if
import socket,os,re

class SkoleSYS_Client:
	def __init__(self,host,port=None,log=sys.stderr):
		self.logfile = log
		if port:
			url = "%s:%d/" % (host,port)
		else:
			url = host
		self.server = SOAPpy.SOAPProxy(url)
		self._get_id()
		
		# Check the DISPLAY variable to see if this is a thin client
		self.tc_displayhost = None
		disp = os.getenv('DISPLAY')
		if disp:
			c = re.compile('^(\S+):\S+')
			m=c.match(disp)
			if m:
				print 'The display host is set to: "%s"' % m.groups()[0]
				self.tc_displayhost = m.groups()[0]
				self.tc_ip = None
				self.tc_hwaddr = None
				try:
					self.tc_ip = socket.gethostbyname(self.tc_displayhost)
				except socket.gaierror, e:
					print 'the display\'s "hostname" %s can not be resolved' % self.tc_displayhost
				
				display_host_if = ip2if(self.tc_ip)
				if display_host_if:
					print 'OK, the display host maps to the local interface "%s", so we are assuming that this is not a remote session' % display_host_if
				
				if not display_host_if and self.tc_ip != None:
					self.tc_hwaddr = ip2hwaddr(self.tc_ip)
					if self.tc_hwaddr == None:
						print "could not resolve the hwaddr of ip %s" % self.tc_ip
				

		
		# Fetch the client hwaddr
		addr = SOAPpy.SOAPAddress(url)
		
		real_addr = addr.host
		if addr.proto == 'https':
			r = httplib.HTTPS(real_addr)
		else:
			r = httplib.HTTP(real_addr)
		r._conn.connect()
		self.local_ip = r._conn.sock._sock.getsockname()[0]
		self.local_if = ip2if(self.local_ip)
		self.local_hwaddr = ip2hwaddr(self.local_ip)
		r._conn.close()
		self.remotedisplay = False
		
		if (self.tc_displayhost and self.tc_hwaddr and not ip2if(self.tc_ip)):
			print "Remote login: [%s]" % self.tc_hwaddr
			self.hwaddr = self.tc_hwaddr
			self.remotedisplay = True
		else:
			print "Local login: %s [%s]" % (self.local_if,self.local_hwaddr)
			self.hwaddr = self.local_hwaddr

		import skolesys.tools.sysinfo as sysinfo
		self.dist_codename = sysinfo.get_dist_codename()

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

	def list_users(self,usertype_id=None,uid=None):
		"""
		Get a list of LDAP posixusers located on the mainserver. Optionally the
		list can be filtered by the user type.
		"""
		return pload(self.server.list_users(pdump(self.session_id),pdump(usertype_id),pdump(uid)))

	def list_usergroups(self,uid):
		"""
		Get a list of LDAP posixgroups located on the mainserver for a certain user "uid".
		"""
		return pload(self.server.list_usergroups(pdump(self.session_id),pdump(uid)))

	def user_exists(self,uid):
		"""
		Do a quick lookup in the mainserver LDAP to see if a 
		certain uid exists.
		"""
		return pload(self.server.user_exists(pdump(self.session_id),pdump(uid)))
	
	
	def createuser(self,uid,givenname,familyname,passwd,usertype_id,primarygroup,firstyear):
		return pload(self.server.createuser(pdump(self.session_id),pdump(uid),pdump(givenname),\
			pdump(familyname),pdump(passwd),pdump(usertype_id),pdump(primarygroup),pdump(firstyear)))

	def changeuser(self,uid,givenname=None,familyname=None,passwd=None,primarygroup=None,firstyear=None):
		return pload(self.server.changeuser(pdump(self.session_id),pdump(uid),pdump(givenname),\
			pdump(familyname),pdump(passwd),pdump(primarygroup),pdump(firstyear)))
				
	def removeuser(self,uid,backup_home=False,remove_home=False):
		return pload(self.server.removeuser(pdump(self.session_id),pdump(uid),pdump(backup_home),pdump(remove_home)))

	def groupadd(self,uid,groupname):
		"""
		Add a group membership to between "uid" and "groupname"
		"""
		return pload(self.server.groupadd(pdump(self.session_id),pdump(uid),pdump(groupname)))
		
	def groupdel(self,uid,groupname):
		"""
		Remove a group membership to between "uid" and "groupname"
		"""
		return pload(self.server.groupdel(pdump(self.session_id),pdump(uid),pdump(groupname)))

	def list_groups(self,usertype_id=None,groupname=None):
		"""
		Get a list of LDAP posixgroups located on the mainserver. Optionally the
		list can be filtered by the user type.
		"""
		return pload(self.server.list_groups(pdump(self.session_id),pdump(usertype_id),pdump(groupname)))

	def list_members(self,groupname):
		"""
		Get a member list of LDAP posixusers located on the mainserver for a certain group "groupname".
		"""
		return pload(self.server.list_members(pdump(self.session_id),pdump(groupname)))

	def group_exists(self,groupname):
		"""
		Do a quick lookup in the mainserver LDAP to see if a 
		certain uid exists.
		"""
		return pload(self.server.group_exists(pdump(self.session_id),pdump(groupname)))

	def creategroup(self,groupname,displayed_name,usertype_id,description):
		"""
		1. Create a new posixgroup in the mainserver LDAP DB.
		2. Create a group home directory
		"""
		return pload(self.server.creategroup(pdump(self.session_id),pdump(groupname),pdump(displayed_name),pdump(usertype_id),pdump(description)))

	def changegroup(self,groupname,description):
		"""
		1. Create a new posixgroup in the mainserver LDAP DB.
		2. Create a group home directory
		"""
		return pload(self.server.changegroup(pdump(self.session_id),pdump(groupname),pdump(description)))
	
	def removegroup(self,groupname,backup_home=False,remove_home=False):
		"""
		1. Delete the posixgroup "groupname" from the mainserver LDAP db
		2. Maybe backup the group home directory
		3. Maybe remove the group home directory
		"""
		print groupname,backup_home,remove_home
		return pload(self.server.removegroup(pdump(self.session_id),pdump(groupname),pdump(backup_home),pdump(remove_home)))
	
	def attach_groupservice(self,groupname,servicename):
		"""
		Attach a service to a group. Members of the group might be affected by this action.
		If the group is already attached to the service nothing will be done
		"""
		return pload(self.server.attach_groupservice(pdump(self.session_id),pdump(groupname),pdump(servicename)))
		
	def detach_groupservice(self,groupname,servicename):
		"""
		Detach a service to a group. Members of the group might be affected by this action.
		If the group is not attached to the service nothing will be done
		"""
		return pload(self.server.detach_groupservice(pdump(self.session_id),pdump(groupname),pdump(servicename)))
		
	def restart_groupservice(self,groupname,servicename):
		"""
		Restart a service for a group. It is the restart method of the service interface
		that specifies which actions should be taken.
		"""
		return pload(self.server.restart_groupservice(pdump(self.session_id),pdump(groupname),pdump(servicename)))

	def list_groupservices(self,groupname=None):
		"""
		List all available services (groupname=None) or only the ones attached to a particular group.
		"""
		return pload(self.server.list_groupservices(pdump(self.session_id),pdump(groupname)))
		
	def list_groupservice_options_available(self,servicename,groupname='dummy'):
		"""
		Fetch a dictionary describing the options available for a certain group service.
		It can only be used in combination with a groupname since it is legal to have options_available
		change dynamically i.e. as a function of the options already set. F.inst. if an option is "use_pop3"
		the options_available might change by adding options like "use_ssl" and "pop3_server".
		SkoleSYS UI is implemented with this in mind.
		"""
		return pload(self.server.list_groupservice_options_available(pdump(self.session_id),pdump(groupname),pdump(servicename)))


	def get_groupservice_option_values(self,servicename,groupname):
		return pload(self.server.get_groupservice_option_values(pdump(self.session_id),pdump(servicename),pdump(groupname)))

	def set_groupservice_option_value(self,servicename,groupname,variable,value):
		"""
		Set a single option value (Variable/value set). All "normal" data types are supported including
		lists, tuples and dictionaries which are simply stored with through the ::__str__() method.
		"""
		return pload(self.server.set_groupservice_option_value(
			pdump(self.session_id),pdump(groupname),pdump(servicename),
			pdump(variable),pdump(value)))

	def unset_groupservice_option(self,servicename,groupname,variable):
		"""
		Set a single option value (Variable/value set). All "normal" data types are supported including
		lists, tuples and dictionaries which are simply stored with through the ::__str__() method.
		"""
		return pload(self.server.unset_groupservice_option(
			pdump(self.session_id),pdump(groupname),pdump(servicename),pdump(variable)))
	
	def register_host(self,hostname,hosttype_id,hwaddr=None):
		"""
		Register the current displaying host
		"""
		if hwaddr == None:
			hwaddr = self.hwaddr
		
		return pload(self.server.register_host(pdump(self.session_id),pdump(hostname),pdump(hosttype_id),pdump(hwaddr)))
		
		
	def is_registered(self,hostname=None,hwaddr=None):
		"""
		Check if a certain host is registered
		"""
		if hostname:
			return pload(self.server.hostname_exists(pdump(self.session_id),pdump(hostname)))
		
		if hwaddr == None:
			hwaddr = self.hwaddr
			
		return pload(self.server.hwaddr_exists(pdump(self.session_id),pdump(hwaddr)))
	
	
	def hostinfo(self,hostname=None,hwaddr=None):
		"""
		Fetch the registered information of a certain host bu hostname or hwaddr. 
		If no arguments are passed then the current displaying host's information is
		returned.
		"""
		if hostname:
			return pload(self.server.hostinfo_by_hostname(pdump(self.session_id),pdump(hostname)))
		
		if hwaddr == None:
			hwaddr = self.hwaddr
			
		return pload(self.server.hostinfo_by_hwaddr(pdump(self.session_id),pdump(hwaddr)))
		
		
	def listhosts(self,hosttype_id=None):
		"""
		Fetch a list og registered hosts. Hosttype_id can be used to apply a filter.
		"""
		return pload(self.server.listhosts(pdump(self.session_id),pdump(hosttype_id)))
		
		
	def getconf(self,dist_codename=None,hwaddr=None,context=None,context_only=False):
		if self.remotedisplay == True:
			print "Error: Cannot fetch configuration through a remotely logged in session"
			return (0,0)
		if hwaddr == None:
			hwaddr = self.local_hwaddr # Should never fetch another host's (remote display mode) configuration!
		if dist_codename == None:
			dist_codename = self.dist_codename
		return pload(self.server.getconf(pdump(self.session_id),pdump(dist_codename),pdump(hwaddr),pdump(context),pdump(context_only)))
	
	
	# FileManager
	def findfiles(self,username=None,groupname=None,minsize=None,regex=None,order=''):
		return pload(self.server.findfiles(pdump(self.session_id),pdump(username),pdump(groupname),pdump(minsize),pdump(regex),pdump(order)))

	def removefiles(self,rmlist):
		return pload(self.server.removefiles(pdump(self.session_id),pdump(rmlist)))
	
	
	


if __name__=='__main__':
    c=SkoleSYS_Client('https://127.0.0.1',8443)
    print c.bind('secret')
    userdict = c.list_users(4)
    for user in userdict.keys():
        print user
