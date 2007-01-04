import os,grp
import ConfigParser as cp
import inspect as i
#import definitions.servicedef as sd

class OptionManager:
	"""
	This class is ment to be inherited by each service's manager class
	"""

	def __init__(self,servicename,username,groupname):
		self.servicename = servicename
		self.groupname = groupname
		self.username = username
		self._lazy_res_location = None
		self.conf_parser = None

	def get_options_available(self):
		return {}

	
	def resource_location(self):
		try:
			self.gid = grp.getgrnam(self.groupname)[2]
		except Exception, e:
			print e
			print 'Group "%s" does not exist on the system' % self.groupname
			return None
		
		if self._lazy_res_location:
			return self._lazy_res_location
		
		from skolesys.lib.conf import conf
		import skolesys.services.userserviceinterface as usi
		import skolesys.services.groupserviceinterface as gsi
		
		if i.getmro(gsi.GroupServiceInterface):
			res_location = "%s/%s/services/%s/%s" % \
				(conf.get('DOMAIN','domain_root'),conf.get('DOMAIN','domain_name'),self.servicename,self.groupname)
		elif i.getmro(usi.UserServiceInterface):
			res_location = "%s/%s/services/%s/%s" % \
				(conf.get('DOMAIN','domain_root'),conf.get('DOMAIN','domain_name'),self.servicename,self.username)
		
		res_location = os.path.normpath(res_location)
		
		if not os.path.exists(res_location):
			# Resource location does not exist
			os.makedirs(res_location)
		
			# Make certain that the permissions are set right
			if self.username:
				os.system('chown %s %s -R' % (self.username,res_location))
			if self.groupname:
				os.system('chgrp %s %s -R' % (self.groupname,res_location))
			
			os.system('chmod g+wrs,o+rX,o-w %s -R -f' % res_location)
		
		self._lazy_res_location = res_location
		
		return res_location

	def get_optionparser(self):
		if self.conf_parser:
			return self.conf_parser
		import os
		res_loc = self.resource_location()
		if not res_loc:
			return None
		conf_path = "%s/config.ini" % res_loc
		if not os.path.exists(conf_path):
			f = open(conf_path,'w')
			f.close()
		f = open(conf_path)
		self.conf_parser = cp.ConfigParser()
		self.conf_parser.readfp(f)
		f.close()
		return self.conf_parser

	def save_options(self):
		if not self.conf_parser:
			print "NOTICE: No config parser is instantiated - nothing to save"
			return
		
		import os
		res_loc = self.resource_location()
		if not res_loc:
			return None
		conf_path = "%s/config.ini" % res_loc
		f = open(conf_path,'w')
		self.conf_parser.write(f)
		f.close()
		del self.conf_parser
		self.conf_parser = None


	def get_option(self,variable):
		"""
		Get a service option. 
		Returnvalues:
			False, False -	If the option is not supported or the optionparser could not be created.
			False, None -	If the option is supported but unset
			True, Value -	If the option is supported and set
		"""
		options = self.get_options_available()
		if not options.has_key(variable):
			print "FAILURE: Service does not support this option, valid options are: %s" % str(options.keys())
			return False, False
		c = self.get_optionparser()
		if not c:
			return False,False
		
		if c.has_option(options[variable]['section'],variable):
			return True, c.get(options[variable]['section'],variable)
		print "NOTICE: Service option %s not set" % variable
		return False, None


	def get_options(self):
		c = self.get_optionparser()
		if not c:
			return False
		
		avail_options = self.get_options_available()
		options = {}
		for variable,details in avail_options.items():
			if c.has_option(details['section'],variable):
				options[variable] = c.get(details['section'],variable)
		return options


	def set_option(self,variable,val):
		"""
		Set a service option. 
		Returnvalues:
			False -	If the option is not supported by the service or the value has the wrong type - or get_optionparser failed.
			True -	If everything went as planned.
		"""
		options = self.get_options_available()
		if not options.has_key(variable):
			print "FAILURE: Service does not support this option, valid options are: %s" % str(options.keys())
			return False
		
		c = self.get_optionparser()
		if not c:
			return False
		
		if not c.has_section(options[variable]['section']):
			# Create the section
			c.add_section(options[variable]['section'])
			
		c.set(options[variable]['section'],variable,val)
		self.save_options()
		return True
	

	def remove_option(self,variable):
		"""
		Set a service option. 
		Returnvalues:
			False -	If the option is not supported by the service or the value has the wrong type - or get_optionparser failed.
			True -	If everything went as planned.
		"""
		options = self.get_options_available()
		if not options.has_key(variable):
			print "FAILURE: Service does not support this option, valid options are: %s" % str(options.keys())
			return False
		
		c = self.get_optionparser()
		if not c:
			return False
		
		if c.has_option(options[variable]['section'],variable):
			c.remove_option(options[variable]['section'],variable)
		
		self.save_options()
		return True

