fetch_method = "svn"
svn_module = "skolesys-ui"

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
	'Package': 'skolesys-ui',
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
""" The skolesys-ui package provides the nessecary graphical tools for administrating the SkoleSYS
 distribution. The main issue here is creating users and groups, controlling permissions,
 creating user and group spaces, registering client workstations (Windows, Linux, MacOS)
 and registering thin client servers (LTSP).
"""}

perm = [['skolesys-ui.py', '755']]

copy = {'.': '/usr/lib/skolesys-ui/'}

links = {'/usr/bin/skolesys-ui': '../lib/skolesys-ui/skolesys-ui.py'}
