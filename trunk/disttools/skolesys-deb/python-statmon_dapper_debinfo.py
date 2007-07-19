fetch_method = "svn"
svn_module = "trunk"
svn_repos = "http://svn.berlios.de/svnroot/repos/statmon"

control = {
	'Package': 'python-statmon',
	'Version': 'file://statmon_ver',
	'NameExtension': 'dapper_all',
	'Section': 'util',
	'Priority': 'optional',
	'Architecture': 'all',
	'Depends': 'python-support, python-pysqlite2 (>= 2.3.2), python-pyinotify (>= 0.7.1)',
	'Recommends': '',
	'Maintainer': 'Jakob Simon-Gaarde <jakob@skolesys.dk>',
	'Description': 'Index files and their attributes in a sqlite db.',
	'longdesc': 
""" Keep track of large quantities of files and all the attributes 
 associated with them. Statmon features a synchronization feature
 and optional enabling of inotify to keep the file stat db up-to-date. 
"""}

perm = {'statmon.py': '755'}

copy = {'.': '/usr/share/python-support/python-statmon/statmon/'}

links = {'/usr/bin/statmon': '../share/python-support/python-statmon/statmon/statmon.py'}

postinst = """#!/bin/sh
set -e

if [ "$1" = "configure" ] && which update-python-modules >/dev/null 2>&1; then
	update-python-modules -a -f -i /usr/share/python-support/python-statmon
fi
"""

prerm = """#!/bin/sh
set -e

if which update-python-modules >/dev/null 2>&1; then
	update-python-modules -c -i /usr/share/python-support/python-statmon
fi
"""

postrm = """#!/bin/sh
if [ -e /usr/share/python-support/python-statmon/statmon ]
then
  find /usr/share/python-support/python-statmon/statmon -name "*.pyc" -delete
  find /usr/share/python-support/python-statmon/statmon -name "*.pyo" -delete
fi
"""

