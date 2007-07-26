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

"""
class InfoCollection
--------------------
InfoCollection takes all information from skolesys.conf and host
information from LDAP and places it into a nicely structured dictionary.
"""

__author__ = "Jakob Simon-Gaarde <jakob@skolesys.dk>"

import re
from skolesys.lib.hostmanager import *
import skolesys.definitions.hostdef as hostdef
from Cheetah.Template import Template
from math import ceil

class InfoCollection:
	"""
	Collect info from LDAP, skolesys.conf etc. InfoCollector is
	build to supply data for cheetah which is the template engine
	cfmachine uses, but can just as well be used for other purposes
	than configuration.
	
	Usage example: (root priviledge is required)
	
	>>> import skolesys.cfmachine.infocollection as ic
	>>> ic_inst = ic.InfoCollection('00:0c:29:d1:74:64')
	>>> conf = ic_inst.get_collection()
	>>> import pprint
	>>> pprint.pprint(conf)
	{'conf': {'cfmachine': {'package_group': 'testing',
				'template_basedir': '/etc/skolesys'},
		'domain': {'domain_name': 'denskaegge.dk',
			'domain_root': '/skolesys',
			'gid_start': '5000',
			'homes_host': 'mainserver.localnet',
			'local_domain_name': 'localnet',
			'ltspclient_iprange': '192.168.10.1 192.168.19.254',
			'ltspserver_dynamic_iprange': '192.168.1.1 192.168.1.254',
			'ltspserver_ip': '192.168.0.1',
			'ltspserver_iprange': '10.1.0.50 10.1.0.254',
			'ltspserver_subnet': '192.168.0.0',
			'ltspserver_subnet_short': '192.168',
			'ltspserver_subnetmask': '255.255.0.0',
			'mainserver_domain_name': 'mainserver.localnet',
			'mainserver_dynamic_iprange': '10.1.50.1 10.1.60.254',
			'mainserver_hostname': 'mainserver',
			'mainserver_ip': '10.1.0.1',
			'mainserver_subnet': '10.1.0.0',
			'mainserver_subnet_short': '10.1',
			'mainserver_subnetmask': '255.255.0.0',
			'uid_start': '5000',
			'workstation_iprange': '10.1.2.1 10.1.9.254'},
		'ldapserver': {'admin': 'cn=admin,dc=denskaegge,dc=skolesys,dc=org',
				'basedn': 'dc=denskaegge,dc=skolesys,dc=org',
				'groups_ou': 'ou=Groups',
				'host': 'mainserver.localnet',
				'hosts_ou': 'ou=Hosts',
				'logins_ou': 'ou=Logins',
				'others_ou': 'ou=Others',
				'parents_ou': 'ou=Parents',
				'passwd': 'bdnprrfe',
				'primary_ou': 'ou=Primary',
				'samba_ou': 'ou=Samba',
				'service_ou': 'ou=Service',
				'smb_groups_ou': 'ou=Groups',
				'smb_machines_ou': 'ou=Computers',
				'smb_users_ou': 'ou=Users',
				'students_ou': 'ou=Students',
				'system_ou': 'ou=System',
				'teachers_ou': 'ou=Teachers'},
		'options': {'default_lang': 'da'},
		'soap_service': {'passwd': 'bdnprrfe', 'interface': 'eth2'},
		'terminal_service': {'freenx': '10.1.0.50'}},
	'hosts': {'ltspserver': [{'cn': 'ltsp1',
				'hostName': 'ltsp1',
				'hostType': 'ltspserver',
				'ipHostNumber': '10.1.0.50',
	"""
	def __init__(self,hwaddr=None):
		"""
		hwaddr	The registered MAC of a host
		
		The constructor calls all the info collecting methods
		(conf_info(), host_info(), user_info())
		"""
		self.data = {}
		self.hwaddr = hostdef.check_hwaddr(hwaddr)
		self.conf_info()
		self.host_info()
		self.user_info()

	def conf_info(self):
		"""
		Read skolesys.conf and populate the member info dictionary. Many of
		the conf values are elabourated before they are stored in the dictionary.
		ie. subnets are registered with the following format in skolesys.conf:
			ltspserver_subnet = 192.168.0.0/16
		but this method expands that information to:
			ltspserver_subnet	192.168.0.0
			ltspserver_subnet_short	192.168
			ltspserver_subnetmask	255.255.0.0
		This kind of post elabouration is nessecary so cheetah can reach the right
		data when needed.
		"""
		from skolesys.lib.conf import conf
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
		res = hostdef.check_subnet(subnet_str)
		if not res:
			return -1
		subnet,subnetmask = res
		subnetmask_int = (2**32-1) - (2**(32-int(subnetmask))-1)
		subnet_int = hostdef.iptoint(subnet)
		subnetmask_address = '%d.%d.%d.%d' % ((subnetmask_int>>24)&255,(subnetmask_int>>16)&255,(subnetmask_int>>8)&255,subnetmask_int&255)
		self.data['conf']['domain']['mainserver_subnet'] = subnet
		self.data['conf']['domain']['mainserver_subnetmask'] = subnetmask_address
		subnet_short = ()
		bit_shifter = 24
		for ip_part in xrange(int(ceil(float(subnetmask)/8))):
			subnet_short += (str((subnet_int>>bit_shifter) & ((subnetmask_int>>bit_shifter) & 255)),)
			bit_shifter -= 8
		self.data['conf']['domain']['mainserver_subnet_short'] = '.'.join(subnet_short)
		
		# LTSP servers
		subnet_str = self.data['conf']['domain']['ltspserver_subnet']
		res = hostdef.check_subnet(subnet_str)
		if not res:
			return -2
		subnet,subnetmask = res
		subnetmask_int = (2**32-1) - (2**(32-int(subnetmask))-1)
		subnet_int = hostdef.iptoint(subnet)
		subnetmask_address = '%d.%d.%d.%d' % ((subnetmask_int>>24)&255,(subnetmask_int>>16)&255,(subnetmask_int>>8)&255,subnetmask_int&255)
		self.data['conf']['domain']['ltspserver_subnet'] = subnet
		self.data['conf']['domain']['ltspserver_subnetmask'] = subnetmask_address
		subnet_short = ()
		bit_shifter = 24
		for ip_part in xrange(int(ceil(float(subnetmask)/8))):
			subnet_short += (str((subnet_int>>bit_shifter) & ((subnetmask_int>>bit_shifter) & 255)),)
			bit_shifter -= 8
		self.data['conf']['domain']['ltspserver_subnet_short'] = '.'.join(subnet_short)
		

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
			if self.hwaddr and self.hwaddr.lower() == nhost['macAddress'].lower():
				self.data['reciever'] = nhost

	
	def user_info(self):
		"""
		TODO - this is ment to be used for users to add there
		TODO - own collection functions. It will be implemented later.
		To add simple static variabled in to the InfoCollection
		concider to create a section in skolesys.conf and put
		the valius there. All variables in skolesys.conf are parsed
		and delivered to the templatesystem (self.conf_info()).
		"""
		pass

	def get_collection(self):
		"""
		Fetch the info collection data dictionary
		"""
		return self.data



# Test
if __name__=='__main__':
	ic = InfoCollection()
	t = Template(file='dhcpd.conf', searchList=[ic.data])
	f=open('dhcpd_out.conf','w')
	f.write(t.__str__())
	f.close()
	
