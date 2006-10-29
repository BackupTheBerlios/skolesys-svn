from infocollection import InfoCollection
import skolesys.definitions.hostdef as hostdef
from Cheetah.Template import Template
import tempfile,os

class ConfigBuilder:

	def __init__(self,hosttype_id,hwaddr=None,context=None,include_common=True):
		"""
		1. Create temp directory
		2. Fetch 
		"""
		self.hosttype = hostdef.hosttype_as_text(hosttype_id)
		self.hwaddr = hostdef.check_hwaddr(hwaddr)
		self.context = context
		self.include_common = include_common
		self.tempdir = tempfile.mkdtemp(prefix='skolesys_')
		self.infocollection = InfoCollection(self.hwaddr)
		self.build_config()
		
	def build_config(self):
		"""
		Build the configuration for a certain hosttype or host. It works in a threaded or
		asynchronious environment by ensuring that a unique temp space is created in /tmp 
		2. Parse the templates
		3. Create a resulting archive file for export
		"""
		
		def store_link(args,dirname,fnames):
			"""
			This function is used by os.path.walk to collect which config templates
			should be used for a certain hosttype and host
			"""
			temp_level, file_location = args
			for f in fnames:
				if os.path.isfile(os.path.join(dirname,f)):
					file_location[os.path.join(dirname[len(temp_level):],f)] = os.path.join(dirname,f)
		
		level_order = ['default','custom','host']
		system_order = [self.hosttype]
		if self.context:
			system_order += ['contexts/%s' % self.context]
		if self.include_common:
			system_order = ['common'] + system_order
		
		if self.hwaddr:
			system_order += [self.hwaddr]
	
		file_location = {}
		template_basedir = self.infocollection.get_collection()['conf']['cfmachine']['template_basedir']
	
		# Determin the config-files for the specific host type and mac-address
		for level in level_order:
			for system in system_order:
				if os.path.exists("%s/%s-templates/%s" % (template_basedir,level,system)):
					os.path.walk("%s/%s-templates/%s" % (template_basedir,level,system),\
						store_link,("%s/%s-templates/%s/" % (template_basedir,level,system),file_location))
		
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
	a=ConfigBuilder(2,'010203040506')
	
