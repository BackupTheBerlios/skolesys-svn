#!/usr/bin/python

import re,os
from sys import argv,exit,path
path += ['.']

# Check root privilegdes
if not os.getuid()==0:
	print "This command requires root priviledges"
	exit(2000)
	
from optparse import OptionParser
from skolesys.cfmachine.apthelpers import SourcesList
from skolesys.cfmachine.fstabhelpers import Fstab


if __name__=='__main__':
	
	commands = {
		'mod_fstab': 'Modify fstab',
		'mod_apt_sources': 'Modify sources.list',
		'install_packages': 'Install deb/apt packages',
		'copy_files': 'Copy files recursively from a base directory to the root fs',
		'set_hostname': 'Set the hostname for the host',
		'run_script': 'Run a script file',
		'kick_daemons': 'Kick some daemons that need to reload the configuration changes'}

	shell_cmd_name = os.path.split(argv[0])[-1:][0]
	
	usage = "usage: %s command controlfile" % shell_cmd_name
	if len(argv)<2 or not commands.has_key(argv[1]):
		print usage
		print 
		print "Commands:"
		for cmd,desc in commands.items():
			print '%s - %s' % (cmd,desc)
		exit(101)
		
	cmd = argv[1]
	
	parser = OptionParser(usage=usage)

	if cmd == "mod_fstab":
		parser.set_usage("usage: %s %s controlfile " % (shell_cmd_name,cmd))
		(options, args) = parser.parse_args()
		
		if len(args)<2:
			print "Missing controlfile for the %s operation" % cmd
			exit(102)
		controlfile = args[1]
		cf = __import__(controlfile)
		if not dir(cf).count('fstab_entries'):
			print "The controlfile %s.py does not implement the variable: %s which is mandatory for this operation" % (controlfile,'fstab_entries')
			exit(103)
		fstab = Fstab()
		for mnt in cf.fstab_entries:
			fstab.add_entry(mnt['sourcefs'],mnt['mountpoint'],mnt['fstype'],mnt['options'],mnt['dump'],mnt['fsckorder'])
			if not os.path.exists(mnt['mountpoint']):
				print 'The mountpoint "%s" does not exist. Creating it now.' % mnt['mountpoint']
				os.makedirs(mnt['mountpoint'])
		fstab.print_fstab()
		if fstab.dirty:
			fstab.write_fstab()
			print "/etc/fstab has been modified, 'mount -a' is now being executed ..."
			exit(os.system('mount -a'))
	
	if cmd == "mod_apt_sources":
		parser.set_usage("usage: %s %s controlfile " % (shell_cmd_name,cmd))
		(options, args) = parser.parse_args()
		
		if len(args)<2:
			print "Missing controlfile for the %s operation" % cmd
			exit(201)
		controlfile = args[1]
		cf = __import__(controlfile)
		if not dir(cf).count('apt_source_entries'):
			print "The controlfile %s.py does not implement the variable: %s which is mandatory for this operation" % (controlfile,'apt_source_entries')
			exit(202)
		slist = SourcesList()
		for src in cf.apt_source_entries:
			slist.add_source(src['type'],src['uri'],src['distribution'],src['components'])
		slist.print_sources_list()
		if slist.dirty:
			slist.write_sources_list()
		exit(os.system('apt-get update'))
		
	if cmd == "install_packages":
		parser.set_usage("usage: %s %s controlfile " % (shell_cmd_name,cmd))
		(options, args) = parser.parse_args()
		
		if len(args)<2:
			print "Missing controlfile for the %s operation" % cmd
			exit(301)
		controlfile = args[1]
		cf = __import__(controlfile)
		if not dir(cf).count('apt_source_entries'):
			print "The controlfile %s.py does not implement the variable: %s which is mandatory for this operation" % (controlfile,'packagelist_files')
			exit(302)
		
		package_acc = []
		
		for plist in cf.packagelist_files:
			f = open(plist)
			packages = f.readlines()
			f.close()
			for p in packages:
				if not p.strip()=='':
					package_acc += [ p.strip() ]
					
		os.environ['DEBIAN_FRONTEND'] = 'noninteractive'
		os.environ['DEBCONF_ADMIN_EMAIL'] = ''
		print ' '.join(package_acc)
		exit(os.system('apt-get install -y %s' % ' '.join(package_acc)))
		
	if cmd == "copy_files":
		parser.set_usage("usage: %s %s controlfile " % (shell_cmd_name,cmd))
		(options, args) = parser.parse_args()
		
		if len(args)<2:
			print "Missing controlfile for the %s operation" % cmd
			exit(401)
		controlfile = args[1]
		cf = __import__(controlfile)
		if not dir(cf).count('copy_files_rootdir'):
			print "The controlfile %s.py does not implement the variable: %s which is mandatory for this operation" % (controlfile,'copy_files_rootdir')
			exit(402)
		
		if not type(cf.copy_files_rootdir) == str:
			print "The %s variable must be assigned a single string value." % 'copy_files_rootdir'
			exit(403)
			
		if not os.path.exists(cf.copy_files_rootdir):
			print "The root directory %s does not seem to exist." % cf.copy_files_rootdir
		exit(os.system('cp %s/* / -Rfc' % cf.copy_files_rootdir))
		

	if cmd == "set_hostname":
		parser.set_usage("usage: %s %s controlfile " % (shell_cmd_name,cmd))
		(options, args) = parser.parse_args()
		
		if len(args)<2:
			print "Missing controlfile for the %s operation" % cmd
			exit(501)
		controlfile = args[1]
		cf = __import__(controlfile)
		if not dir(cf).count('hostname'):
			print "The controlfile %s.py does not implement the variable: %s which is mandatory for this operation" % (controlfile,'hostname')
			exit(502)
		
		if not type(cf.hostname) == str:
			print "The %s variable must be assigned a single string value." % 'hostname'
			exit(503)
		
		print "Setting hostname to %s" % cf.hostname
		os.environ['HOSTNAME'] = cf.hostname
		os.system('hostname %s' % cf.hostname)
		f = open('/etc/hostname','w')
		f.write('%s\n' % cf.hostname)
		f.close()


	if cmd == "run_script":
		parser.set_usage("usage: %s %s controlfile " % (shell_cmd_name,cmd))
		parser.add_option("-i", "--interpretor", dest="interpretor",default='',
		                  help="The interpretor to be used for excuting the script", metavar="INTERPRETOR")
		(options, args) = parser.parse_args()
		if len(args)<2:
			print "Missing script file for the %s operation" % cmd
			exit(601)

		script_file = args[1]
		exit(os.system("%s %s" % (options.interpretor,script_file)))

	
	if cmd == "kick_daemons":
		parser.set_usage("usage: %s %s controlfile " % (shell_cmd_name,cmd))
		(options, args) = parser.parse_args()
		
		if len(args)<2:
			print "Missing controlfile for the %s operation" % cmd
			exit(701)
		controlfile = args[1]
		cf = __import__(controlfile)
		if not dir(cf).count('kick_daemons'):
			print "The controlfile %s.py does not implement the variable: %s which is mandatory for this operation" % (controlfile,'kick_daemons')
			exit(702)
		
		if not type(cf.kick_daemons) == tuple and not type(cf.kick_daemons) == list:
			print "The %s variable must be assigned a sequence." % 'kick_daemons'
			exit(703)
			
		for kick in cf.kick_daemons:
			os.system(kick)

	exit(0)
