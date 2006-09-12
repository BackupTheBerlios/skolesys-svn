control = \
"""Package: python2.4-skolesys
Version: 0.5
Section: python
Priority: optional
Architecture: i386
Depends: python2.4, python-smbpasswd, python2.4-soappy, m2crypto, python2.4-ldap
Recommends: skolesys_ui
Maintainer: Jakob Simon-Gaarde <jakob@skolesys.org>
Description: This is the base control library of the SkoleSYS linux distribution
 The skolesys package provides the nessecary tools for administrating the SkoleSYS
 distribution. The main issue here is creating users and groups, controlling permissions,
 creating user and group spaces, registering client workstations (Windows, Linux, MacOS)
 and registering thin client servers (LTSP).
"""

copy = {
	'__init__.py': '/usr/lib/python2.4/site-packages/skolesys/',
	'lib': '/usr/lib/python2.4/site-packages/skolesys/',
	'soap': '/usr/lib/python2.4/site-packages/skolesys/',
	'cert': '/usr/lib/python2.4/site-packages/skolesys/'}
