apt_source_entries = [
	{'type':'deb','uri':'http://archive.skolesys.dk/$[conf.cfmachine.package_group]','distribution':'feisty','components':['main']},
        {'type':'deb','uri':'http://archive.ubuntu.com/ubuntu/','distribution':'feisty','components':['main','restricted','universe']},
        {'type':'deb-src','uri':'http://archive.ubuntu.com/ubuntu/','distribution':'feisty','components':['main','restricted','universe']},
        {'type':'deb','uri':'http://archive.ubuntu.com/ubuntu/','distribution':'feisty-backports','components':['main','restricted','universe','multiverse']},
        {'type':'deb-src','uri':'http://archive.ubuntu.com/ubuntu/','distribution':'feisty-backports','components':['main','restricted','universe','multiverse']},
        {'type':'deb','uri':'http://security.ubuntu.com/ubuntu','distribution':'feisty-security','components':['main','restricted','universe']},
        {'type':'deb-src','uri':'http://security.ubuntu.com/ubuntu','distribution':'feisty-security','components':['main','restricted','universe']}]

fstab_entries = [
	{'sourcefs':'mainserver.localnet:/skolesys','mountpoint':'/skolesys','fstype':'nfs','options':'defaults','dump':'0','fsckorder':'0'}]
	
packagelist_files = [
	'default-packages','custom-packages']

copy_files_rootdir = \
	'rootdir'

hostname = \
	'$reciever.hostName'

kick_daemons = [
	'/etc/init.d/networking restart',
	'/etc/init.d/dhcp3-server restart',
	'/etc/init.d/nfs-kernel-server restart',
	'/etc/init.d/nfs-common restart',
	'/etc/init.d/tftpd-hpa restart']
