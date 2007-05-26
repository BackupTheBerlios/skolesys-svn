fetch_method = "svn"
svn_module = "skolesys"

control = {
	'Package': 'python2.4-skolesys-mainserver',
	'Version': '0.9.5-1',
	'NameExtension': 'skolesys1_all',
	'Section': 'python',
	'Priority': 'optional',
	'Architecture': 'all',
	'Depends': 'python2.4, python-cheetah, python-smbpasswd, python2.4-soappy, m2crypto, python2.4-ldap',
	'Recommends': '',
	'Maintainer': 'Jakob Simon-Gaarde <jakob@skolesys.org>',
	'Description': 'This is the base control library of the SkoleSYS linux distribution',
	'Replaces': 'python2.4-skolesys-seeder',
	'Conflicts': 'python2.4-skolesys-seeder,python2.4-skolesys-client',
	'longdesc': 
""" The skolesys package provides the nessecary tools for administrating the SkoleSYS
 distribution. The main issue here is creating users and groups, controlling permissions,
 creating user and group spaces, registering client workstations (Windows, Linux, MacOS)
 and registering thin client servers (LTSP).
"""}

perm = [['soap/server.py', '755'],
	['soap/skolesysd', '755'],
	['lib/usercommands.py', '755'],
	['lib/groupcommands.py', '755'],
	['lib/hostcommands.py', '755'],
	['cfmachine/cfinstaller.py', '755'],
	['config-templates/default-templates', 'u+wrX,g-wx+rX,o-wx+rX'],
	['config-templates/default-templates/common/rootdir/etc/ldap.secret','g-r,o-r'],
	['config-templates/default-templates/common/rootdir/etc/pam_ldap.secret','g-r,o-r'],
	['config-templates/default-templates/ltspserver/rootdir/etc/firestarter/configuration','g-r,o-r'],
	['config-templates/default-templates/ltspserver/rootdir/etc/firestarter/inbound','g-Xr,o-Xr'],
	['config-templates/default-templates/ltspserver/rootdir/etc/cron.hourly/ss_update-hosts','u+rwx,g-rw,o-rw'],
	['misc/etc','g-r,o-r']]

copy = {
	'__init__.py': '/usr/lib/python2.4/site-packages/skolesys/',
	'lib': '/usr/lib/python2.4/site-packages/skolesys/',
	'soap': '/usr/lib/python2.4/site-packages/skolesys/',
	'cfmachine': '/usr/lib/python2.4/site-packages/skolesys/',
	'tools': '/usr/lib/python2.4/site-packages/skolesys/',
	'services': '/usr/lib/python2.4/site-packages/skolesys/',
	'definitions': '/usr/lib/python2.4/site-packages/skolesys/',
	'config-templates/default-templates': '/etc/skolesys/',
	'config-templates/custom-templates': '/etc/skolesys/',
	'config-templates/host-templates': '/etc/skolesys/',
	'config-templates/skel': '/etc/skolesys/',
	'config-templates/www': '/etc/skolesys/',
	'misc/etc/skolesys': '/etc/',
	'misc/etc/ldap/schema': '/etc/ldap/'}

links = {
	'/usr/sbin/ss_usermanager': '../lib/python2.4/site-packages/skolesys/lib/usercommands.py',
	'/usr/sbin/ss_groupmanager': '../lib/python2.4/site-packages/skolesys/lib/groupcommands.py',
	'/usr/sbin/ss_hostmanager': '../lib/python2.4/site-packages/skolesys/lib/hostcommands.py',
	'/usr/sbin/ss_soapserver': '../lib/python2.4/site-packages/skolesys/soap/server.py',
	'/usr/sbin/ss_installer': '../lib/python2.4/site-packages/skolesys/cfmachine/cfinstaller.py',
	'/etc/init.d/skolesysd': '/usr/lib/python2.4/site-packages/skolesys/soap/skolesysd',
	'/etc/rc0.d/K01skolesys': '../init.d/skolesysd',
	'/etc/rc2.d/S99skolesys': '../init.d/skolesysd',
	'/etc/rc3.d/S99skolesys': '../init.d/skolesysd',
	'/etc/rc4.d/S99skolesys': '../init.d/skolesysd',
	'/etc/rc5.d/S99skolesys': '../init.d/skolesysd',
	'/etc/rc6.d/K01skolesys': '../init.d/skolesysd'}


postrm = """#!/bin/sh
if [ -e /usr/lib/python2.4/site-packages/skolesys ]
then
  find /usr/lib/python2.4/site-packages/skolesys -name "*.pyc" -delete
  find /usr/lib/python2.4/site-packages/skolesys -name "*.pyo" -delete
fi
"""
