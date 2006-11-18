#!/usr/bin/python

#!/usr/bin/python
import skolesys.tools.mkpasswd as pw
import getpass,os,time,re,sys
import inspect
import skolesys.cfmachine.apthelpers as apthelper

# Check root privilegdes
if not os.getuid()==0:
        print "This command requires root priviledges"
        sys.exit(1)

os.system('clear')

print "To create a SkoleSYS workstation you must register the host with the mainserver"
print "-------------------------------------------------------------------------------"

hostname = raw_input('Workstation hostname: ')

res = os.system('ss_reghost -n %s -t workstation' % hostname)
if res<>0:
	sys.exit(1)
print 
print res

# INSTALL

# Wipe sources.list on mainserver install
os.system('echo "" > /etc/apt/sources.list')

# ensure some entries in sources.list
apt_source_entries = [
        {'type':'deb','uri':'http://skolesys.dk/testing','distribution':'pilot','components':['main','nonfree']},
        {'type':'deb','uri':'http://archive.ubuntu.com/ubuntu/','distribution':'dapper','components':['main','restricted','universe']},
        {'type':'deb-src','uri':'http://archive.ubuntu.com/ubuntu/','distribution':'dapper','components':['main','restricted','universe']},
        {'type':'deb','uri':'http://archive.ubuntu.com/ubuntu/','distribution':'dapper-backports','components':['main','restricted','universe','multiverse']},
        {'type':'deb-src','uri':'http://archive.ubuntu.com/ubuntu/','distribution':'dapper-backports','components':['main','restricted','universe','multiverse']},
        {'type':'deb','uri':'http://security.ubuntu.com/ubuntu','distribution':'dapper-security','components':['main','restricted','universe']},
        {'type':'deb-src','uri':'http://security.ubuntu.com/ubuntu','distribution':'dapper-security','components':['main','restricted','universe']}]

slist = apthelper.SourcesList()
for src in apt_source_entries:
	slist.add_source(src['type'],src['uri'],src['distribution'],src['components'])
slist.print_sources_list()
if slist.dirty:
	slist.write_sources_list()
	res = os.system('apt-get update')
	if not res==0:
		print
		print "SkoleSYS Seeder - failed while updating packages"
		sys.exit(1)


# Replace python-skolesys-seeder with python-skolesys-mainserver
os.environ['DEBIAN_FRONTEND'] = 'noninteractive'
os.environ['DEBCONF_ADMIN_EMAIL'] = ''

os.system('ss_getconf')

