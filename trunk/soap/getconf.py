import skolesys.soap.client as ss_client
import os
from skolesys.tools.confhelper import conf2dict

soapconf = None
if os.path.exists('./skolesoap.conf'):
	conf2dict('./skolesoap.conf')
elif os.path.exists('/etc/skolesys/skolesoap.conf'):
	conf2dict('/etc/skolesys/skolesoap.conf')
else:
        print "skolesoap.conf could be read"

if soapconf:
	print soapconf.items('SOAP_CLIENT')

if not os.path.exists('/etc/skolesys'):
	os.makedirs('/etc/skolesys')
if os.path.exists('/etc/skolesys/conf.tgz'):
	os.system('rm /etc/skolesys/conf.tgz')


#c=ss_client.SkoleSYS_Client()