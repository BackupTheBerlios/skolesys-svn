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

from sys import exit,argv
import os
	
from stat import S_IRUSR,S_IWUSR,S_IRGRP,S_IROTH
import skolesys.soap.client as ss_client
import getpass
from skolesys.tools.confhelper import conf2dict
from optparse import OptionParser
import skolesys.definitions.hostdef as hostdef

if __name__=='__main__':
	# Check root privilegdes
	if not os.getuid()==0:
		print "This command requires root priviledges"
		exit(1)
	
	soapconf = None
	if os.path.exists('./skolesoap.conf'):
		soapconf = conf2dict('./skolesoap.conf')
	elif os.path.exists('/etc/skolesys/skolesoap.conf'):
		soapconf = conf2dict('/etc/skolesys/skolesoap.conf')
	else:
		print "skolesoap.conf could not be read."
	
	server_url = None
	portnum = None
	if soapconf:
		if soapconf['soap_client'].has_key('server_url'):
			server_url = soapconf['soap_client']['server_url']
		
		if soapconf['soap_client'].has_key('port'):
			portnum = soapconf['soap_client']['port']
	
	parser = OptionParser()
	shell_cmd_name = os.path.split(argv[0])[-1:][0]
	parser.set_usage("usage: %s [options]" % shell_cmd_name)
	parser.add_option("-u", "--soap-url", dest="server_url",default=None,
				help="The url of the mainserver SOAP service", metavar="SERVERURL")
	parser.add_option("-p", "--port-number", dest="portnum",default=None,
				help="The port number of the mainserver SOAP service", metavar="PORTNUM")
	parser.add_option("-n", "--hostname", dest="hostname",default=None,
				help="The hostname of the host being registered", metavar="HOSTNAME")
	parser.add_option("-t", "--hosttype", dest="hosttype",default=None,
				help="The host's host type (mainserver,ltspserver,workstation or ltspclient)", metavar="HOSTTYPE")
	parser.add_option("-r", "--remove",
		action="store_true", dest="remove", default=False,
		help="Remove the entry if one already exists for this host")

	(options, args) = parser.parse_args()
			
	if options.server_url:
		server_url = options.server_url
	
	if options.portnum:
		portnum = options.portnum
	
	if not server_url:
		server_url = raw_input('Mainserver SOAP url [https://mainserver.localnet]: ')
		if server_url == '':
			server_url = 'https://mainserver.localnet'
		
	if not portnum:
		portnum = raw_input('Mainserver SOAP port [10033]: ')
		if portnum == '':
			portnum = 10033
	else:
		portnum = int(portnum)
	
	
	if options.hostname:
		options.hostname = hostdef.check_hostname(options.hostname)
	while not options.hostname:
		input_hostname = raw_input("Input the hostname for the host being assigned: ")
		options.hostname = hostdef.check_hostname(input_hostname)
		if not options.hostname:
			print '"%s" is not a valid hostname. Use only letters and numbers.' % input_hostname
	
	hosttype_id = None
	if options.hosttype:
		hosttype_id = hostdef.hosttype_as_text(options.hosttype)
	while not hosttype_id:
		input_hosttype = raw_input("Input the host type (mainserver,ltspserver,workstation or ltspclient): ")
		hosttype_id = hostdef.hosttype_as_text(input_hosttype)
		if not hosttype_id:
			print '"%s" is not a valid host type.' % input_hosttype
	
	if not os.path.exists('/etc/skolesys'):
		os.makedirs('/etc/skolesys')
	if os.path.exists('/etc/skolesys/conf.tgz'):
		os.system('rm /etc/skolesys/conf.tgz')
	
	c=ss_client.SkoleSYS_Client(server_url,portnum)
	print
	username = raw_input('Username: ')
	passwd = getpass.getpass('Password: ')
	if not c.bind(username,passwd):
		print "Wrong password"
	else:
		print "Authentication OK"
		if not soapconf:
			print "Storing the connection info in /etc/skolesys/skolesoap.conf"
			f = open('/etc/skolesys/skolesoap.conf','w')
			f.write("[SOAP_CLIENT]\n")
			f.write("server_url\t= %s\n" % server_url)
			f.write("port\t= %s\n" % portnum)
			f.close()
			os.chmod('/etc/skolesys/skolesoap.conf',S_IRUSR|S_IWUSR|S_IRGRP|S_IROTH)
	
	if options.remove and c.is_registered(hwaddr=c.hwaddr):
		c.remove_host(hwaddr=c.hwaddr)

	print "Registering the host...",
	res = c.register_host(options.hostname,hosttype_id)
	
	# Handle errors
	if res==-5:
		print "The host's hwaddr [%s] has already been registered" % c.hwaddr
		exit(-5)
	
	if res==-6:
		print 'The hostname "%s" has already been registered' % options.hostname
		exit(-6)
	
	# OK!
	print "OK"
	exit(0)
