fetch_method = "tgz"

#prebuild_script = \
#"""
#"""

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

