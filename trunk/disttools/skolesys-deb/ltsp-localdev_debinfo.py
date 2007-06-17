fetch_method = "tgz"

control = {
	'Package': 'skolesys-ltsp-localdev-kde',
	'Version': '4.2-2',
	'NameExtension': 'skolesys1_i386',
	'Section': 'misc',
	'Priority': 'optional',
	'Architecture': 'i386',
	'Depends': 'libfuse2, fuse-utils, libx11-protocol-perl',
	'Recommends': '',
	'Maintainer': 'Jakob Simon-Gaarde <jakob@skolesys.org>',
	'Description': 'SkoleSYS LTSP Local devices for KDE',
	'longdesc': 
""" This package Enables local devices for on a SkoleSYS LTSP server.
"""}

copy = {'etc': '/',
	'usr': '/'}

postinst = """#! /usr/bin/python

def check_exists_fuse():
	import re

	f=open('/etc/modules')
	lines = f.readlines()
	f.close()

	c=re.compile('^\s*fuse\s*$')
	for l in lines:
		if c.match(l):
			return True

	return False


import os,sys

if not os.path.exists('/etc/modules'):
	print "WARNING: /etc/modules does not exist, cannot check if fuse is loaded at boot."
	sys.exit(1)

if check_exists_fuse()==False:
	print "Adding fuse to /etc/modules"
        f=open('/etc/modules','a')
	f.write('fuse\\n')
        f.close()

sys.exit(0)
"""
