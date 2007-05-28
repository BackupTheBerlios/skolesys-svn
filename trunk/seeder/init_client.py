#!/usr/bin/python

import skolesys.tools.mkpasswd as pw
import getpass,os,time,re,sys
import inspect
import skolesys.cfmachine.apthelpers as apthelper
from optparse import OptionParser

def init_client(clienttype,hostname=None):
	# Check root privilegdes
	if not os.getuid()==0:
		print "This command requires root priviledges"
		return 1
	
	if not hostname:
		os.system('clear')
		print "To create a SkoleSYS %s you must register the host with the mainserver" % clienttype
		print "-------------------------------------------------------------------------------"
		hostname = raw_input('%s hostname: ' % clienttype)
	
	# INSTALL
	
	# Wipe sources.list on mainserver install
	os.system('echo "" > /etc/apt/sources.list')
	
	# fetch the release codename
	w,r = os.popen2('lsb_release -cs')
	codename = r.readline().strip()
	r.close()
	w.close()

	# ensure some entries in sources.list
	apt_source_entries = [
		{'type':'deb','uri':'http://archive.skolesys.dk/release','distribution':codename,'components':['main','nonfree']},
		{'type':'deb','uri':'http://archive.ubuntu.com/ubuntu/','distribution':codename,'components':['main','restricted','universe']},
		{'type':'deb-src','uri':'http://archive.ubuntu.com/ubuntu/','distribution':codename,'components':['main','restricted','universe']},
		{'type':'deb','uri':'http://archive.ubuntu.com/ubuntu/','distribution':'%s-backports' % codename ,'components':['main','restricted','universe','multiverse']},
		{'type':'deb-src','uri':'http://archive.ubuntu.com/ubuntu/','distribution':'%s-backports' % codename,'components':['main','restricted','universe','multiverse']},
		{'type':'deb','uri':'http://archive.ubuntu.com/ubuntu/','distribution':'%s-updates' % codename ,'components':['main','restricted','universe','multiverse']},
		{'type':'deb-src','uri':'http://archive.ubuntu.com/ubuntu/','distribution':'%s-updates' % codename,'components':['main','restricted','universe','multiverse']},
		{'type':'deb','uri':'http://security.ubuntu.com/ubuntu','distribution':'%s-security' % codename,'components':['main','restricted','universe']},
		{'type':'deb-src','uri':'http://security.ubuntu.com/ubuntu','distribution':'%s-security' % codename,'components':['main','restricted','universe']}]
	
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
			return 1
	
	# Replace python-skolesys-seeder with python-skolesys-mainserver
	os.environ['DEBIAN_FRONTEND'] = 'noninteractive'
	os.environ['DEBCONF_ADMIN_EMAIL'] = ''
	
	res = os.system('ss_reghost -n %s -t %s' % (hostname,clienttype))
	if not res==0:
		print
		print "SkoleSYS Seeder - failed while updating packages"
		return 1
	
	res = os.system('ss_getconf')
	if not res==0:
		print
		print "SkoleSYS Seeder - failed while updating packages"
		return 1
	
	


if __name__=='__main__':
	
	# Check root privilegdes
	if not os.getuid()==0:
		print "This command requires root priviledges"
		sys.exit(1)
		
	os.system('clear')
	shell_cmd_name = os.path.split(sys.argv[0])[-1:][0]
	parser = OptionParser(usage="usage: %s [options]" % (shell_cmd_name))
	parser.add_option("-t", "--client-type", dest="clienttype",default='',
				help="The type og SkoleSYS client to be seeded (workstation,ltspserver)", metavar="CLIENTTYPE")
	(options, args) = parser.parse_args()
	
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
	sys.exit(init_client(options.clienttype,hostname))
