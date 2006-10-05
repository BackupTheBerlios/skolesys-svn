apt_source_entries = [
	{'type':'deb','uri':'http://mainserver.skolesys.local/debian','distribution':'pilot','components':['main','nonfree']}]

fstab_entries = [
	{'sourcefs':'mainserver.skolesys.local:/skolesys','mountpoint':'/skolesys','fstype':'nfs','options':'defaults','dump':'0','fsckorder':'0'}]
	
packagelist_files = [
	'default-packages','custom-packages']

copy_files_rootdir = \
	['rootdir']

kick_daemons = [
	'/etc/init.d/networking restart',
	'/etc/init.d/nscd restart',
	'/etc/init.d/dhcp3-server restart',
	'/etc/init.d/nfs-kernel-server restart',
	'/etc/init.d/nfs-common restart',
	'/etc/init.d/tftpd-hpa restart']
