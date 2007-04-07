import os
from skolesys.lib.conf import conf

auth_pam_group = """
		AuthPAM_Enabled on
		AuthType Basic
		AuthName "<auth_name>"
		require group "<groupname>"
	"""

directory = """
        Alias /<groupname> /skolesys/denskaegge.dk/services/webservice/<groupname>/data/

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
			
		if auth_type.lower()=='group':
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
			f = open('/etc/skolesys/www/directories/intra/%s' % self.groupname , 'w')
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

	def setup_resource_location(self):
		if not os.path.exists('%s/data' % self.resloc):
			os.system('mkdir %s/data' % self.resloc)
			os.system('chgrp %s %s/data -Rf' % (self.groupname,self.resloc))
			os.system('chmod g+rwt %s/data -Rf' % self.resloc)

		home_path = "%s/%s/groups/%s" % (conf.get('DOMAIN','domain_root'),conf.get('DOMAIN','domain_name'),self.groupname)
		if not os.path.exists('%s/www' % home_path):
			os.system('ln -s %s/data %s/www' % (self.resloc,home_path))
	
		