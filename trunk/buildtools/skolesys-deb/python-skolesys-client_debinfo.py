fetch_method = "svn"
svn_module = "skolesys"

control = {
	'Package': 'python2.4-skolesys-client',
	'Version': '0.7.3',
	'NameExtension': 'skolesys1_all',
	'Section': 'python',
	'Priority': 'optional',
	'Architecture': 'all',
	'Depends': 'python2.4, python2.4-soappy, m2crypto',
	'Recommends': 'skolesys_ui',
	'Maintainer': 'Jakob Simon-Gaarde <jakob@skolesys.org>',
	'Replaces': 'python2.4-skolesys-seeder',
	'Conflicts': 'python2.4-skolesys-mainserver, python2.4-skolesys-seeder',
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
	'__init__.py': '/usr/lib/python2.4/site-packages/skolesys/',
	'soap/__init__.py': '/usr/lib/python2.4/site-packages/skolesys/soap',
	'soap/netinfo.py': '/usr/lib/python2.4/site-packages/skolesys/soap',
	'soap/marshall.py': '/usr/lib/python2.4/site-packages/skolesys/soap',
	'soap/getconf.py': '/usr/lib/python2.4/site-packages/skolesys/soap',
	'soap/reghost.py': '/usr/lib/python2.4/site-packages/skolesys/soap',
	'soap/client.py': '/usr/lib/python2.4/site-packages/skolesys/soap',
	'soap/p2.py': '/usr/lib/python2.4/site-packages/skolesys/soap',
	'cfmachine/__init__.py': '/usr/lib/python2.4/site-packages/skolesys/cfmachine',
	'cfmachine/cfinstaller.py': '/usr/lib/python2.4/site-packages/skolesys/cfmachine',
	'cfmachine/apthelpers.py': '/usr/lib/python2.4/site-packages/skolesys/cfmachine',
	'cfmachine/fstabhelpers.py': '/usr/lib/python2.4/site-packages/skolesys/cfmachine',
	'tools': '/usr/lib/python2.4/site-packages/skolesys/',
	'definitions': '/usr/lib/python2.4/site-packages/skolesys/'}

links = {
	'/usr/sbin/ss_installer': '../lib/python2.4/site-packages/skolesys/cfmachine/cfinstaller.py',
	'/usr/sbin/ss_getconf': '../lib/python2.4/site-packages/skolesys/soap/getconf.py',
	'/usr/sbin/ss_reghost': '../lib/python2.4/site-packages/skolesys/soap/reghost.py'}

postrm = """#!/bin/sh
rm /usr/lib/python2.4/site-packages/skolesys -R -f
"""
