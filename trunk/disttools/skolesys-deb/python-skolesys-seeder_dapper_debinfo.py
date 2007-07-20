fetch_method = "svn"
svn_module = "system"

control = {
	'Package': 'python-skolesys-seeder',
	'Version': 'file://skolesys_ver',
	'NameExtension': 'dapper_all',
	'Section': 'python',
	'Priority': 'optional',
	'Architecture': 'all',
	'Depends': 'python-support, m2crypto',
	'Recommends': '',
	'Maintainer': 'Jakob Simon-Gaarde <jakob@skolesys.dk>',
	'Description': 'The SkoleSYS seeder package',
	'Provides': 'python2.3-skolesys-seeder, python2.4-skolesys-seeder',
	'Conflicts': 'python2.4-skolesys-mainserver, python2.4-skolesys-client, python-skolesys-mainserver, python-skolesys-client',
	'longdesc': 
""" The SkoleSYS seeder package provides scripts to seed a host as a mainserver or client
"""}

perm = {'seeder/seed_workstation.py': '755',
	'seeder/seed_ltspserver.py': '755',
	'seeder/seed_mainserver.py': '755',
	'cfmachine/cfinstaller.py': '755',
	'soap/getconf.py': '755',
	'soap/reghost.py': '755',
	'tmp/skolesys_apt_primer': '755'}

copy = {
	'__init__.py': '/usr/share/python-support/python-skolesys-seeder/skolesys/',
	'tools': '/usr/share/python-support/python-skolesys-seeder/skolesys/',
	'soap/__init__.py': '/usr/share/python-support/python-skolesys-seeder/skolesys/soap',
	'soap/netinfo.py': '/usr/share/python-support/python-skolesys-seeder/skolesys/soap',
	'soap/marshall.py': '/usr/share/python-support/python-skolesys-seeder/skolesys/soap',
	'soap/getconf.py': '/usr/share/python-support/python-skolesys-seeder/skolesys/soap',
	'soap/reghost.py': '/usr/share/python-support/python-skolesys-seeder/skolesys/soap',
	'soap/client.py': '/usr/share/python-support/python-skolesys-seeder/skolesys/soap',
	'soap/p2.py': '/usr/share/python-support/python-skolesys-seeder/skolesys/soap',
	'cfmachine/__init__.py': '/usr/share/python-support/python-skolesys-seeder/skolesys/cfmachine',
	'cfmachine/cfinstaller.py': '/usr/share/python-support/python-skolesys-seeder/skolesys/cfmachine',
	'cfmachine/apthelpers.py': '/usr/share/python-support/python-skolesys-seeder/skolesys/cfmachine',
	'cfmachine/fstabhelpers.py': '/usr/share/python-support/python-skolesys-seeder/skolesys/cfmachine',
	'seeder': '/usr/share/python-support/python-skolesys-seeder/skolesys/',
	'definitions': '/usr/share/python-support/python-skolesys-seeder/skolesys/',
	'misc/tmp': '/'}

links = {
	'/usr/sbin/ss_seed_mainserver': '../share/python-support/python-skolesys-seeder/skolesys/seeder/seed_mainserver.py',
	'/usr/sbin/ss_seed_workstation': '../share/python-support/python-skolesys-seeder/skolesys/seeder/seed_workstation.py',
	'/usr/sbin/ss_seed_ltspserver': '../share/python-support/python-skolesys-seeder/skolesys/seeder/seed_ltspserver.py',
	'/usr/sbin/ss_installer': '../share/python-support/python-skolesys-seeder/skolesys/cfmachine/cfinstaller.py',
	'/usr/sbin/ss_getconf': '../share/python-support/python-skolesys-seeder/skolesys/soap/getconf.py',
	'/usr/sbin/ss_reghost': '../share/python-support/python-skolesys-seeder/skolesys/soap/reghost.py'}

postinst = """#!/bin/sh
set -e
# Automatically added by dh_pysupport
if [ "$1" = "configure" ] && which update-python-modules >/dev/null 2>&1; then
        update-python-modules -a -f -i /usr/share/python-support/python-skolesys-seeder
fi

/tmp/skolesys_apt_primer

# End automatically added section
"""

prerm = """#!/bin/sh
set -e
# Automatically added by dh_pysupport
if which update-python-modules >/dev/null 2>&1; then
        update-python-modules -c -i /usr/share/python-support/python-skolesys-seeder
fi
# End automatically added section
"""

postrm = """#!/bin/sh
if [ -e /usr/share/python-support/python-skolesys-seeder/skolesys ]
then
  find /usr/share/python-support/python-skolesys-seeder/skolesys -name "*.pyc" -delete
  find /usr/share/python-support/python-skolesys-seeder/skolesys -name "*.pyo" -delete
fi
"""
