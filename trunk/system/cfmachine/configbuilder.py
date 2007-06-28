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

__author__ = "Jakob Simon-Gaarde <jakob@skolesys.dk>"


from infocollection import InfoCollection
import skolesys.definitions.hostdef as hostdef
from Cheetah.Template import Template
import tempfile,os


class ConfigBuilder:
	"""
	ConfigBuilder handles the SkoleSYS configuration template hierarchy. The configuration to be
	generated is controlled by the parameters given in the constructor. The constructor also 
	calls to the configuration builder method. So when the constructor returns the configuration
	scripts are build and ready to ship.
	
	The ConfigBuilder uses tempfile to create a temporary directory in the system's temp directory.
	The specific location of the configuration scripts that has been build can be read in the member
	tempdir.
	
	ConfigBuilder also packages the result into the file conf.tgz inside the temporary workspace
	directory so it can be marshalled easyly through some sort of network protocol - the SkoleSYS
	SOAP service and client provides automatic fetching of configuration scripts for registered
	hosts so a client can at any time fetch it's full configuration just by calling ss_getconf 
	as root.
	
	NOTE! The temporary workspace usually /tmp/skolesys_<somthing> is really temporary. It is 
	deleted by the destructor. So to fetch the result you must keep the ConfigBuilder instance
	alive long enough for you to make a copy.
	
	The template hierarchi:
	----------------------
	SkoleSYS ships with default configuration templates, but the resulting configuration scripts
	can easyly be customized. For instance if a particular organization wishes to customize the 
	/etc/hosts file generated for workstations it is done by copying the default /etc/hosts file
	into the custom-templates hierarchi and changing it there. This mechanism ensures 2 things:
		1. The default-templates remain untouched.
		2. SkoleSYS mainserver updates don't overwrite the organization cusomizations.
		
	A side from the default templates there are 2 levels of cusomizations:
		(0. default-templates)
		1. custom-templates (general customizations)
		2. host-templates (host specific customizations)
	
	Inside the default-templates and custom-templates exists a 'common' directory, a directory 
	per hosttype ('mainserver','ltspserver','workstation') and a 'contexts' directory which 
	again holds one directory per hosttype
		example:
		/etc/skolesys/default-templates/common
		/etc/skolesys/default-templates/mainserver
		/etc/skolesys/default-templates/ltspserver
		/etc/skolesys/default-templates/workstation
		/etc/skolesys/default-templates/contexts/mainserver
		/etc/skolesys/default-templates/contexts/ltspserver
	
	The host-templates holds a mac-address folder per host having special configurations
		example:
		host-templates/01:02:03:04:05:06
		host-templates/01:23:45:67:89:ab
	
	Distribution end points are used to target the specific Ubuntu version of the system requesting its configuration. The ss_getconf
	command on skolesys clients (ltspserver or workstation) will automatically detect the distribution codename.
	
	The configuration hierarchi is as follows for host '01:23:45:67:89:ab' with hosttype 'ltspserver' running on Ubuntu codename 'feisty':
		default-templates/common/all
		default-templates/common/feisty
		default-templates/mainserver/all
		default-templates/mainserver/feisty
		custom-templates/common/all
		custom-templates/common/feisty
		custom-templates/mainserver/all
		custom-templates/mainserver/feisty
		host-templates/01:23:45:67:89:ab/all (you could add 'feisty' here too but there is not much point in it)
	
	So what happens is that all files files under the each of the directories above are parsed 
	recursively using python cheetah. The data used to parse the files origin partially from 
	skolesys,conf and partially from the hosts registered in the ldap back-end.
	
	Contexts:
	--------
	Contexts (context argument) are used for creating specialized configurations used for certain events. 
	When in context mode it is possible to skip the basic hierarchi (from above) and just run through
	the context alone (context_only argument) in the examples below are shown a context parse with
	context_only and one in combination with the basic hierarchi.
	
	The configuration hierarchi for host '01:23:45:67:89:ab' with hosttype 'mainserver' in the 
	context 'update-hosts' (context_only=True):
		default-templates/contexts/mainserver/update-hosts
		custom-templates/contexts/mainserver/update-hosts
		host-templates/contexts/01:23:45:67:89:ab/mainserver/update-hosts
	
	The configuration hierarchi for host '01:23:45:67:89:ab' with hosttype 'mainserver' in the 
	context 'update-hosts' (context_only=False):
		default-templates/common
		default-templates/mainserver
		default-templates/contexts/mainserver/update-hosts
		custom-templates/common
		custom-templates/mainserver
		custom-templates/contexts/mainserver/update-hosts
		host-templates/01:23:45:67:89:ab
		host-templates/contexts/01:23:45:67:89:ab/mainserver/update-hosts
	"""


	def __init__(self,hosttype_id,dist_codename,hwaddr=None,context=None,context_only=False,pretend=False):
		"""
		Build the configuration for a certain hosttype or host. It works in a threaded or
		asynchronious environment by ensuring that a unique temp space is created in /tmp 
		
		1. Create temp directory.
		2. Fetch system, domain and hosts information.
		3. Initiate the configuration parser.
		"""
		self.hosttype = hostdef.hosttype_as_text(hosttype_id)
		self.hwaddr = hostdef.check_hwaddr(hwaddr)
		self.dist_codename = dist_codename
		self.context = context
		self.context_only = context_only
		
		# Create a temp directory
		self.tempdir = tempfile.mkdtemp(prefix='skolesys_')
		
		# Collect info about domain and host
		self.infocollection = InfoCollection(self.hwaddr)
		
		# Build the configuration
		self.build_config(pretend)
		
		
	def build_config(self,pretend):
		"""
		1. Parse the templates
		2. Create a resulting archive file for export
		"""
		
		def store_link(args,dirname,fnames):
			"""
			This function is used by os.path.walk to collect which config templates
			should be used for a certain hosttype, host and context.
			"""
			temp_level, file_location = args
			for f in fnames:
				if os.path.isfile(os.path.join(dirname,f)):
					file_location[os.path.join(dirname[len(temp_level):],f)] = os.path.join(dirname,f)
		
		level_order = ['default','custom','host']
		
		dist_order = ['all',self.dist_codename]
		
		system_order = []
		if not self.context or not self.context_only:
			system_order += ['common']
			system_order += [self.hosttype]
			if self.hwaddr:
				system_order += [self.hwaddr]
			
		if self.context:
			system_order += ['contexts/%s/%s' % (self.hosttype,self.context)]
			if self.hwaddr:
				system_order += ['contexts/%s/%s/%s' % (self.hwaddr,self.hosttype,self.context)]
		
		file_location = {}
		template_basedir = self.infocollection.get_collection()['conf']['cfmachine']['template_basedir']
	
		# Determin the config-files for the specific host type and mac-address
		for level in level_order:
			for system in system_order:
				for dist in dist_order:
					if os.path.exists("%s/%s-templates/%s/%s" % (template_basedir,level,system,dist)):
						os.path.walk("%s/%s-templates/%s/%s" % (template_basedir,level,system,dist),\
							store_link,("%s/%s-templates/%s/%s/" % (template_basedir,level,system,dist),file_location))
		
		if pretend==True:
			for fi in file_location.keys():
				print fi
				print " -> %s" % file_location[fi]
			return
		
		# Copy the config files running them through cheetah
		for k,v in file_location.items():
			f_stat = os.stat(v)
			mod,uid,gid,siz = f_stat.st_mode,f_stat.st_uid,f_stat.st_gid,f_stat.st_size
			destfile = os.path.join(self.tempdir,k)
			destdir =  os.path.split(destfile)[0]
			try:
				os.makedirs(destdir)
			except:
				pass
			
			if siz > 0:
				t = Template(file=v, searchList=[self.infocollection.get_collection()])
			else:
				t = ''

			f=open(destfile,'w')
			print "Fil: %s" % v
			try:
				f.write(t.__str__())
			except Exception, e:
				print "%s, (while parsing %s)" % (e,v)
				f.close()
				return False
			f.close()
			os.chmod(destfile,mod)
			os.chown(destfile,uid,gid)
			
		# Finally create a tarball for network export
		curdir = os.getcwd()
		os.chdir(self.tempdir)
		os.system('tar czpf conf.tgz *')
		os.chdir(curdir)
		return True

	def __del__(self):
		os.system('rm %s -R -f' % self.tempdir)

if __name__=='__main__':
	# test
	a=ConfigBuilder(1,'feisty','0040b94c8900',pretend=False)
	
