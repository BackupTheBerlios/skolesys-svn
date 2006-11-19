#!/usr/bin/python

#!/usr/bin/python
import skolesys.tools.mkpasswd as pw
import getpass,os,time,re,sys
import inspect
import skolesys.cfmachine.apthelpers as apthelper
from optparse import OptionParser

# Check root privilegdes
if not os.getuid()==0:
        print "This command requires root priviledges"
        sys.exit(0)

shell_cmd_name = os.path.split(sys.argv[0])[-1:][0]
parser = OptionParser(usage="usage: %s [options]" % (shell_cmd_name))
parser.add_option("-t", "--client-type", dest="clienttype",default='',
			help="The type og SkoleSYS client to be seeded (workstation,ltspserver)", metavar="CLIENTTYPE")
(options, args) = parser.parse_args()

os.system('clear')

types = ['workstation','ltspserver']

if not types.count(options.clienttype):
	print "What type of client do you wish to seed"
	print "---------------------------------------"
	while not types.count(options.clienttype):
		options.clienttype = raw_input('Client type (%s): ' % ','.join(types)).lower()
	print
	print
	
print "To create a SkoleSYS %s you must register the host with the mainserver" % options.clienttype
print "-------------------------------------------------------------------------------"

hostname = raw_input('%s hostname: ' % options.clienttype)

res = os.system('ss_reghost -n %s -t %s' % (hostname,options.clienttype))
if res<>0:
	sys.exit(1)

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

