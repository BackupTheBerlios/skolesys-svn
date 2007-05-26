fetch_method = "svn"
svn_module = "skolesys"

control = {
	'Package': 'python-skolesys-client',
	'Version': '0.9.5-2',
	'NameExtension': 'feisty_all',
	'Section': 'python',
	'Priority': 'optional',
	'Architecture': 'all',
	'Depends': 'python-support (>= 0.2), python-soappy, python-m2crypto',
	'Recommends': 'skolesys-qt4',
	'Maintainer': 'Jakob Simon-Gaarde <jakob@skolesys.dk>',
	'Replaces': 'python-skolesys-seeder, python2.4-skolesys-seeder, python2.4-skolesys-client',
	'Conflicts': 'python2.4-skolesys-mainserver, python2.4-skolesys-seeder, python-skolesys-mainserver, python-skolesys-seeder',
	'Provides': 'python2.5-skolesys-client, python2.3-skolesys-client, python2.4-skolesys-client',
	'Description': 'This is the soap client part of the SkoleSYS linux distribution',
	'longdesc': 
""" The skolesys package provides the nessecary tools for administrating the SkoleSYS
 distribution. The main issue here is creating users and groups, controlling permissions,
 creating user and group spaces, registering client workstations (Windows, Linux, MacOS)
 and registering thin client servers (LTSP).
"""}

perm = [['cfmachine/cfinstaller.py', '755'],
	['soap/getconf.py', '755'],
	['soap/reghost.py', '755']]

copy = {
	'__init__.py': '/usr/share/python-support/python-skolesys-client/skolesys/',
	'soap/__init__.py': '/usr/share/python-support/python-skolesys-client/skolesys/soap',
	'soap/netinfo.py': '/usr/share/python-support/python-skolesys-client/skolesys/soap',
	'soap/marshall.py': '/usr/share/python-support/python-skolesys-client/skolesys/soap',
	'soap/getconf.py': '/usr/share/python-support/python-skolesys-client/skolesys/soap',
	'soap/reghost.py': '/usr/share/python-support/python-skolesys-client/skolesys/soap',
	'soap/client.py': '/usr/share/python-support/python-skolesys-client/skolesys/soap',
	'soap/p2.py': '/usr/share/python-support/python-skolesys-client/skolesys/soap',
	'cfmachine/__init__.py': '/usr/share/python-support/python-skolesys-client/skolesys/cfmachine',
	'cfmachine/cfinstaller.py': '/usr/share/python-support/python-skolesys-client/skolesys/cfmachine',
	'cfmachine/apthelpers.py': '/usr/share/python-support/python-skolesys-client/skolesys/cfmachine',
	'cfmachine/fstabhelpers.py': '/usr/share/python-support/python-skolesys-client/skolesys/cfmachine',
	'tools': '/usr/share/python-support/python-skolesys-client/skolesys/',
	'definitions': '/usr/share/python-support/python-skolesys-client/skolesys/'}

links = {
	'/usr/sbin/ss_installer': '../share/python-support/python-skolesys-client/skolesys/cfmachine/cfinstaller.py',
	'/usr/sbin/ss_getconf': '../share/python-support/python-skolesys-client/skolesys/soap/getconf.py',
	'/usr/sbin/ss_reghost': '../share/python-support/python-skolesys-client/skolesys/soap/reghost.py'}

postinst = """#!/bin/sh
set -e
# Automatically added by dh_pysupport
if [ "$1" = "configure" ] && which update-python-modules >/dev/null 2>&1; then
        update-python-modules -i /usr/share/python-support/python-skolesys-client
fi
# End automatically added section
"""

prerm = """#!/bin/sh
set -e
# Automatically added by dh_pysupport
if which update-python-modules >/dev/null 2>&1; then
        update-python-modules -c -i /usr/share/python-support/python-skolesys-client
fi
# End automatically added section
"""

postrm = """#!/bin/sh
if [ -e /usr/share/python-support/python-skolesys-client/skolesys ]
then
  find /usr/share/python-support/python-skolesys-client/skolesys -name "*.pyc" -delete
  find /usr/share/python-support/python-skolesys-client/skolesys -name "*.pyo" -delete
fi
"""

