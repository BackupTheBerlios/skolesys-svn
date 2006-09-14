fetch_method = "iso"

prebuild_script = \
"""
import os
import re

rx_tgzfile = re.compile('^(.*)\.tgz$')

def tgz_filter(args,dirname,names):
	for n in names:
		m = rx_tgzfile.match(n)
		if m:
			print "Extracting %s..." % os.path.join(dirname,n)
			os.system('tar -C rep/extract/ -xzpf %s' % os.path.join(dirname,n))

if not os.path.exists('rep/extract'):
	os.mkdir('rep/extract')
os.path.walk('rep',tgz_filter,None)


if not os.path.exists('rep/deb/lts'):
	os.makedirs('rep/deb/lts')

os.system('mv rep/extract/i386 rep/deb')
os.system('mv rep/extract/ltsp-utils rep/deb')
os.system('mv rep/extract/* rep/deb/lts/')

for f in os.listdir('rep/deb/lts'):
	if os.path.isdir('rep/deb/lts/%s' % f):
		os.system('ln -s %s rep/deb/lts/ltsp' % f)
		print "Creating link rep/deb/lts/ltsp -> %s" % f
		break
"""

control = {
	'Package': 'skolesys-ltsp',
	'Version': '4.2-2',
	'NameExtension': 'skolesys1_i386',
	'Section': 'misc',
	'Priority': 'optional',
	'Architecture': 'i386',
	'Depends': '',
	'Recommends': '',
	'Maintainer': 'Jakob Simon-Gaarde <jakob@skolesys.org>',
	'Description': 'The LTSP in a package',
	'longdesc': 
""" This package rolls the LTSP base system in the same manner
 as ltsp-admin.
"""}

copy = {'deb/i386': '/opt/ltsp/',
	'deb/lts': '/tftpboot/'}

