#!/usr/bin/python
from sys import exit,argv
import os
# Check root privilegdes
if not os.getuid()==0:
	print "This command requires root priviledges"
	exit(0)
	
from stat import S_IRUSR,S_IWUSR,S_IRGRP,S_IROTH
import skolesys.soap.client as ss_client
import time,getpass
from optparse import OptionParser
from skolesys.tools.confhelper import conf2dict

parser = OptionParser()
shell_cmd_name = os.path.split(argv[0])[-1:][0]
parser.set_usage("usage: %s [options]" % shell_cmd_name)
parser.add_option("-c", "--config-context", dest="config_context",default=None,
			help="Retrieve a specialized configuration for a given event or context", metavar="CONFCONTEXT")

(options, args) = parser.parse_args()

soapconf = None
if os.path.exists('./skolesoap.conf'):
	soapconf = conf2dict('./skolesoap.conf')
elif os.path.exists('/etc/skolesys/skolesoap.conf'):
	soapconf = conf2dict('/etc/skolesys/skolesoap.conf')
else:
        print "skolesoap.conf could be read"

server_url = None
portnum = None
if soapconf:
	if soapconf['soap_client'].has_key('server_url'):
		server_url = soapconf['soap_client']['server_url']
	
	if soapconf['soap_client'].has_key('port'):
		portnum = soapconf['soap_client']['port']

if not server_url:
	server_url = raw_input('Mainserver url [https://mainserver.skolesys.local]: ')
	if server_url == '':
		server_url = 'https://mainserver.skolesys.local'
	
if not portnum:
	portnum = raw_input('Mainserver port [8443]: ')
	if portnum == '':
		portnum = 8443
else:
	portnum = int(portnum)

if not os.path.exists('/etc/skolesys'):
	os.makedirs('/etc/skolesys')
if os.path.exists('/etc/skolesys/conf.tgz'):
	os.system('rm /etc/skolesys/conf.tgz')

c=ss_client.SkoleSYS_Client(server_url,portnum)
print
context_only = False
if options.config_context:
	context_only = True
if options.config_context == 'update-hosts' and context_only:
	pass
else:
	passwd = getpass.getpass('Mainserver admin password: ')
	if not c.bind(passwd):
		print "Wrong password"
	else:
		print "Authentication OK"

print "Fetching host configuration...",
res = c.getconf(None,options.config_context,context_only)

# Handle errors
if res[0] == -1:
	print "This host has not been registered. Only registered hosts can ask for configuration (use ss_reghost)"
	exit(-1)
	
if res[0] == -2:
	print "The host is registered with an invalid host type id"
	exit(-2)
	
# OK!
if res[0] == 1:
	print "OK"
	if not soapconf:
		print "Storing the connection info in /etc/skolesys/skolesoap.conf"
		f = open('/etc/skolesys/skolesoap.conf','w')
		f.write("[SOAP_CLIENT]\n")
		f.write("server_url\t= %s\n" % server_url)
		f.write("port\t= %s\n" % portnum)
		f.close()
		os.chmod('/etc/skolesys/skolesoap.conf',S_IRUSR|S_IWUSR|S_IRGRP|S_IROTH)
	timestamp = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
	confdir = '/etc/skolesys/%s' % timestamp
	os.makedirs(confdir)
	print "Writing configuration scripts to %s" % confdir
	f=open('%s/conf.tgz' % confdir, 'wb')
	f.write(res[1])
	f.close()
	curdir = os.getcwd()
	os.chdir(confdir)
	os.system('tar xzpf conf.tgz')
	
	print "========== Start configuration process ==========="
	
	res = os.system('./install.sh')
	if not res==0:
		print "The configuration process failed to complete"
		exit (1)
		
	print "========== Configuration process ended ==========="
	
	print "No problems reported."
	os.chdir(curdir)
	os.system('rm %s/conf.tgz -f' % confdir)
	
	exit(0)

exit(1) # undetermined



