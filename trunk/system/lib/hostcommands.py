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

import re,grp,os,ldap
from sys import argv,exit


from optparse import OptionParser
import hostmanager,sambacontroller
import skolesys.definitions.hostdef as hostdef


if __name__=='__main__':
	
	commands = {
		'hostadd': 'Register a new host to the network',
		'hostinfo': 'List the registered information of a host',
		'listhosts': 'List registered hosts',
		'join_domain': 'Let a host join a samba domain'}

	shell_cmd_name = os.path.split(argv[0])[-1:][0]
	
	usage = "usage: %s [command] [options] arg1, arg2" % shell_cmd_name
	if len(argv)<2 or not commands.has_key(argv[1]):
		print usage
		print 
		print "Commands:"
		for cmd,desc in commands.items():
			print '%s - %s' % (cmd,desc)
		exit(0)
		
	# Check root privilegdes
	if not os.getuid()==0:
		print "This command requires root priviledges"
		exit(0)
		
	from conf import conf
	
	cmd = argv[1]
	
	parser = OptionParser(usage=usage)

	if cmd == "hostadd":
		parser.set_usage("usage: %s %s [options] hostname " % (shell_cmd_name,cmd))
		parser.add_option("-m", "--hw-addr", dest="hwaddr",default=None,
		                  help="The hardware address of the host's network interface (mac-address)", metavar="HWADDR")
		parser.add_option("-t", "--host-type", dest="hosttype",default=None,
		                  help="The host's type (mainserver,ltspserver,workstation)", metavar="HOSTTYPE")
		parser.add_option("-i", "--ip-address", dest="ipaddr",default=None,
		                  help="Try to register the host with this ip-address", metavar="IPADDR")
		(options, args) = parser.parse_args()
		
		if len(args)<2:
			print "Missing hostname for the hostadd operation"
			exit(0)
		
		hostname = hostdef.check_hostname(args[1])
		if not hostname:
			print "The entered hostname is invalid"
			exit(0)
			
		# Check if this hostname is already registered
		hm = hostmanager.HostManager()
		if hm.host_exists(hostname=hostname):
			print 'The hostname: "%s" has already been registered use hostmod instead' % hostname
			exit(0)
		
		if options.ipaddr:
			ipchk = hostdef.check_ipaddr(options.ipaddr)
			if not ipchk:
				print 'The ipaddress: "%s" entered is not valid' % options.ipaddr
				exit(0)
				
		print "Hostname: %s" % hostname
		
		while not options.hwaddr or not hostdef.check_hwaddr(options.hwaddr):
			options.hwaddr = raw_input("Input the hardware address of the host's network interface (mac-address): ")
		options.hwaddr = hostdef.check_hwaddr(options.hwaddr)
			
		
		# Check if this hwaddr is already registered
		if hm.host_exists(hwaddr=options.hwaddr):
			print 'The hwaddr: "%s" has already been registered use hostmod instead' % options.hwaddr
			exit(0)
			
		while not options.hosttype or not hostdef.hosttype_as_id(options.hosttype):
			options.hosttype = raw_input("Input the host type (%s): " % ','.join(hostdef.list_hosttypes_by_text()))
		hosttype_id = hostdef.hosttype_as_id(options.hosttype)
		
		try:
			hostadd_res = hm.register_host(options.hwaddr,hostname,hosttype_id,options.ipaddr)
		except Exception, e:
			print e
			print "An error occured while writing to the user LDAP database"
			exit(0)
		
		# Errors -1 to -4 are alle sanitychecks on string formats and have already been done.
		if hostadd_res==-5:
			print 'The hwaddr: "%s" is already registered - use host mod to modify it.' % options.hwaddr
			exit(0)
		if hostadd_res==-6:
			print 'The hostname: "%s" is already registered - use host mod to modify it.' % hostname
			exit(0)
		
		if hostadd_res==-7:
			print 'The ip-address: "%s" is statically assigned to another host.' % options.ipaddr
			exit(0)
		
		if hostadd_res==-8:
			print 'An ip address could not be assigned, no more addresses in the ip range of the host type (expand the iprange in skolesys.conf)'
			exit(0)
			
		print "Host registered..."

	if cmd == "hostinfo":
		parser.set_usage("usage: %s %s ( -m hwaddr | -n hostname ) [options]" % (shell_cmd_name,cmd))
		parser.add_option("-m", "--hw-addr", dest="hwaddr",default=None,
			help="The hardware address of the host's network interface (mac-address)", metavar="HWADDR")
		parser.add_option("-n", "--hostname", dest="hostname",default=None,
			help="The hostname of the host", metavar="HOSTNAME")
		parser.add_option("--no-header",
			action="store_true", dest="noheader", default=False,
			help="Show the host without the column header")
		(options, args) = parser.parse_args()
		
		# Create a host manager instance
		hm = hostmanager.HostManager()
		
		if options.hwaddr:
			hwaddr = hostdef.check_hwaddr(options.hwaddr)
			if not hwaddr:
				print 'The hwaddr: "%s" is not valid.' % options.hwaddr
				exit(0)
			hinfo = hm.host_info(hwaddr=hwaddr)
			matchtype = 'hwaddr'
			matchstring = hwaddr
			
		elif options.hostname:
			hostname = hostdef.check_hostname(options.hostname)
			if not hostname:
				print 'The hostname: "%s" is not valid.' % options.hostname
				exit(0)
			hinfo = hm.host_info(hostname=hostname)
			matchtype = 'hostname'
			matchstring = hostname
		else:
			print "You must enter either option -m or -n."
			exit(0)
		if not hinfo:
			print 'No host exists with the %s: "%s"' % (matchtype,matchstring)
			exit(0)
			
		if not options.noheader:
			print "%-20s   %-15s   %-17s   %s" % ('Hostname','IPaddress','HWaddress','Hosttype')
		print "%-20s   %-15s   %-17s   %s" % (hinfo['hostName'][0],hinfo['ipHostNumber'][0],hinfo['macAddress'][0],hinfo['hostType'][0])
			
		
	if cmd == "listhosts":
		parser.set_usage("usage: %s %s [options]" % (shell_cmd_name,cmd))
		parser.add_option("-t", "--host-type", dest="hosttype",default=None,
		                  help="The host's type (mainserver,ltspserver,workstation)", metavar="HOSTTYPE")
		parser.add_option("--no-header",
			action="store_true", dest="noheader", default=False,
			help="Show the host without the column header")
		(options, args) = parser.parse_args()
		
		hosttype_id = None
		if options.hosttype:
			hosttype_id = hostdef.hosttype_as_id(options.hosttype)
			if not hosttype_id:
				print 'The host type: "%s" is not valid.' % options.hosttype
				
		hm = hostmanager.HostManager()
		hlist = hm.list_hosts(hosttype_id)
		if not hlist or not len(hlist):
			print "No hosts seem to be registered"
		
		if not options.noheader:
			print "%-20s   %-15s   %-17s   %s" % ('Hostname','IPaddress','HWaddress','Hosttype')
		for hinfo in hlist:
			print "%-20s   %-15s   %-17s   %s" % (hinfo['hostName'][0],hinfo['ipHostNumber'][0],hinfo['macAddress'][0],hinfo['hostType'][0])

	if cmd == "join_domain":
		parser.set_usage("usage: %s %s netbiosname ntdomain" % (shell_cmd_name,cmd))
		(options, args) = parser.parse_args()
		if len(args) < 3:
			print parser.usage
		netbiosname,ntdomain = args[1:3]
		
		sc = sambacontroller.SambaController()
		res = sc.add_machine(netbiosname,ntdomain)
		if res==-1:
			print 'The domain "%s" does not reside on this server' % ntdomain
