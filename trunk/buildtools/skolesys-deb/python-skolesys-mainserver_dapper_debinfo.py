fetch_method = "svn"
svn_module = "skolesys"

control = {
	'Package': 'python-skolesys-mainserver',
	'Version': 'file://skolesys_ver',
	'NameExtension': 'dapper_all',
	'Section': 'python',
	'Priority': 'optional',
	'Architecture': 'all',
	'Depends': 'python-support, python-cheetah, python-smbpasswd, python-soappy, m2crypto, python-ldap',
	'Recommends': '',
	'Maintainer': 'Jakob Simon-Gaarde <jakob@skolesys.dk>',
	'Description': 'This is the base control library of the SkoleSYS linux distribution',
	'Replaces': 'python2.4-skolesys-seeder,python-skolesys-seeder,python2.4-skolesys-mainserver',
	'Provides': 'python2.3-skolesys-mainserver, python2.4-skolesys-mainserver',
	'Conflicts': 'python2.4-skolesys-seeder,python2.4-skolesys-client,python-skolesys-seeder,python-skolesys-client',
	'longdesc': 
""" The skolesys package provides the nessecary tools for administrating the SkoleSYS
 distribution. The main issue here is creating users and groups, controlling permissions,
 creating user and group spaces, registering client workstations (Windows, Linux, MacOS)
 and registering thin client servers (LTSP).
"""}

perm = {'soap/server.py': '755',
	'soap/skolesysd': '755',
	'lib/usercommands.py': '755',
	'lib/groupcommands.py': '755',
	'lib/hostcommands.py': '755',
	'cfmachine/cfinstaller.py': '755',
	'config-templates/default-templates': 'u+wrX,g-wx+rX,o-wx+rX',
	'config-templates/default-templates/common/rootdir/etc/ldap.secret':'g-r,o-r',
	'config-templates/default-templates/common/rootdir/etc/pam_ldap.secret':'g-r,o-r',
	'config-templates/default-templates/ltspserver/rootdir/etc/firestarter/configuration':'g-r,o-r',
	'config-templates/default-templates/ltspserver/rootdir/etc/firestarter/inbound':'g-Xr,o-Xr',
	'config-templates/default-templates/ltspserver/rootdir/etc/cron.hourly/ss_update-hosts':'u+rwx,g-rw,o-rw',
	'misc/etc':'g-r,o-r'}

copy = {
	'__init__.py': '/usr/share/python-support/python-skolesys-mainserver/skolesys/',
	'lib': '/usr/share/python-support/python-skolesys-mainserver/skolesys/',
	'soap': '/usr/share/python-support/python-skolesys-mainserver/skolesys/',
	'cfmachine': '/usr/share/python-support/python-skolesys-mainserver/skolesys/',
	'tools': '/usr/share/python-support/python-skolesys-mainserver/skolesys/',
	'services': '/usr/share/python-support/python-skolesys-mainserver/skolesys/',
	'definitions': '/usr/share/python-support/python-skolesys-mainserver/skolesys/',
	'config-templates/default-templates': '/etc/skolesys/',
	'config-templates/custom-templates': '/etc/skolesys/',
	'config-templates/host-templates': '/etc/skolesys/',
	'config-templates/skel': '/etc/skolesys/',
	'config-templates/www': '/etc/skolesys/',
	'misc/etc/skolesys': '/etc/',
	'misc/etc/ldap/schema': '/etc/ldap/'}

links = {
	'/usr/sbin/ss_usermanager': '../share/python-support/python-skolesys-mainserver/skolesys/lib/usercommands.py',
	'/usr/sbin/ss_groupmanager': '../share/python-support/python-skolesys-mainserver/skolesys/lib/groupcommands.py',
	'/usr/sbin/ss_hostmanager': '../share/python-support/python-skolesys-mainserver/skolesys/lib/hostcommands.py',
	'/usr/sbin/ss_soapserver': '../share/python-support/python-skolesys-mainserver/skolesys/soap/server.py',
	'/usr/sbin/ss_installer': '../share/python-support/python-skolesys-mainserver/skolesys/cfmachine/cfinstaller.py',
	'/etc/init.d/skolesysd': '/usr/share/python-support/python-skolesys-mainserver/skolesys/soap/skolesysd',
	'/etc/rc0.d/K01skolesys': '../init.d/skolesysd',
	'/etc/rc2.d/S99skolesys': '../init.d/skolesysd',
	'/etc/rc3.d/S99skolesys': '../init.d/skolesysd',
	'/etc/rc4.d/S99skolesys': '../init.d/skolesysd',
	'/etc/rc5.d/S99skolesys': '../init.d/skolesysd',
	'/etc/rc6.d/K01skolesys': '../init.d/skolesysd'}

preinst = """#!/bin/sh
rm default-templates -Rf
"""

postinst = """#!/bin/sh
set -e

if [ "$1" = "configure" ] && which update-python-modules >/dev/null 2>&1; then
        update-python-modules -i /usr/share/python-support/python-skolesys-mainserver
fi

/etc/init.d/skolesysd restart
"""

prerm = """#!/bin/sh
set -e

/etc/init.d/skolesysd stop

if which update-python-modules >/dev/null 2>&1; then
        update-python-modules -c -i /usr/share/python-support/python-skolesys-mainserver
fi
"""

postrm = """#!/bin/sh
if [ -e /usr/share/python-support/python-skolesys-mainserver/skolesys ]
then
  find /usr/share/python-support/python-skolesys-mainserver/skolesys -name "*.pyc" -delete
  find /usr/share/python-support/python-skolesys-mainserver/skolesys -name "*.pyo" -delete
fi
"""

