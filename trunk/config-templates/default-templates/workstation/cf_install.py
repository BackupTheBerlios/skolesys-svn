apt_source_entries = [
	{'type':'deb','uri':'http://skolesys.dk/testing','distribution':'pilot','components':['main','nonfree']},
        {'type':'deb','uri':'http://archive.ubuntu.com/ubuntu/','distribution':'dapper','components':['main','restricted','universe']},
        {'type':'deb-src','uri':'http://archive.ubuntu.com/ubuntu/','distribution':'dapper','components':['main','restricted','universe']},
        {'type':'deb','uri':'http://archive.ubuntu.com/ubuntu/','distribution':'dapper-backports','components':['main','restricted','universe','multiverse']},
        {'type':'deb-src','uri':'http://archive.ubuntu.com/ubuntu/','distribution':'dapper-backports','components':['main','restricted','universe','multiverse']},
        {'type':'deb','uri':'http://security.ubuntu.com/ubuntu','distribution':'dapper-security','components':['main','restricted','universe']},
        {'type':'deb-src','uri':'http://security.ubuntu.com/ubuntu','distribution':'dapper-security','components':['main','restricted','universe']}]

fstab_entries = [
	{'sourcefs':'mainserver.skolesys.local:/skolesys','mountpoint':'/skolesys','fstype':'nfs','options':'defaults','dump':'0','fsckorder':'0'}]
	
packagelist_files = [
	'default-packages','custom-packages']

copy_files_rootdir = \
	'rootdir'

hostname = \
	'$reciever.hostName'

kick_daemons = [
	'/etc/init.d/networking restart']