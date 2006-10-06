#!/usr/bin/python
from sys import exit
import os
# Check root privilegdes
if not os.getuid()==0:
	print "This command needs requires priviledges"
	exit(0)
	
import skolesys.soap.client as ss_client
import time,getpass
from skolesys.tools.confhelper import conf2dict


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
passwd = getpass.getpass('Mainserver admin password: ')
if not c.bind(passwd):
	print "Wrong password"
else:
	print "Authentication OK"

print "Fetching host configuration...",
res = c.getconf()

# Handle errors
if res[0] == -1:
	print "Only registered hosts can ask for configuration"
	exit(0)
	
if res[0] == -2:
	print "The host is registered with an invalid host type id"
	exit(0)
	
# OK!
if res[0] == 1:
	print "OK"
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
	os.system('./install.sh')
	print "========== Configuration process ended ==========="
	print "No problems reported."
	os.chdir(curdir)
	os.system('rm %s/conf.tgz -f' % confdir)
	



