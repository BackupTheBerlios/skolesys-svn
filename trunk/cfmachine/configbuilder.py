from infocollection import InfoCollection
from skolesys.lib.hostmanager import translate_hosttype_id,check_hwaddr
from Cheetah.Template import Template
import tempfile,os

class ConfigBuilder:

	def __init__(self,hosttype_id,hwaddr=None):
		"""
		1. Create temp directory
		2. Fetch 
		"""
		self.hosttype = translate_hosttype_id(hosttype_id)
		self.hwaddr = check_hwaddr(hwaddr)
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
		system_order = ['common',self.hosttype]
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
			mod,uid,gid = f_stat[0],f_stat[4],f_stat[5]
			destfile = os.path.join(self.tempdir,k)
			destdir =  os.path.split(destfile)[0]
			try:
				os.makedirs(destdir)
			except:
				pass
			t = Template(file=v, searchList=[self.infocollection.get_collection()])
			f=open(destfile,'w')
			f.write(t.__str__())
			f.close()
			os.chmod(destfile,mod)
			os.chown(destfile,uid,gid)
			
		# Finally create a tarball for network export
		curdir = os.getcwd()
		os.chdir(self.tempdir)
		os.system('tar czpf conf.tgz rootdir scripts')
		os.chdir(curdir)

	def __del__(self):
		os.system('rm %s -R -f' % self.tempdir)

if __name__=='__main__':
	# test
	a=ConfigBuilder(2,'010203040506')
	
