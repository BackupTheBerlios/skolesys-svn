fetch_method = "svn"
svn_module = "skolesys-qt4"

control = {
	'Package': 'skolesys-qt4',
	'Version': 'file://skolesys_ver',
	'NameExtension': 'feisty_all',
	'Section': 'util',
	'Priority': 'optional',
	'Architecture': 'all',
	'Depends': 'python-skolesys-client, python-qt4, pyqt4-dev-tools',
	'Recommends': '',
	'Maintainer': 'Jakob Simon-Gaarde <jakob@skolesys.dk>',
	'Description': 'This is the graphical administration tool for SkoleSYS linux distribution',
	'longdesc': 
""" The skolesys-qt4 package provides the nessecary graphical tools for administrating the SkoleSYS
 distribution. The main issue here is creating users and groups, controlling permissions,
 creating user and group spaces, registering client workstations (Windows, Linux, MacOS)
 and registering thin client servers (LTSP).
"""}

perm = [['skolesys-qt4.py', '755']]

copy = {'.': '/usr/lib/skolesys-qt4/'}

links = {'/usr/bin/skolesys-qt4': '../lib/skolesys-qt4/skolesys-qt4.py'}

postinst = """
import os
import re

rx_uifile = re.compile('^(.*)\.ui$')

def ui_filter(args,dirname,names):
        for n in names:
                m = rx_uifile.match(n)
                if m:
                        os.system("pyuic4 %s -o %s" % (os.path.join(dirname,n),os.path.join(dirname,m.groups()[0])+'.py'))
                        print "Building %s.py..." % os.path.join(dirname,m.groups()[0])
                        os.system('rm %s' % os.path.join(dirname,n))

os.path.walk('/usr/lib/skolesys-qt4',ui_filter,None)
"""

postrm = """#!/bin/sh
if [ -e /usr/lib/skolesys-qt4 ]
then
  find /usr/lib/skolesys-qt4 -name "*.pyc" -delete
  find /usr/lib/skolesys-qt4 -name "*.pyo" -delete
fi
"""

