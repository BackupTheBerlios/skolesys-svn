import os.path
from ConfigParser import ConfigParser
if os.path.exists('./lin4schools.conf'):
	conf = ConfigParser()
	conf.readfp(open('./lin4schools.conf'))
	
elif os.path.exists('/etc/lin4schools.conf'):
	conf = ConfigParser()
	conf.readfp(open('/etc/lin4schools.conf'))
else:
	print "lin4schools.conf could be read"

