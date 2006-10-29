#!/usr/bin/python
import skolesys.tools.mkpasswd as pw
import getpass,os,time,re,sys
import inspect
import skolesys.seeder
import skolesys.cfmachine.apthelpers as apthelper

# Check root privilegdes
if not os.getuid()==0:
        print "This command requires root priviledges"
        sys.exit(0)

os.system('clear')
location = os.path.split(inspect.getsourcefile(skolesys.seeder))[0] 

print "SkoleSYS administrator login"
print "----------------------------"
in_adminpw = getpass.getpass('Enter the ldap skolesys.org admin passwd: ')
if in_adminpw != getpass.getpass('Verify the ldap skolesys.org admin passwd: '):
	print "The passwords entered did not match"
	sys.exit()

print
print "The school administrator login"
print "------------------------------"
in_schooladminpw = getpass.getpass('Enter the ldap school admin passwd: ')
if in_schooladminpw != getpass.getpass('Verify the ldap school admin passwd: '):
	print "The passwords entered did not match"
	sys.exit()


print
print "School domain setup"
print "-------------------"
domain_name = raw_input("What is the school's domain name (ex. riggshigh.co.uk): ")
domain_name_prefix = domain_name.split('.')[0]

# Read template files before they are removed
f = open('%s/slapd.conf_template' % location)
slapd_conf_lines = f.readlines()
f.close()

f = open('%s/skolesys.ldif_template' % location)
skolesys_ldif_lines = f.readlines()
f.close()


# INSTALL
# ensure some entries in sources.list
apt_source_entries = [
        {'type':'deb','uri':'http://skolesys.dk/skolesys/debian','distribution':'pilot','components':['main','nonfree']},
        {'type':'deb','uri':'http://dk.archive.ubuntu.com/ubuntu/','distribution':'dapper','components':['main','restricted','universe']},
        {'type':'deb-src','uri':'http://dk.archive.ubuntu.com/ubuntu/','distribution':'dapper','components':['main','restricted','universe']},
        {'type':'deb','uri':'http://dk.archive.ubuntu.com/ubuntu/','distribution':'dapper-backports','components':['main','restricted','universe','multiverse']},
        {'type':'deb-src','uri':'http://dk.archive.ubuntu.com/ubuntu/','distribution':'dapper-backports','components':['main','restricted','universe','multiverse']},
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

# Better read the skolesys.conf template file since the mainserver package will remove it next
f = open('%s/skolesys.conf_template' % location)
lines = f.readlines()
f.close()

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

res = os.system('apt-get install -y python2.4-skolesys-mainserver')
if not res==0:
	print
	print "SkoleSYS Seeder - failed while installing SkoleSYS mainserver package"
	sys.exit(1)

f = open('/etc/skolesys/skolesys.conf','w')
for l in lines:
        l = l.replace('<domain_name>',domain_name)
        l = l.replace('<domain_name_prefix>',domain_name_prefix)
        l = l.replace('<schooladmin_passwd>',in_schooladminpw)
        f.write(l)
f.close()
os.system('chmod 600 /etc/skolesys/skolesys.conf')

if not os.path.exists('/skolesys/%s/groups' % domain_name):
	os.makedirs('/skolesys/%s/groups' % domain_name)
if not os.path.exists('/skolesys/%s/users' % domain_name):
	os.makedirs('/skolesys/%s/users' % domain_name)

from skolesys.lib.conf import conf

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

def fetch_conf_ou(ou):
	global conf
	try:
		return c.match(conf.get('LDAPSERVER','%s_ou' % ou)).groups()
	except:
		print "skolesys.conf needs the required variable '%s_ou' to be set." % ou
		sys.exit(0)

groups_ou,groups = fetch_conf_ou('groups')
logins_ou,logins = fetch_conf_ou('logins')
teachers_ou,teachers = fetch_conf_ou('teachers')
students_ou,students = fetch_conf_ou('students')
parents_ou,parents = fetch_conf_ou('parents')
others_ou,others = fetch_conf_ou('others')
samba_ou,samba = fetch_conf_ou('samba')
smb_users_ou,smb_users = fetch_conf_ou('smb_users')
smb_machines_ou,smb_machines = fetch_conf_ou('smb_machines')
smb_groups_ou,smb_groups = fetch_conf_ou('smb_groups')
hosts_ou,hosts = fetch_conf_ou('hosts')

domain_name_prefix = conf.get('DOMAIN','domain_name').split('.')[0]

for l in skolesys_ldif_lines:
	l = l.replace('<basedn>',conf.get('LDAPSERVER','basedn'))
	l = l.replace('<groups_ou>',groups_ou)
	l = l.replace('<logins_ou>',logins_ou)
	l = l.replace('<teachers_ou>',teachers_ou)
	l = l.replace('<students_ou>',students_ou)
	l = l.replace('<parents_ou>',parents_ou)
	l = l.replace('<others_ou>',others_ou)
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
	
print "Sleeping 2 seconds to ensure slapd restart..."
time.sleep(2)
res = os.system('ldapadd -x -D "cn=admin,dc=skolesys,dc=org" -w %s -f skolesys.ldif' % in_adminpw)
if not res==0:
	print
	print "SkoleSYS Seeder - failed while adding creating LDAP server structure"
	sys.exit(1)

res = os.system('rm init.ldif skolesys.ldif -f')

f = open('/etc/hosts','a')
f.write('127.0.0.1\tmainserver.skolesys.local\n')
f.close()

import skolesys.lib.hostmanager as h
import skolesys.definitions.hostdef as hostdef
import skolesys.soap.netinfo as netinfo
hm = h.HostManager()
print hm.register_host(netinfo.if2hwaddr('eth0'),'mainserver',hostdef.hosttype_as_id('mainserver'))

import skolesys.cfmachine.configbuilder as confbuilder
cb = confbuilder.ConfigBuilder(hostdef.hosttype_as_id('mainserver'),netinfo.if2hwaddr('eth0'),'seed-mainserver')
curdir = os.getcwd()
os.chdir(cb.tempdir)
os.system('./install.sh')
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