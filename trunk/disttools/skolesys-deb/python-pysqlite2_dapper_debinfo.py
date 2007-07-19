fetch_method = "tgz"

control = {
	'Package': 'python-pysqlite2',
	'Version': '2.3.4',
	'NameExtension': 'dapper_i386',
	'Section': 'python',
	'Priority': 'optional',
	'Architecture': 'i386',
	'Replaces': 'python2.3-pysqlite2, python2.4-pysqlite2',
	'Provides': 'python2.4-pysqlite2, python2.5-pysqlite2',
	'Conflicts': 'python2.3-pysqlite2, python2.4-pysqlite2',
	'Depends': 'python-support, libc6 (>= 2.3.4-1), libsqlite3-0 (>= 3.2.8), python (<< 2.6), python (>= 2.4)',
	'Recommends': '',
	'Maintainer': 'Jakob Simon-Gaarde <jakob@skolesys.org>',
	'Description': 'Python sqlite3 interface',
	'longdesc': 
""" Python interface to SQLite 3
 pysqlite is a DB-API 2.0-compliant database interface for SQLite.
 .
 This package is built against SQLite 3. For an interface to SQLite 2,
 see the package python-sqlite. An alternative Python SQLite 3 module
 is packaged as python-apsw.
 .
 SQLite is a relational database management system contained in a
 relatively small C library. It is a public domain project created
 by D. Richard Hipp. Unlike the usual client-server paradigm, the
 SQLite engine is not a standalone process with which the program
 communicates, but is linked in and thus becomes an integral part
 of the program. The library implements most of SQL-92 standard,
 including transactions, triggers and most of complex queries.
 .
 pysqlite makes this powerful embedded SQL engine available to
 Python programmers. It stays compatible with the Python database
 API specification 2.0 as much as possible, but also exposes most
 of SQLite's native API, so that it is for example possible to
 create user-defined SQL functions and aggregates in Python.
 .
 If you need a relational database for your applications, or even
 small tools or helper scripts, pysqlite is often a good fit. It's
 easy to use, easy to deploy, and does not depend on any other
 Python libraries or platform libraries, except SQLite. SQLite
 itself is ported to most platforms you'd ever care about.
 .
 It's often a good alternative to MySQL, the Microsoft JET engine
 or the MSDE, without having any of their license and deployment
 issues.
"""}

prebuild_script = \
"""
import os
cwd = os.getcwd()
os.chdir('rep')
os.system('python2.4 setup.py build')
os.chdir(cwd)
"""

copy = {'doc': '/usr/share/doc/python-pysqlite2/',
	'LICENSE': '/usr/share/doc/python-pysqlite2',
	'build/lib.linux-i686-2.4/pysqlite2': '/usr/share/python-support/python-pysqlite2/'}

postinst = """#!/bin/sh
set -e

if [ "$1" = "configure" ] && which update-python-modules >/dev/null 2>&1; then
	update-python-modules -a -f -i /usr/share/python-support/python-pysqlite2
fi
"""

prerm = """#!/bin/sh
set -e

if which update-python-modules >/dev/null 2>&1; then
	update-python-modules -c -i /usr/share/python-support/python-pysqlite2
fi
"""

postrm = """#!/bin/sh
if [ -e /usr/share/python-support/python-pysqlite2/pysqlite2 ]
then
  find /usr/share/python-support/python-pysqlite2/pysqlite2 -name "*.pyc" -delete
  find /usr/share/python-support/python-pysqlite2/pysqlite2 -name "*.pyo" -delete
fi
"""

