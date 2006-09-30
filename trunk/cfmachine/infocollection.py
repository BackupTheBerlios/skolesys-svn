import re
from skolesys.lib.hostmanager import *
from skolesys.lib.conf import *
from Cheetah.Template import Template

class InfoCollection:
	"""
	Collect info from LDAP, skolesys.conf e.t.c. to be used
	by the configuration template system.
	"""
	def __init__(self):
		self.data = {}
		self.conf_info()
		self.host_info()
		self.user_info()

	def conf_info(self):
		# conf data
		self.data['conf'] = {}
		sections = conf.sections()
		for sec in sections:
			s = sec.lower()
			self.data['conf'][s] = {}
			for var,val in conf.items(sec):
				self.data['conf'][s][var.lower()] = val
		# TODO - There is to be made skolesys.conf sanity checker build into 
		# TODO - skolesys.lib.conf. That way the user can be presented with a 
		# TODO - configuration invalidity like missing mandetory variables:
		
		# Mainserver
		subnet_str = self.data['conf']['domain']['mainserver_subnet']
		res = check_subnet(subnet_str)
		if not res:
			return -1
		subnet,subnetmask = res
		subnetmask_int = 2**int(subnetmask)-1
		subnetmask_address = '%d.%d.%d.%d' % (subnetmask_int&255,(subnetmask_int>>8)&255,(subnetmask_int>>16)&255,(subnetmask_int>>24)&255)
		self.data['conf']['domain']['mainserver_subnet'] = subnet
		self.data['conf']['domain']['mainserver_subnetmask'] = subnetmask_address
		
		# LTSP servers
		subnet_str = self.data['conf']['domain']['ltspserver_subnet']
		res = check_subnet(subnet_str)
		if not res:
			return -2
		subnet,subnetmask = res
		subnetmask_int = 2**int(subnetmask)-1
		subnetmask_address = '%d.%d.%d.%d' % (subnetmask_int&255,(subnetmask_int>>8)&255,(subnetmask_int>>16)&255,(subnetmask_int>>24)&255)
		self.data['conf']['domain']['ltspserver_subnet'] = subnet
		self.data['conf']['domain']['ltspserver_subnetmask'] = subnetmask_address
		

	def host_info(self):
		hm = HostManager()
		hosts_all = hm.list_hosts()
		self.data['hosts'] = {}
		for host in hosts_all:
			nhost = {}
			for k,v in host.items():
				nhost[k] = v[0]
			htyp = nhost['hostType']
			if not self.data['hosts'].has_key(htyp):
				self.data['hosts'][htyp] = []
			self.data['hosts'][htyp] += [nhost]
	
	def user_info(self):
		"""
		TODO - this is ment to be used for users to add there
		TODO - own collection functions. It will be implemented later.
		To add simple static variabled in to the InfoCollection
		concider to create a section in skolesys.conf and put
		the valies there. All variables in skolesys.conf are parsed
		and delivered to the templatesystem (self.conf_info()).
		"""
		pass


# Test
if __name__=='__main__':
	ic = InfoCollection()
	f=open('dhcpd.conf')
	buf = f.read()
	f.close()
	t = Template(buf, searchList=[ic.data])
	f=open('dhcpd_out.conf','w')
	f.write(t.__str__())
	f.close()
	
