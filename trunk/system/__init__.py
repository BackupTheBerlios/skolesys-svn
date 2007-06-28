# This file is part of the SkoleSYS libraries
# Copyright (C) 2007 Jakob Simon-Gaarde <info at skolesys.dk>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License version 2 as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public License
# along with this library; see the file COPYING.LIB.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301, USA.

"""
The skolesys package is used by SkoleSYS mainservers and SkoleSYS workstations
and SkoleSYS LTSP servers. These three host types all depend on different parts
of the package contents but not all of the contents. Therefore it kan not be
expected that all contents are available on any given SkoleSYS seeded host.

skolesys.cfmachine
------------------
The SkoleSYS configuration system. Any Linux based SkoleSYS host (mainserver,
LTSP server or workstation) can request an updated configuration as long as the
host is registered.
cfmachine is template based. SkoleSYS comes with default templates for configuring
the three SkoleSYS linux based host types - these templates can be found in 
/etc/skolesys/default-templates. Here you will also find two other empty directories
custom-templates and host-templates for general and host-specific customization.

skolesys.definitions
--------------------
The definitions sub-package is where types are defined. While writing this there
are 3 definition classes: user type definitions, group type definitions, host type
definitions. There is also a class for glueing groups and users together with LDAP
queries.

skolesys.lib
------------
A sub-package containing the classes for controlling users, groups, services
and hosts. The SkoleSYS mainserver uses these classes for it's main housekeeping:
	- Create, delete and modify users
	- Create, delete and modify groups
	- Register SkoleSYS linux based hosts
	
There are also command line scripts for doing administration via a shell.
skolesys.lib is only used by the SkoleSYS mainserver but can be manipulated by
school administrators through the skolesys.soap interface.

skolesys.services
-----------------
SkoleSYS services are pluggable and can be installed as add-on products. The only
service that that is distributed with SkoleSYS is groupservice "webservice".
services can be grouped into 2 categories groupservices and userservices. 

skolesys.soap
-------------
Features a SOAP server that runs on the SkoleSYS mainserver, and a SOAP client
that can run from any other Linux based SkoleSYS host type. The SOAP server
exposes all nessecary functions needed to do "normal" administrative tasks
remotely. The official SkoleSYS administrative GUI "skolesys-qt4" uses this
SOAP interface to communicate with the SkoleSYS back-end. SOAPpy is used
for the interface implementation.

skolesys.tools
--------------
Here will be placed all ad-hoc functions.

"""
__author__ = "Jakob Simon-Gaarde <jakob@skolesys.dk>"
__all__ = ["lib","soap","cfmachine","tools","definitions","services"]

def _get_exports_list(module):
    try:
        return list(module.__all__)
    except AttributeError:
        return [n for n in dir(module) if n[0] != '_']

