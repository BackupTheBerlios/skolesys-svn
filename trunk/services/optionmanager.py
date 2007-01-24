import os,grp
import ConfigParser as cp
import inspect as i
#import definitions.servicedef as sd

true_strings = ['true','yes','on']
false_strings = ['false','no','off']

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


	def _conv_to_regtype(self,rawval,regtyp):
		"""
		Try to convert a raw text-based config value to a certain type
		"""
		rawval = rawval.strip()
		if regtyp == int:
			if rawval.isdigit():
				return int(rawval)
		
		if regtyp == str:
			return rawval
		
		if regtyp == bool:
			if rawval.isdigit():
				return bool(int(rawval))
			elif true_strings.count(rawval.lower()):
				return True
			elif false_strings.count(rawval.lower()):
				return False
		
		return None

	def get_option(self,variable,raw=False):
		"""
		Get a service option. 
		Returnvalues:
			False, False -	If the option is not supported or cannot be typecasted or the optionparser could not be created.
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
			rawval = c.get(options[variable]['section'],variable)
			if raw:
				return True, rawval
			else:
				if not options[variable].has_key('type'):
					print "FAILURE: The option seems to be registered without a type and therfore disregarded."
					return False, False
				
				opttyp = options[variable]['type']
				if not type(opttyp) == type:
					print "FAILURE: The option's type is not of type: type and therfore disregarded."
					return False, False
				
				val = self._conv_to_regtype(rawval,opttyp)
				if not val == None:
					return True, val
				
		print "NOTICE: Service option %s not set" % variable
		return False, None


	def get_options(self,raw=False):
		c = self.get_optionparser()
		if not c:
			return False
		
		avail_options = self.get_options_available()
		options = {}
		for variable in avail_options.keys():
			res,val = self.get_option(variable,raw)
			if res == True:
				options[variable] = val
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
		
		if not options[variable].has_key('type'):
			print "FAILURE: The option seems to be registered without a type and therfore disregarded."
			return False
		
		opttyp = options[variable]['type']
		if not type(opttyp) == type:
			print "FAILURE: The option's type is not of type: type and therfore disregarded."
			return False
		
		# check validity of the option being set
		valtyp = type(val)
		endval = None
		if opttyp == int:
			if valtyp == int or valtyp == long or valtyp == bool:
				endval = int(val) # If the type is long python auto-switches the type to long anyway
			if valtyp == str and val.isdigit():
				endval = int(val)
				
		elif opttyp == str:
			endval = str(val)
			
		elif opttyp == bool:
			if valtyp == int or valtyp == long or valtyp == bool:
				endval = bool(val)
		
			if valtyp == str:
				if val.isdigit():
					endval = bool(int(val))
				elif true_strings.count(val.lower()):
					endval = True
				elif false_strings.count(val.lower()):
					endval = False
	
		if endval == None: #Value could not be type-casted to any the registered type
			print "FAILURE: The option %s is registered %s the incomming has type %s and value: %s" % \
				(variable,opttyp,valtyp,str(val))
			return False
	
		c = self.get_optionparser()
		if not c:
			return False
		
		if not c.has_section(options[variable]['section']):
			# Create the section
			c.add_section(options[variable]['section'])
			
		c.set(options[variable]['section'],variable,endval)
		self.save_options()
		return True
	

	def unset_option(self,variable):
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

