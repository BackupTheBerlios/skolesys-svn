#!/usr/bin/python

# This file is part of the SkoleSYS libraries
# Copyright (C) 2007 Jakob Simon-Gaarde <info at skolesys.dk>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License version 2 as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public License
# along with this library; see the file COPYING.LIB.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301, USA.

def init_mainserver():
	import skolesys.tools.mkpasswd as pw
	import getpass,os,time,re,sys
	import inspect,shutil
	import skolesys
	import skolesys.cfmachine.apthelpers as apthelper
	import skolesys.tools.sysinfo as sysinfo

	# Check root privilegdes
	if not os.getuid()==0:
		print "This command requires root priviledges"
		sys.exit(1)
	
	os.system('clear')
	location = os.path.split(inspect.getfile(skolesys))[0]
	
	print "SkoleSYS administrator login"
	print "----------------------------"
	in_adminpw = getpass.getpass('Enter the ldap skolesys.org admin passwd: ')
	if in_adminpw != getpass.getpass('Verify the ldap skolesys.org admin passwd: '):
		print "The passwords entered did not match"
		sys.exit(1)
	
	print
	print "The school administrator login"
	print "------------------------------"
	in_schooladminpw = getpass.getpass('Enter the ldap school admin passwd: ')
	if in_schooladminpw != getpass.getpass('Verify the ldap school admin passwd: '):
		print "The passwords entered did not match"
		sys.exit(1)
	
	
	print
	print "School domain setup"
	print "-------------------"
	
	organization_name = raw_input("What is the name of the school: ")
	print 
	
	domain_name = raw_input("What is the school's domain name (ex. riggshigh.co.uk): ")
	domain_name_prefix = domain_name.split('.')[0]
	
	print
	country_code = raw_input("What is the country code of servers location (ex. dk=Denmark, uk=United Kingdom): ")
	
	print
	province = raw_input("Province or state (free text no constraints): ")
	
	print
	lang = raw_input("What should be the default language (ex. da=danish, en=english): ")
	
	
	
	# Create certificate and master ssh keypair
	
	f = open('%s/seeder/cert.cnf_template' % location )
	cert_cnf_lines = f.readlines()
	f.close()
	
	f = open('cert.cnf','w')
	for l in cert_cnf_lines:
		l = l.replace('<domain_name>',domain_name)
		l = l.replace('<lang>',lang)
		l = l.replace('<country_code>',country_code)
		l = l.replace('<province>',province)
		l = l.replace('<organization_name>','skolesys')
		l = l.replace('<organization_unit_name>',organization_name)
		l = l.replace('<common_name>',organization_name)
		l = l.replace('<country_code>',country_code)
		f.write(l)
	f.close()	
	
	res = os.system('openssl req -new -passin pass:%s -passout pass:%s -config cert.cnf > new.cert.csr' % (in_schooladminpw,in_schooladminpw))
	if not res==0:
		print
		print "SkoleSYS Seeder - failed while creating the SOAP certificate files"
		sys.exit(1)
		
	res = os.system('openssl rsa -in privkey.pem -passin pass:%s -out %s.key' % (in_schooladminpw,domain_name))
	if not res==0:
		print
		print "SkoleSYS Seeder - failed while creating the SOAP certificate files"
		sys.exit(1)
	
	res = os.system('openssl x509 -in new.cert.csr -out %s.cert -req -signkey %s.key -days 20000' % (domain_name,domain_name))
	if not res==0:
		print
		print "SkoleSYS Seeder - failed while creating the SOAP certificate files"
		sys.exit(1)
	
	# Copy certificate into place
	if not os.path.exists('/etc/skolesys/cert/'):
		os.makedirs('/etc/skolesys/cert/')
	res = os.system('cp %s.key %s.cert /etc/skolesys/cert/' % (domain_name,domain_name))
	if not res==0:
		print
		print "SkoleSYS Seeder - failed while copying certificate into place"
		sys.exit(1)
	
	# Create the master ssh keypair
	if not os.path.exists('/etc/skolesys/ssh/'):
		os.makedirs('/etc/skolesys/ssh/')	
	res = os.system('ssh-keygen -b 1024 -t dsa -N "" -f /etc/skolesys/ssh/id_dsa')
	if not res==0:
		print
		print "SkoleSYS Seeder - failed while creating the master ssh keypair"
		sys.exit(1)

	

	# Read template files before they are removed
	f = open('%s/seeder/slapd.conf_template' % location)
	slapd_conf_lines = f.readlines()
	f.close()
	
	f = open('%s/seeder/skolesys.ldif_template' % location)
	skolesys_ldif_lines = f.readlines()
	f.close()
	
	
	# INSTALL
	
	# Wipe sources.list on mainserver install
	os.system('echo "" > /etc/apt/sources.list')
	
	# fetch the release codename
	codename = sysinfo.get_dist_codename()
	
	# ensure some entries in sources.list
	apt_source_entries = [
		{'type':'deb','uri':'http://archive.skolesys.dk/stable','distribution':codename,'components':['main']},
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
			sys.exit(1)
	
	# Better read the skolesys.conf template file since the mainserver package will remove it next
	f = open('%s/seeder/skolesys.conf_template' % location)
	lines = f.readlines()
	f.close()

	f = open('/etc/skolesys/skolesys.conf','w')
	for l in lines:
		l = l.replace('<domain_name>',domain_name)
		l = l.replace('<domain_name_prefix>',domain_name_prefix)
		l = l.replace('<uc_domain_name_prefix>', domain_name_prefix.upper())
		l = l.replace('<lang>',lang)
		f.write(l)
	f.close()
	os.system('chmod 644 /etc/skolesys/skolesys.conf')
	
	# Replace python-skolesys-seeder with python-skolesys-mainserver
	os.environ['DEBIAN_FRONTEND'] = 'noninteractive'
	os.environ['DEBCONF_ADMIN_EMAIL'] = ''
	
	res = os.system('apt-get install -y slapd')
	if not res==0:
		print
		print "SkoleSYS Seeder - failed while installing LDAP server"
		sys.exit(1)
	
	res = os.system('apt-get install -y ldap-utils')
	if not res==0:
		print
		print "SkoleSYS Seeder - failed while installing LDAP utils"
		sys.exit(1)

	shutil.copy('%s/seeder/skolesys.schema' % location,'/etc/ldap/schema/')
	shutil.copy('%s/seeder/samba.schema' % location,'/etc/ldap/schema/')
	
	if not os.path.exists('/skolesys/misc_backup'):
		os.makedirs('/skolesys/misc_backup')

	if not os.path.exists('/skolesys/%s/groups' % domain_name):
		os.makedirs('/skolesys/%s/groups' % domain_name)
	if not os.path.exists('/skolesys/%s/users' % domain_name):
		os.makedirs('/skolesys/%s/users' % domain_name)
	if not os.path.exists('/skolesys/%s/profiles' % domain_name):
		os.makedirs('/skolesys/%s/profiles' % domain_name)
	if not os.path.exists('/skolesys/%s/services' % domain_name):
		os.makedirs('/skolesys/%s/services' % domain_name)
	if not os.path.exists('/skolesys/%s/smbshares' % domain_name):
		os.makedirs('/skolesys/%s/smbshares' % domain_name)

	from skolesys.lib.conf import conf
	conf.set('LDAPSERVER','passwd',in_adminpw)
	
	res = os.system('/etc/init.d/slapd stop')
	if not res==0:
		print
		print "SkoleSYS Seeder - failed while stopping the LDAP Server"
		sys.exit(1)
	os.system('rm /var/lib/ldap/* -R -f')
	
	f = open('/etc/ldap/slapd.conf','w')
	for l in slapd_conf_lines:
		l = l.replace('<basedn>',conf.get('LDAPSERVER','basedn'))
		l = l.replace('<passwd>',pw.mkpasswd(in_adminpw,3,'ssha').strip())
		l = l.replace('<admin>',conf.get('LDAPSERVER','admin'))
		f.write(l)
	f.close()
	os.system('chmod 600 /etc/ldap/slapd.conf')
	
	# ldif fore initializing ldap
	f = open('skolesys.ldif','w')
	c = re.compile('(ou=(\S+))')
	
	def fetch_conf_ou(ou,conf):
		try:
			return c.match(conf.get('LDAPSERVER','%s_ou' % ou)).groups()
		except:
			print "skolesys.conf needs the required variable '%s_ou' to be set." % ou
			sys.exit(1)
	
	groups_ou,groups = fetch_conf_ou('groups',conf)
	logins_ou,logins = fetch_conf_ou('logins',conf)
	teachers_ou,teachers = fetch_conf_ou('teachers',conf)
	students_ou,students = fetch_conf_ou('students',conf)
	parents_ou,parents = fetch_conf_ou('parents',conf)
	others_ou,others = fetch_conf_ou('others',conf)
	primary_ou,primary = fetch_conf_ou('primary',conf)
	system_ou,system = fetch_conf_ou('system',conf)
	service_ou,service = fetch_conf_ou('service',conf)
	samba_ou,samba = fetch_conf_ou('samba',conf)
	smb_users_ou,smb_users = fetch_conf_ou('smb_users',conf)
	smb_machines_ou,smb_machines = fetch_conf_ou('smb_machines',conf)
	smb_groups_ou,smb_groups = fetch_conf_ou('smb_groups',conf)
	hosts_ou,hosts = fetch_conf_ou('hosts',conf)
	
	domain_name_prefix = conf.get('DOMAIN','domain_name').split('.')[0]
	
	for l in skolesys_ldif_lines:
		l = l.replace('<basedn>',conf.get('LDAPSERVER','basedn'))
		l = l.replace('<groups_ou>',groups_ou)
		l = l.replace('<logins_ou>',logins_ou)
		l = l.replace('<teachers_ou>',teachers_ou)
		l = l.replace('<students_ou>',students_ou)
		l = l.replace('<parents_ou>',parents_ou)
		l = l.replace('<others_ou>',others_ou)
		l = l.replace('<primary_ou>',primary_ou)
		l = l.replace('<system_ou>',system_ou)
		l = l.replace('<service_ou>',service_ou)
		l = l.replace('<samba_ou>',samba_ou)
		l = l.replace('<smb_users_ou>',smb_users_ou)
		l = l.replace('<smb_machines_ou>',smb_machines_ou)
		l = l.replace('<smb_groups_ou>',smb_groups_ou)
		l = l.replace('<hosts_ou>',hosts_ou)
		l = l.replace('<groups>',groups)
		l = l.replace('<logins>',logins)
		l = l.replace('<teachers>',teachers)
		l = l.replace('<students>',students)
		l = l.replace('<parents>',parents)
		l = l.replace('<others>',others)
		l = l.replace('<primary>',primary)
		l = l.replace('<system>',system)
		l = l.replace('<service>',service)
		l = l.replace('<samba>',samba)
		l = l.replace('<smb_users>',smb_users)
		l = l.replace('<smb_machines>',smb_machines)
		l = l.replace('<smb_groups>',smb_groups)
		l = l.replace('<hosts>',hosts)
		l = l.replace('<domain_name>',conf.get('DOMAIN','domain_name'))
		l = l.replace('<domain_name_prefix>',domain_name_prefix)
		l = l.replace('<passwd>',pw.mkpasswd(in_adminpw,3,'crypt').strip())
		l = l.replace('<schooladmin_passwd>',pw.mkpasswd(in_schooladminpw,3,'crypt').strip())
		f.write(l)
	f.close()
	
	res = os.system('/etc/init.d/slapd restart')
	if not res==0:
		print
		print "SkoleSYS Seeder - failed while restarting the LDAP Server"
		sys.exit(1)
		
	print "Sleeping 5 seconds to ensure slapd restart..."
	time.sleep(5)
	res = os.system('ldapadd -x -D "cn=admin,dc=skolesys,dc=org" -w %s -f skolesys.ldif' % in_adminpw)
	if not res==0:
		print
		print "SkoleSYS Seeder - failed while adding creating LDAP server structure"
		sys.exit(1)
	
	res = os.system('rm skolesys.ldif -f')

	f = open('/etc/hosts','a')
	f.write('127.0.0.1\tmainserver.localnet\n')
	f.close()
	
	res = os.system('apt-get install -y python-skolesys-mainserver')
	if not res==0:
		print
		print "SkoleSYS Seeder - failed while installing SkoleSYS mainserver package"
		sys.exit(1)

	
	import skolesys.lib.hostmanager as h
	import skolesys.definitions.hostdef as hostdef
	import skolesys.soap.netinfo as netinfo
	hm = h.HostManager()
	print hm.register_host(netinfo.if2hwaddr('eth0'),'mainserver',hostdef.hosttype_as_id('mainserver'),update_hosts=False)
	
	import skolesys.cfmachine.configbuilder as confbuilder
	cb = confbuilder.ConfigBuilder(hostdef.hosttype_as_id('mainserver'),codename,netinfo.if2hwaddr('eth0'),'seed-mainserver')
	curdir = os.getcwd()
	os.chdir(cb.tempdir)
	res = os.system('./install.sh')
	if not res==0:
		print
		print "SkoleSYS Seeder - failed while fetching the configuration"
		sys.exit(1)
	
	os.chdir(curdir)
	del cb
	
	res = os.system('smbpasswd -w %s' % in_schooladminpw)
	if not res==0:
		print
		print "SkoleSYS Seeder - failed while storing LDAP password for samba"
		sys.exit(1)
	
	res = os.system('/etc/init.d/samba restart')
	if not res==0:
		print
		print "SkoleSYS Seeder - faield to restart samba"
		sys.exit(1)
	
	res = os.system('useradd smbadmin')
	if not res==0:
		print
		print "SkoleSYS Seeder - failed while adding user smbadmin"
		sys.exit(1)
	
	w,r = os.popen2('smbpasswd -a smbadmin -s')
	w.write('%s\n' % in_schooladminpw)
	w.write('%s\n' % in_schooladminpw)
	w.close()
	r.close()
	
	print "Done configuring the mainserver."
	
	print "Add system groups..."
	
	os.system('ss_groupmanager creategroup fuse -t primary -n USB')
	
