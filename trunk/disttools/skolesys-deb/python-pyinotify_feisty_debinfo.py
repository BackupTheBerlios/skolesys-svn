fetch_method = "tgz"

control = {
	'Package': 'python-pyinotify',
	'Version': '0.7.1',
	'NameExtension': 'feisty_i386',
	'Section': 'python',
	'Priority': 'optional',
	'Architecture': 'i386',
	'Replaces': 'python2.3-pyinotify, python2.4-pyinotify',
	'Provides': 'python2.4-pyinotify, python2.5-pyinotify',
	'Conflicts': 'python2.3-pyinotify, python2.4-pyinotify',
	'Depends': 'python-support, libc6 (>= 2.3.4-1), python (<< 2.6), python (>= 2.4)',
	'Recommends': '',
	'Maintainer': 'Jakob Simon-Gaarde <jakob@skolesys.org>',
	'Description': 'Simple Linux inotify Python bindings',
	'longdesc': 
""" pyinotify is a simple wrapper for the Linux inotify mechanism.
 .
 inotify is a Linux Kernel feature available since 2.6.13. inotify makes
 it possible for applications to easily be notified of filesystem changes.
 .
 Homepage: http://pyinotify.sourceforge.net/
"""}

prebuild_script = \
"""
import os
cwd = os.getcwd()
os.chdir('rep')
os.system('python2.4 setup.py build')
os.system('mkdir bin_python2.4 bin_python2.5')
os.system('cp src/pyinotify/_inotify.so bin_python2.4/_inotify.so')
os.system('rm src/pyinotify/_inotify.so src/pyinotify/pyinotify.pyo')
os.system('python2.5 setup.py build')
os.system('cp src/pyinotify/_inotify.so bin_python2.5/_inotify.so')
os.chdir(cwd)
"""

copy = {'doc': '/usr/share/doc/python-pyinotify/',
	'COPYING': '/usr/share/doc/python-pyinotify',
	'README': '/usr/share/doc/python-pyinotify',
	'src/pyinotify.pth': '/usr/share/python-support/python-pyinotify',
	'src/pyinotify/iglob.py': '/usr/share/python-support/python-pyinotify/pyinotify',
	'src/pyinotify/inotify.py': '/usr/share/python-support/python-pyinotify/pyinotify',
	'src/pyinotify/pyinotify.py': '/usr/share/python-support/python-pyinotify/pyinotify',
	'bin_python2.4/_inotify.so': '/usr/lib/python-support/python-pyinotify/python2.4/pyinotify',
	'bin_python2.5/_inotify.so': '/usr/lib/python-support/python-pyinotify/python2.5/pyinotify'}

postinst = """#!/bin/sh
set -e

if [ "$1" = "configure" ] && which update-python-modules >/dev/null 2>&1; then
	update-python-modules -a -f -i /usr/share/python-support/python-pyinotify
fi
"""

prerm = """#!/bin/sh
set -e

if which update-python-modules >/dev/null 2>&1; then
	update-python-modules -c -i /usr/share/python-support/python-pyinotify
fi
"""

postrm = """#!/bin/sh
if [ -e /usr/share/python-support/python-pyinotify/pyinotify ]
then
  find /usr/share/python-support/python-pyinotify/pyinotify -name "*.pyc" -delete
  find /usr/share/python-support/python-pyinotify/pyinotify -name "*.pyo" -delete
fi
"""

