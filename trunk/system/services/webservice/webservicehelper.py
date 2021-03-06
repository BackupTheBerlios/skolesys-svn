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
from skolesys.lib.conf import conf

auth_pam_group = """
		AuthPAM_Enabled on
		AuthType Basic
		AuthName "<auth_name>"
		require group "<groupname>"
	"""

directory = """
        Alias /<groupname> /skolesys/<domain_name>/services/webservice/<groupname>/data/

        <Directory /skolesys/<domain_name>/services/webservice/<groupname>/data/>
                Options Indexes FollowSymLinks MultiViews
                AllowOverride None
                Order allow,deny
                allow from all
		<auth>
        </Directory>
	"""

class WebserviceHelper:
	def __init__(self,groupname,resource_location):
		self.groupname = groupname
		self.resloc = resource_location

	def remove_configuration(self):
		# Maybe clear directories
		if os.path.exists('/etc/skolesys/www/directories/%s/%s' % ('both',self.groupname)):
			os.remove('/etc/skolesys/www/directories/%s/%s' % ('both',self.groupname))
			
		if os.path.exists('/etc/skolesys/www/directories/%s/%s' % ('intra',self.groupname)):
			os.remove('/etc/skolesys/www/directories/%s/%s' % ('intra',self.groupname))
			
		if os.path.exists('/etc/skolesys/www/directories/%s/%s' % ('inter',self.groupname)):
			os.remove('/etc/skolesys/www/directories/%s/%s' % ('inter',self.groupname))

		# Maybe clear virtual host
		if os.path.exists('/etc/skolesys/www/vhosts/%s' % (self.groupname)):
			os.remove('/etc/skolesys/www/vhosts/%s' % (self.groupname))


	def write_configuration(self,access_type,auth_type=None,auth_name=None,servername=None):
		# Clean up configurations
		self.remove_configuration()
		
		# Write new configuration
		auth_str = ''
		if access_type == None:
			access_type = 'both'
			
		if auth_type != None and auth_type.lower()=='group':
			if auth_name == None:
				auth_name = 'Password restriction to %s' % self.groupname
			auth_str = auth_pam_group
			auth_str = auth_str.replace('<auth_name>',auth_name)
			auth_str = auth_str.replace('<groupname>',self.groupname)
			
		if servername==None:
			d = directory
			d = d.replace('<domain_name>',conf.get('DOMAIN','domain_name'))
			d = d.replace('<groupname>',self.groupname)
			d = d.replace('<auth>',auth_str)
			f = open('/etc/skolesys/www/directories/%s/%s' % (access_type,self.groupname) , 'w')
			f.write(d)
			f.close()
		else:
			d = directory
			d = d.replace('<domain_name>',conf.get('DOMAIN','domain_name'))
			d = d.replace('<groupname>',self.groupname)
			d = d.replace('<auth>',auth_str)
			f = open('/etc/skolesys/www/directories/%s/%s' % (access_type,self.groupname) , 'w')
			f.write(d)
			f.close()
		
		self.setup_resource_location()

	def setup_resource_location(self):
		print "bla"
		if not os.path.exists('%s/data' % self.resloc):
			os.system('mkdir %s/data' % self.resloc)
			os.system('chgrp %s %s/data -Rf' % (self.groupname,self.resloc))
			os.system('chmod g+rwt %s/data -Rf' % self.resloc)
		
		home_path = "%s/%s/groups/%s" % (conf.get('DOMAIN','domain_root'),conf.get('DOMAIN','domain_name'),self.groupname)
		if not os.path.exists('%s/www' % home_path):
			os.system('ln -sf %s/data %s/www' % (self.resloc,home_path))
	
		
	def restart_apache(self):
		res = os.system('apache2ctl configtest')
		if res != 0:
			return res
		os.system('apache2ctl graceful')
