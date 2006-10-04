#!/usr/bin/python

import re,grp,os,ldap
from sys import argv,exit

# Check root privilegdes
if not os.getuid()==0:
	print "This command needs requires priviledges"
	exit(0)
	
from optparse import OptionParser
from apthelpers import SourcesList
from fstabhelpers import Fstab


if __name__=='__main__':
	
	commands = {
		'mod_fstab': 'Modify fstab',
		'mod_apt_sources': 'Modify sources.list',
		'install_packages': 'Install deb/apt packages'}

	shell_cmd_name = os.path.split(argv[0])[-1:][0]
	
	usage = "usage: %s command commandfile" % shell_cmd_name
	if len(argv)<2 or not commands.has_key(argv[1]):
		print usage
		print 
		print "Commands:"
		for cmd,desc in commands.items():
			print '%s - %s' % (cmd,desc)
		exit(0)
		
	cmd = argv[1]
	
	parser = OptionParser(usage=usage)

	if cmd == "mod_fstab":
		parser.set_usage("usage: %s %s commandfile " % (shell_cmd_name,cmd))
		(options, args) = parser.parse_args()
		
		if len(args)<2:
			print "Missing commandfile for the %s operation" % cmd
			exit(0)
		commandfile = args[1]
		cf = __import__(commandfile)
		if not dir(cf).count('fstab_entries'):
			print "The commandfile %s.py does not implement the variable: %s which is mandatory for this operation" % (commandfile,'fstab_entries')
			exit(0)
		fstab = Fstab()
		for mnt in cf.fstab_entries:
			fstab.add_entry(mnt['sourcefs'],mnt['mountpoint'],mnt['fstype'],mnt['options'],mnt['dump'],mnt['fsckorder'])
		fstab.print_fstab()
		if fstab.dirty:
			fstab.write_fstab()
			print "/etc/fstab has been modified, 'mount -a' is now being executed ..."
			os.system('mount -a')
	
	if cmd == "mod_apt_sources":
		parser.set_usage("usage: %s %s commandfile " % (shell_cmd_name,cmd))
		(options, args) = parser.parse_args()
		
		if len(args)<2:
			print "Missing commandfile for the %s operation" % cmd
			exit(0)
		commandfile = args[1]
		cf = __import__(commandfile)
		if not dir(cf).count('apt_source_entries'):
			print "The commandfile %s.py does not implement the variable: %s which is mandatory for this operation" % (commandfile,'apt_source_entries')
			exit(0)
		slist = SourcesList()
		for src in cf.apt_source_entries:
			slist.add_source(src['type'],src['uri'],src['distribution'],src['components'])
		slist.print_sources_list()
		if slist.dirty:
			slist.write_sources_list()
			os.system('apt-get update')
		
	if cmd == "install_packages":
		parser.set_usage("usage: %s %s commandfile " % (shell_cmd_name,cmd))
		(options, args) = parser.parse_args()
		
		if len(args)<2:
			print "Missing commandfile for the %s operation" % cmd
			exit(0)
		commandfile = args[1]
		cf = __import__(commandfile)
		if not dir(cf).count('apt_source_entries'):
			print "The commandfile %s.py does not implement the variable: %s which is mandatory for this operation" % (commandfile,'packagelist_files')
			exit(0)
		
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
		os.system('apt-get install -y %s' % ' '.join(package_acc))
		
	if cmd == "dist_conf":
		parser.set_usage("usage: %s %s dir " % (shell_cmd_name,cmd))
		(options, args) = parser.parse_args()
		
		if len(args)<2:
			print "Missing directory for the %s operation" % cmd
			exit(0)

	if cmd == "kick_daemons":
		parser.set_usage("usage: %s %s commandfile " % (shell_cmd_name,cmd))
		(options, args) = parser.parse_args()
		
		if len(args)<2:
			print "Missing commandfile for the %s operation" % cmd
			exit(0)
	