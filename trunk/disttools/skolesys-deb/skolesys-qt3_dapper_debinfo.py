fetch_method = "svn"
svn_module = "ui/skolesys-qt3"

prebuild_script = \
"""
import os
import re

rx_uifile = re.compile('^(.*)\.ui$')

def ui_filter(args,dirname,names):
        for n in names:
                m = rx_uifile.match(n)
                if m:
                        os.system("pyuic %s -o %s" % (os.path.join(dirname,n),os.path.join(dirname,m.groups()[0])+'.py'))
                        print "Building %s.py..." % os.path.join(dirname,m.groups()[0])
                        os.system('rm %s' % os.path.join(dirname,n))

os.path.walk('rep',ui_filter,None)
"""

control = {
	'Package': 'skolesys-qt3',
	'Version': '0.7.9',
	'NameExtension': 'skolesys1_all',
	'Section': 'util',
	'Priority': 'optional',
	'Architecture': 'all',
	'Depends': 'python2.4, python2.4-skolesys-client, python2.4-qt3',
	'Recommends': '',
	'Maintainer': 'Jakob Simon-Gaarde <jakob@skolesys.org>',
	'Description': 'This is the graphical administration tool for SkoleSYS linux distribution',
	'longdesc': 
""" The skolesys-qt3 package provides the nessecary graphical tools for administrating the SkoleSYS
 distribution. The main issue here is creating users and groups, controlling permissions,
 creating user and group spaces, registering client workstations (Windows, Linux, MacOS)
 and registering thin client servers (LTSP).
"""}

perm = {'skolesys-qt3.py': '755'}

copy = {'.': '/usr/lib/skolesys-qt3/'}

links = {'/usr/bin/skolesys-qt3': '../lib/skolesys-qt3/skolesys-qt3.py'}

postrm = """#!/bin/sh
if [ -e /usr/lib/skolesys-qt3 ]
then
  find /usr/lib/skolesys-qt3 -name "*.pyc" -delete
  find /usr/lib/skolesys-qt3 -name "*.pyo" -delete
fi
"""