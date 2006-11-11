fetch_method = "svn"
svn_module = "skolesys"

control = {
	'Package': 'python2.4-skolesys-seeder',
	'Version': '0.7.8',
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

perm = [['seeder/init_client.py', '755'],
	['seeder/init_mainserver.py', '755'],
	['cfmachine/cfinstaller.py', '755']]

copy = {
	'__init__.py': '/usr/lib/python2.4/site-packages/skolesys/',
	'tools': '/usr/lib/python2.4/site-packages/skolesys/',
	'cfmachine/__init__.py': '/usr/lib/python2.4/site-packages/skolesys/cfmachine',
	'cfmachine/cfinstaller.py': '/usr/lib/python2.4/site-packages/skolesys/cfmachine',
	'cfmachine/apthelpers.py': '/usr/lib/python2.4/site-packages/skolesys/cfmachine',
	'cfmachine/fstabhelpers.py': '/usr/lib/python2.4/site-packages/skolesys/cfmachine',
	'seeder': '/usr/lib/python2.4/site-packages/skolesys/'}

links = {
	'/usr/sbin/ss_installer': '../lib/python2.4/site-packages/skolesys/cfmachine/cfinstaller.py',
	'/usr/sbin/ss_seed_mainserver': '../lib/python2.4/site-packages/skolesys/seeder/init_mainserver.py',
	'/usr/sbin/ss_seed_client': '../lib/python2.4/site-packages/skolesys/seeder/init_client.py'}

postrm = """#!/bin/sh
rm /usr/lib/python2.4/site-packages/skolesys -R -f
"""
