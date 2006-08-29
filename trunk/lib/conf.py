import os.path
from ConfigParser import ConfigParser
if os.path.exists('./skolesys.conf'):
	conf = ConfigParser()
	conf.readfp(open('./skolesys.conf'))
	
elif os.path.exists('/etc/skolesys.conf'):
	conf = ConfigParser()
	conf.readfp(open('/etc/skolesys.conf'))
else:
	print "skolesys.conf could be read"

