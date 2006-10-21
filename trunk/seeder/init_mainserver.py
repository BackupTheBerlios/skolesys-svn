#!/usr/bin/python
import skolesys.tools.mkpasswd as pw
import getpass,os,time,re,sys
import inspect
import skolesys.seeder

# Check root privilegdes
if not os.getuid()==0:
        print "This command requires root priviledges"
        sys.exit(0)

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

f = open('%s/skolesys.conf_template' % location)
lines = f.readlines()
f.close()

f = open('/etc/skolesys/skolesys.conf','w')
for l in lines:
        l = l.replace('<domain_name>',domain_name)
        l = l.replace('<domain_name_prefix>',domain_name_prefix)
        l = l.replace('<schooladmin_passwd>',in_schooladminpw)
        f.write(l)
f.close()
os.system('chmod 600 /etc/skolesys/skolesys.conf')

# Read template files before they are removed
f = open('%s/slapd.conf_template' % location)
slapd_conf_lines = f.readlines()
f.close()

f = open('%s/skolesys.ldif_template' % location)
skolesys_ldif_lines = f.readlines()
f.close()

# Replace python-skolesys-seeder with python-skolesys-mainserver
os.system('apt-get install python2.4-skolesys-mainserver -y')

from skolesys.lib.conf import conf

f = open('/etc/ldap/slapd.conf','w')
os.system('rm /var/lib/ldap/* -R -f')
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
users_ou,users = fetch_conf_ou('users')
machines_ou,machines = fetch_conf_ou('machines')
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
	l = l.replace('<users_ou>',users_ou)
	l = l.replace('<machines_ou>',machines_ou)
	l = l.replace('<hosts_ou>',hosts_ou)
	l = l.replace('<groups>',groups)
	l = l.replace('<logins>',logins)
	l = l.replace('<teachers>',teachers)
	l = l.replace('<students>',students)
	l = l.replace('<parents>',parents)
	l = l.replace('<others>',others)
	l = l.replace('<samba>',samba)
	l = l.replace('<users>',users)
	l = l.replace('<machines>',machines)
	l = l.replace('<hosts>',hosts)
	l = l.replace('<domain_name>',conf.get('DOMAIN','domain_name'))
	l = l.replace('<domain_name_prefix>',domain_name_prefix)
	l = l.replace('<passwd>',pw.mkpasswd(in_adminpw,3,'crypt').strip())
	l = l.replace('<schooladmin_passwd>',pw.mkpasswd(in_schooladminpw,3,'crypt').strip())
	f.write(l)
f.close()

os.system('/etc/init.d/slapd restart')
print "Sleeping 2 seconds to ensure slapd restart..."
time.sleep(2)
os.system('ldapadd -x -D "cn=admin,dc=skolesys,dc=org" -w %s -f skolesys.ldif' % in_adminpw)
os.system('rm init.ldif skolesys.ldif -f')
