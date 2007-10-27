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

import skolesys.tools.mkpasswd as pw
import getpass,os,time,re,sys
import inspect
import skolesys.cfmachine.apthelpers as apthelper
import skolesys.tools.sysinfo as sysinfo
from optparse import OptionParser

def init_client(clienttype,hostname=None):
	# Check root privilegdes
	if not os.getuid()==0:
		print "This command requires root priviledges"
		return 1
	
	if not hostname:
		os.system('clear')
		print "To create a SkoleSYS %s you must register the host with the mainserver" % clienttype
		print "-------------------------------------------------------------------------------"
		hostname = raw_input('%s hostname: ' % clienttype)
	
	package_group = raw_input('What package group do you wish to run (testing/stable) [stable]: ')
	if package_group == '':
		package_group = 'stable'

	if not ['testing','stable'].count(package_group):
		print "%s is not a valid package group"
		sys.exit(1)
	
	# INSTALL
	
	# Wipe sources.list on mainserver install
	os.system('echo "" > /etc/apt/sources.list')
	
	# fetch the release codename
	codename = sysinfo.get_dist_codename()

	# ensure some entries in sources.list
	apt_source_entries = [
		{'type':'deb','uri':'http://archive.skolesys.dk/stable','distribution':codename,'components':['main']},
		{'type':'deb','uri':'http://archive.ubuntu.com/ubuntu/','distribution':codename,'components':['main','restricted','universe']},
		{'type':'deb-src','uri':'http://archive.ubuntu.com/ubuntu/','distribution':codename,'components':['main','restricted','universe']},
		{'type':'deb','uri':'http://archive.ubuntu.com/ubuntu/','distribution':'%s-backports' % codename ,'components':['main','restricted','universe','multiverse']},
		{'type':'deb-src','uri':'http://archive.ubuntu.com/ubuntu/','distribution':'%s-backports' % codename,'components':['main','restricted','universe','multiverse']},
		{'type':'deb','uri':'http://archive.ubuntu.com/ubuntu/','distribution':'%s-updates' % codename ,'components':['main','restricted','universe','multiverse']},
		{'type':'deb-src','uri':'http://archive.ubuntu.com/ubuntu/','distribution':'%s-updates' % codename,'components':['main','restricted','universe','multiverse']},
		{'type':'deb','uri':'http://security.ubuntu.com/ubuntu','distribution':'%s-security' % codename,'components':['main','restricted','universe']},
		{'type':'deb-src','uri':'http://security.ubuntu.com/ubuntu','distribution':'%s-security' % codename,'components':['main','restricted','universe']}]
	
	slist = apthelper.SourcesList()
	for src in apt_source_entries:
		slist.add_source(src['type'],src['uri'],src['distribution'],src['components'])
	slist.print_sources_list()
	if slist.dirty:
		slist.write_sources_list()
		res = os.system('apt-get update')
		if not res==0:
			print
			print "SkoleSYS Seeder - failed while updating packages"
			return 1
	
	# Replace python-skolesys-seeder with python-skolesys-mainserver
	os.environ['DEBIAN_FRONTEND'] = 'noninteractive'
	os.environ['DEBCONF_ADMIN_EMAIL'] = ''
	
	res = os.system('ss_reghost -n %s -t %s -r' % (hostname,clienttype))
	if not res==0:
		print
		print "SkoleSYS Seeder - failed while updating packages"
		return 1
	
	res = os.system('ss_getconf')
	if not res==0:
		print
		print "SkoleSYS Seeder - failed while updating packages"
		return 1


if __name__=='__main__':
	
	# Check root privilegdes
	if not os.getuid()==0:
		print "This command requires root priviledges"
		sys.exit(1)
		
	os.system('clear')
	shell_cmd_name = os.path.split(sys.argv[0])[-1:][0]
	parser = OptionParser(usage="usage: %s [options]" % (shell_cmd_name))
	parser.add_option("-t", "--client-type", dest="clienttype",default='',
				help="The type og SkoleSYS client to be seeded (workstation,ltspserver)", metavar="CLIENTTYPE")
	(options, args) = parser.parse_args()
	
	types = ['workstation','ltspserver']
	
	if not types.count(options.clienttype):
		print "What type of client do you wish to seed"
		print "---------------------------------------"
		while not types.count(options.clienttype):
			options.clienttype = raw_input('Client type (%s): ' % ','.join(types)).lower()
		print
		print
		
	print "To create a SkoleSYS %s you must register the host with the mainserver" % options.clienttype
	print "-------------------------------------------------------------------------------"
	
	hostname = raw_input('%s hostname: ' % options.clienttype)
	sys.exit(init_client(options.clienttype,hostname))
