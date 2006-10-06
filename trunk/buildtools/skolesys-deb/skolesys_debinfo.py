fetch_method = "svn"

control = {
	'Package': 'python2.4-skolesys',
	'Version': '0.5.4',
	'NameExtension': 'skolesys1_all',
	'Section': 'python',
	'Priority': 'optional',
	'Architecture': 'all',
	'Depends': 'python2.4, python-smbpasswd, python2.4-soappy, m2crypto, python2.4-ldap',
	'Recommends': 'skolesys_ui',
	'Maintainer': 'Jakob Simon-Gaarde <jakob@skolesys.org>',
	'Description': 'This is the base control library of the SkoleSYS linux distribution',
	'longdesc': 
""" The skolesys package provides the nessecary tools for administrating the SkoleSYS
 distribution. The main issue here is creating users and groups, controlling permissions,
 creating user and group spaces, registering client workstations (Windows, Linux, MacOS)
 and registering thin client servers (LTSP).
"""}

perm = {'soap/server.py': '755',
	'lib/shell.py': '755',
	'lib/hostcommands.py': '755',
	'cfmachine/cfinstaller.py': '755',
	'soap/getconf.py': 755}

copy = {
	'__init__.py': '/usr/lib/python2.4/site-packages/skolesys/',
	'lib': '/usr/lib/python2.4/site-packages/skolesys/',
	'soap': '/usr/lib/python2.4/site-packages/skolesys/',
	'cert': '/usr/lib/python2.4/site-packages/skolesys/',
	'cfmachine': '/usr/lib/python2.4/site-packages/skolesys/',
	'tools': '/usr/lib/python2.4/site-packages/skolesys/'}

links = {
	'/usr/sbin/ss_accounts': '../lib/python2.4/site-packages/skolesys/lib/shell.py',
	'/usr/sbin/ss_hosts': '../lib/python2.4/site-packages/skolesys/lib/hostcommands.py',
	'/usr/sbin/ss_soapserver': '../lib/python2.4/site-packages/skolesys/soap/server.py',
	'/usr/sbin/ss_installer': '../lib/python2.4/site-packages/skolesys/cfmachine/cfinstaller.py',
	'/usr/sbin/ss_getconf': '../lib/python2.4/site-packages/skolesys/soap/getconf.py'}

