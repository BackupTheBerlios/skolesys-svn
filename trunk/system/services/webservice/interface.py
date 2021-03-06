# coding=UTF-8

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

import skolesys.services.groupserviceinterface as gsi
from skolesys.lib.conf import conf
import grp
import copy,os
import webservicehelper as wshelper

class ServiceInterface(gsi.GroupServiceInterface):
	global testlist
	
	options = {
		'AccessType': 	{'type': int,  'section': 'APACHE', 'default': 3, 'enum': {'Intranet access':1,'Internet access':2,'Full access':3}},
		'ServerName': 	{'type': str,  'section': 'APACHE'},
		'AuthType': 	{'type': str,  'section': 'APACHE', 'default': 'Off', 'choices': ['Off','Group']},
		'AuthName': 	{'type': str,  'section': 'APACHE', 'default': None}}
		#'mod_php_enabled': 	{'type': bool, 'section': 'APACHE', 'default': False},
		#'mod_python_enabled': 	{'type': bool, 'section': 'APACHE', 'default': False},
		#'bla_enumeration': 	{'type': int,  'section': 'APACHE', 'default': 3, 'enum': {'Mor': 32, 'æøå':1, 'Jens':3, 'Jakob':2}},
		#'bla_number_value': 	{'type': int,  'section': 'APACHE', 'default': 0, 'range': [5,56]},
		#'Svend':		{'type': int,  'section': 'APACHE', 'range': [0,100]}}
	
	def __init__(self,groupname):
		gsi.GroupServiceInterface.__init__(self,"webservice",groupname)
		self.helper = wshelper.WebserviceHelper(groupname,self.resource_location())	
	
	def get_options_available(self):
		return self.options

	def hook_attachservice(self,userlist):
		self.helper.setup_resource_location()
		self.invalidate()
		self.restart()
		print "Hmm. I also need to do something with these users: %s" % ','.join(userlist)
		return 0

	def hook_detachservice(self,userlist):
		self.helper.remove_configuration()
		self.restart()
		home_path = "%s/%s/groups/%s" % (conf.get('DOMAIN','domain_root'),conf.get('DOMAIN','domain_name'),self.groupname)
                if os.path.exists('%s/www' % home_path):
                        os.system('rm %s/www' % home_path)

		print "Users %s might be affected" % ','.join(userlist)

	def hook_groupadd(self,user):
		pass

	def hook_groupdel(self,user):
		pass

	def invalidate(self):
		accesstype_to_name = {1: 'intra', 2: 'inter', 3: 'both', None: 'both'}
		del self.conf_parser
		self.conf_parser = None
		
		res,accesstype = self.get_option("AccessType")
		print accesstype
		accesstype = accesstype_to_name[accesstype]
		res,servername = self.get_option("ServerName")
		res,authtype = self.get_option("AuthType")
		res,authname = self.get_option("AuthName")
		# if servername is set the site should be setup as a virtual host.
		self.helper.write_configuration(accesstype,authtype,authname,servername)
		
	def restart(self):
		self.helper.restart_apache()
