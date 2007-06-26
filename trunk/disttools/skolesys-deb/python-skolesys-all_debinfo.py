fetch_method = "svn"
svn_module = "system"

control = {
	'Package': 'python-skolesys-all',
	'Version': 'file://skolesys_ver',
	'NameExtension': 'all',
	'Section': 'python',
	'Priority': 'optional',
	'Architecture': 'all',
	'Depends': 'python-support, python-cheetah, python-smbpasswd, python-soappy, m2crypto, python-ldap',
	'Recommends': '',
	'Maintainer': 'Jakob Simon-Gaarde <jakob@skolesys.dk>',
	'Description': 'This is the base control library of the SkoleSYS linux distribution',
	'Provides': 'python-skolesys-all',
	'Replaces': 'python-skolesys-client',
	'Conflicts': '',
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
	'cfmachine/cfinstaller.py': '755'}

copy = {
	'__init__.py': '/usr/share/python-support/python-skolesys-all/skolesys/',
	'lib': '/usr/share/python-support/python-skolesys-all/skolesys/',
	'soap': '/usr/share/python-support/python-skolesys-all/skolesys/',
	'cfmachine': '/usr/share/python-support/python-skolesys-all/skolesys/',
	'tools': '/usr/share/python-support/python-skolesys-all/skolesys/',
	'services': '/usr/share/python-support/python-skolesys-all/skolesys/',
	'definitions': '/usr/share/python-support/python-skolesys-all/skolesys/',
	'seeder': '/usr/share/python-support/python-skolesys-all/skolesys/'}


preinst = """#!/bin/sh
rm default-templates -Rf
"""

postinst = """#!/bin/sh
set -e

if [ "$1" = "configure" ] && which update-python-modules >/dev/null 2>&1; then
        update-python-modules -i /usr/share/python-support/python-skolesys-all
fi

"""

prerm = """#!/bin/sh
set -e

if which update-python-modules >/dev/null 2>&1; then
        update-python-modules -c -i /usr/share/python-support/python-skolesys-all
fi
"""

postrm = """#!/bin/sh
if [ -e /usr/share/python-support/python-skolesys-all/skolesys ]
then
  find /usr/share/python-support/python-skolesys-all/skolesys -name "*.pyc" -delete
  find /usr/share/python-support/python-skolesys-all/skolesys -name "*.pyo" -delete
fi
"""

