fetch_method = "svn"

control = {
	'Package': 'python2.4-skolesys-client',
	'Version': '0.5.5',
	'NameExtension': 'skolesys1_all',
	'Section': 'python',
	'Priority': 'optional',
	'Architecture': 'all',
	'Depends': 'python2.4, python2.4-soappy, m2crypto',
	'Recommends': 'skolesys_ui',
	'Maintainer': 'Jakob Simon-Gaarde <jakob@skolesys.org>',
	'Description': 'This is the soap client part of the SkoleSYS linux distribution',
	'longdesc': 
""" The skolesys package provides the nessecary tools for administrating the SkoleSYS
 distribution. The main issue here is creating users and groups, controlling permissions,
 creating user and group spaces, registering client workstations (Windows, Linux, MacOS)
 and registering thin client servers (LTSP).
"""}

perm = {'cfmachine/cfinstaller.py': '755',
	'soap/getconf.py': '755',
	'soap/reghost.py': '755'}

copy = {
	'__init__.py': '/usr/lib/python2.4/site-packages/skolesys/',
	'lib': '/usr/lib/python2.4/site-packages/skolesys/',
	'soap': '/usr/lib/python2.4/site-packages/skolesys/',
	'cert': '/usr/lib/python2.4/site-packages/skolesys/',
	'cfmachine': '/usr/lib/python2.4/site-packages/skolesys/',
	'tools': '/usr/lib/python2.4/site-packages/skolesys/',
	'definitions': '/usr/lib/python2.4/site-packages/skolesys/'}

links = {
	'/usr/sbin/ss_installer': '../lib/python2.4/site-packages/skolesys/cfmachine/cfinstaller.py',
	'/usr/sbin/ss_getconf': '../lib/python2.4/site-packages/skolesys/soap/getconf.py',
	'/usr/sbin/ss_reghost': '../lib/python2.4/site-packages/skolesys/soap/getconf.py'}

