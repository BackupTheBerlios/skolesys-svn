#!/usr/bin/python

import re,grp,os,ldap
from sys import argv,exit

# Check root privilegdes
if not os.getuid()==0:
	print "This command needs requires priviledges"
	exit(0)
	
	
from optparse import OptionParser
from conf import conf
import hostmanager


if __name__=='__main__':
	
	commands = {'hostadd': 'Register a new host to the network'}

	shell_cmd_name = os.path.split(argv[0])[-1:][0]
	
	usage = "usage: %s [command] [options] arg1, arg2" % shell_cmd_name
	if len(argv)<2 or not commands.has_key(argv[1]):
		print usage
		print 
		print "Commands:"
		for cmd,desc in commands.items():
			print '%s - %s' % (cmd,desc)
		exit(0)
		
	cmd = argv[1]
	
	parser = OptionParser(usage=usage)

	if cmd == "hostadd":
		parser.set_usage("usage: %s %s hostname " % (shell_cmd_name,cmd))
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
		
		hostname = hostmanager.check_hostname(args[1])
		if not hostname:
			print "The entered hostname is invalid"
			exit(0)
			
		# Check if this hostname is already registered
		hm = hostmanager.HostManager()
		if hm.host_exists(hostname=hostname):
			print 'The hostname: "%s" has already been registered use hostmod instead' % hostname
			exit(0)
		
		if options.ipaddr:
			ipchk = hostmanager.check_ipaddr(options.ipaddr)
			if not ipchk:
				print 'The ipaddress: "%s" entered is not valid' % options.ipaddr
				exit(0)
				
		print "Hostname: %s" % hostname
		
		while not options.hwaddr or not hostmanager.check_hwaddr(options.hwaddr):
			options.hwaddr = raw_input("Input the hardware address of the host's network interface (mac-address): ")
		options.hwaddr = hostmanager.check_hwaddr(options.hwaddr)
			
		
		# Check if this hwaddr is already registered
		if hm.host_exists(hwaddr=options.hwaddr):
			print 'The hwaddr: "%s" has already been registered use hostmod instead' % options.hwaddr
			exit(0)
			
		while not options.hosttype or not hostmanager.check_hosttype(options.hosttype):
			options.hosttype = raw_input("Input the host type (ltspserver,workstation): ")
		
		
		try:
			hostadd_res = hm.registerHost(options.hwaddr,hostname,options.hosttype,options.ipaddr)
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
		
		print "Host registered..."
