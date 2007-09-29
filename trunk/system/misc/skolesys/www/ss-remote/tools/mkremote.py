#!/usr/bin/python

import zipfile,os,sys,pwd
from skolesys.lib.conf import conf

def mk_user_ss_remote(username):

	publish_dir = '/skolesys/www/ss-remote/userclients/%s/win32' % username
	if not os.path.exists(publish_dir):
		os.makedirs(publish_dir)		

	try:
		linux_home_path = pwd.getpwnam(username)[5]
	except:
		print 'User "%s" does not exist or has no homedir' % username
		sys.exit(1)

	domain_name = conf.get('DOMAIN','domain_name')
	host = "%s.skolesys.dk" % domain_name.split('.')[0]
	remote_host = conf.get('TERMINAL_SERVICE','freenx')
	f=open('%s/hostinfo.conf' % publish_dir,'w')
	f.write("""[HOSTINFO]

host = %s
remote_host = %s
remote_port = 22

local_port = 10000
""" % (host,remote_host))
	f.close()

	if os.path.exists('/skolesys/www/ss-remote/win32/ss-remote.exe'):
	
		if not os.path.exists('%s/.ssh/id_dsa'%linux_home_path):
			print 'User "%s" has no keyfile "%s/.ssh/id_dsa"' % (username,linux_home_path)
			sys.exit(1)

		os.system('cp /skolesys/www/ss-remote/win32/ss-remote.exe %s/' % publish_dir)

		zf = zipfile.ZipFile('%s/ss-remote.exe' % publish_dir ,'a')
		zf.write('%s/hostinfo.conf' % publish_dir,'dist/hostinfo.conf')
		zf.write('%s/.ssh/id_dsa'%linux_home_path,'dist/id_dsa')
		zf.close()

		w,r = os.popen2('zip -z %s/ss-remote.exe' % publish_dir)
		w.write(""";The comment below contains SFX script commands
Setup=start.vbs
TempMode
Overwrite=1
""")
		w.close()
		r.close()

		os.system('chown www-data.www-data %s -R' % publish_dir)

if __name__=='__main__':
	if len(sys.argv)<2:
		print "usage: %s username" % sys.argv[0]
		sys.exit(1)

	mk_user_ss_remote(sys.argv[1])
