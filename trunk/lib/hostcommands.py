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
	
	commands = {
		'hostadd': 'Register a new host to the network',
		'hostinfo': 'List the registered information of a host',
		'listhosts': 'List registered hosts'}

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
			
		while not options.hosttype or not hostmanager.check_hosttype_text(options.hosttype):
			options.hosttype = raw_input("Input the host type (ltspserver,ltspclient,workstation): ")
		hosttype_id = hostmanager.check_hosttype_text(options.hosttype)
		
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
			hwaddr = hostmanager.check_hwaddr(options.hwaddr)
			if not hwaddr:
				print 'The hwaddr: "%s" is not valid.' % options.hwaddr
				exit(0)
			hinfo = hm.host_info(hwaddr=hwaddr)
			matchtype = 'hwaddr'
			matchstring = hwaddr
			
		elif options.hostname:
			hostname = hostmanager.check_hostname(options.hostname)
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
			print "%-20s   %-15s   %-17s   %-20s" % ('Hostname','IPaddress','HWaddress','Hosttype')
		print "%-20s   %-15s   %-17s   %-20s" % (hinfo['hostName'][0],hinfo['ipHostNumber'][0],hinfo['macAddress'][0],hinfo['hostType'][0])
			
		
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
			hosttype_id = hostmanager.check_hosttype_text(options.hosttype)
			if not hosttype_id:
				print 'The host type: "%s" is not valid.' % options.hosttype
				
		hm = hostmanager.HostManager()
		hlist = hm.list_hosts(hosttype_id)
		if not hlist or not len(hlist):
			print "No hosts seem to be registered"
		
		if not options.noheader:
			print "%-20s   %-15s   %-17s   %-20s" % ('Hostname','IPaddress','HWaddress','Hosttype')
		for hinfo in hlist:
			print "%-20s   %-15s   %-17s   %-20s" % (hinfo['hostName'][0],hinfo['ipHostNumber'][0],hinfo['macAddress'][0],hinfo['hostType'][0])

		