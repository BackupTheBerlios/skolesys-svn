'''
This file is part of the SkoleSYS libraries
Copyright (C) 2007 Jakob Simon-Gaarde <info at skolesys.dk>

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Library General Public
License version 2 as published by the Free Software Foundation.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Library General Public License for more details.

You should have received a copy of the GNU Library General Public License
along with this library; see the file COPYING.LIB.  If not, write to
the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
Boston, MA 02110-1301, USA.
'''
import re
from skolesys.lib.hostmanager import *
import skolesys.definitions.hostdef as hostdef
from skolesys.lib.conf import *
from Cheetah.Template import Template
from math import ceil

class InfoCollection:
	"""
	Collect info from LDAP, skolesys.conf e.t.c. to be used
	by the configuration template system.
	"""
	def __init__(self,hwaddr=None):
		self.data = {}
		self.hwaddr = hostdef.check_hwaddr(hwaddr)
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
		Fetch the info collection data container
		"""
		return self.data



# Test
if __name__=='__main__':
	ic = InfoCollection()
	t = Template(file='dhcpd.conf', searchList=[ic.data])
	f=open('dhcpd_out.conf','w')
	f.write(t.__str__())
	f.close()
	
