#!/usr/bin/python

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

"""
ss_installer -> cfinstaller.py  (symlink on installed systems)

cfinstaller is a client confuguration deployment tool. It is accessible
from command line as ss_installer (symlink created when one of the 
SkoleSYS packages are installed (python-skolesys-mainserver,
python-skolesys-client or python-skolesys-seeder).

ss_installer can perform the following operations:

  Command (Argument 1)   |  Description
  ----------------------------------------------------------------------------------
  mod_fstab              |  Modify fstab
  mod_apt_sources        |  Modify sources.list
  install_packages       |  Install deb/apt packages
  copy_files             |  Copy files recursively from a base directory to the root fs
  set_hostname           |  Set the hostname for the host
  run_script             |  Run a script file
  kick_daemons           |  Kick some daemons that need to reload the configuration changes

Usage: ss_installer command (controlfile|scriptname)
(scriptname when the command is run_script)

When ss_installer is executed it runs only one of the commands. It takes a 
controlfile as Argument 2 that describes how to perform a certain command.
Control data for ss_installer is stored as local variables in the 
controlfile:

  ss_installer Command   | Control file variable
  -------------------------------------------------
  mod_fstab              | fstab_entries
  mod_apt_sources        | apt_source_entries
  install_packages       | packagelist_files
  copy_files             | copy_files_rootdir
  set_hostname           | hostname
  kick_daemons           | kick_daemons

Note. run_script command takes the path to a script as argument 2 instead
of a controlfile.

The following example is taken out of the configuration system's
default-templates (default-templates/common/all/install.sh). It uses
ss_installer to deploy host configurations:

install.sh:
----------
#!/bin/sh
if ! ss_installer mod_apt_sources cf_install
then
        echo "ss_installer failed to update source.list"
        exit 1
fi

if ! ss_installer install_packages cf_install
then
        echo "ss_installer failed to install packages"
        exit 1
fi

if ! ss_installer copy_files cf_install
then
        echo "ss_installer failed to copy configuration files"
        exit 1
fi

if ! ss_installer set_hostname cf_install
then
        echo "ss_installer failed to set the hostname"
        exit 1
fi

if ! ss_installer kick_daemons cf_install
then
        echo "ss_installer failed kick daemons"
        exit 1
fi

if ! ss_installer mod_fstab cf_install
then
        echo "ss_installer failed update fstab"
        exit 1
fi
exit 0

This is the controlfile used by the script. It also taken from the
default configuration templates (default-templates/mainserver/feisty/cf_install.py)

cf_install.py: 
-------------
apt_source_entries = [
	{'type':'deb','uri':'http://archive.skolesys.dk/$[conf.cfmachine.package_group]','distribution':'dapper','components':['main']},
        {'type':'deb','uri':'http://archive.ubuntu.com/ubuntu/','distribution':'dapper','components':['main','restricted','universe']},
        {'type':'deb-src','uri':'http://archive.ubuntu.com/ubuntu/','distribution':'dapper','components':['main','restricted','universe']},
        {'type':'deb','uri':'http://archive.ubuntu.com/ubuntu/','distribution':'dapper-backports','components':['main','restricted','universe','multiverse']},
        {'type':'deb-src','uri':'http://archive.ubuntu.com/ubuntu/','distribution':'dapper-backports','components':['main','restricted','universe','multiverse']},
        {'type':'deb','uri':'http://security.ubuntu.com/ubuntu','distribution':'dapper-security','components':['main','restricted','universe']},
        {'type':'deb-src','uri':'http://security.ubuntu.com/ubuntu','distribution':'dapper-security','components':['main','restricted','universe']}]

fstab_entries = [
	{'sourcefs':'mainserver.skolesys.local:/skolesys','mountpoint':'/skolesys','fstype':'nfs','options':'defaults','dump':'0','fsckorder':'0'}]
	
packagelist_files = [
	'default-packages','custom-packages']

copy_files_rootdir = \
	'rootdir'

hostname = \
	'$reciever.hostName'

kick_daemons = [
	'/etc/init.d/networking restart',
	'/etc/init.d/dhcp3-server restart',
	'/etc/init.d/nfs-kernel-server restart',
	'/etc/init.d/nfs-common restart',
	'/etc/init.d/tftpd-hpa restart']
"""

__author__ = "Jakob Simon-Gaarde <jakob@skolesys.dk>"

import re,os
from sys import argv,exit,path
path += ['.']

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
		
	# Check root privilegdes
	if not os.getuid()==0:
		print "This command requires root priviledges"
		exit(2000)
	
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
