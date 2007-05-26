fetch_method = "svn"
svn_module = "skolesys"

control = {
	'Package': 'python2.4-skolesys-seeder',
	'Version': '0.9.3',
	'NameExtension': 'skolesys1_all',
	'Section': 'python',
	'Priority': 'optional',
	'Architecture': 'all',
	'Depends': 'python2.4, m2crypto',
	'Recommends': '',
	'Maintainer': 'Jakob Simon-Gaarde <jakob@skolesys.org>',
	'Description': 'The SkoleSYS seeder package',
	'Conflicts': 'python2.4-skolesys-mainserver, python2.4-skolesys-client',
	'longdesc': 
""" The SkoleSYS seeder package provides scripts to seed a host as a mainserver or client
"""}

perm = [['seeder/seed_workstation.py', '755'],
	['seeder/seed_ltspserver.py', '755'],
	['seeder/seed_mainserver.py', '755'],
	['cfmachine/cfinstaller.py', '755'],
	['soap/getconf.py', '755'],
	['soap/reghost.py', '755']]

copy = {
	'__init__.py': '/usr/lib/python2.4/site-packages/skolesys/',
	'tools': '/usr/lib/python2.4/site-packages/skolesys/',
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
	'seeder': '/usr/lib/python2.4/site-packages/skolesys/',
	'definitions': '/usr/lib/python2.4/site-packages/skolesys/'}

links = {
	'/usr/sbin/ss_seed_mainserver': '../lib/python2.4/site-packages/skolesys/seeder/seed_mainserver.py',
	'/usr/sbin/ss_seed_workstation': '../lib/python2.4/site-packages/skolesys/seeder/seed_workstation.py',
	'/usr/sbin/ss_seed_ltspserver': '../lib/python2.4/site-packages/skolesys/seeder/seed_ltspserver.py',
	'/usr/sbin/ss_installer': '../lib/python2.4/site-packages/skolesys/cfmachine/cfinstaller.py',
	'/usr/sbin/ss_getconf': '../lib/python2.4/site-packages/skolesys/soap/getconf.py',
	'/usr/sbin/ss_reghost': '../lib/python2.4/site-packages/skolesys/soap/reghost.py'}

postrm = """#!/bin/sh
if [ -e /usr/lib/python2.4/site-packages/skolesys ]
then
  find /usr/lib/python2.4/site-packages/skolesys -name "*.pyc" -delete
  find /usr/lib/python2.4/site-packages/skolesys -name "*.pyo" -delete
fi
"""
