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
skolesys.cfmachine is the SkoleSYS configuration service. Any registered 
SkoleSYS host can request its own (maybe unique) configuration.
When a host requests an updated configuration cfmachine starts by 
collecting all relevant information for the domain, host type and even
the specific host. The configuration is returned as a tarball which the
requesting host then extracts and deploys by calling the install.sh
script enclosed in the tarball.

The configuration system is template based and default templates come with
the standard SkoleSYS installation placed under:
  /etc/skolesys/default-templates

Hosts can request their full configuration or just a part of it (by
context). For the system to deliver the best suited configuration
for a specific host it must send its distibution release "codename"
(ie. dapper or feisty). This is done automatically when using the 
ss_getconf command from a host.

  Usage: ss_getconf [options]

  Options:
    -h, --help            show this help message and exit
    -c CONFCONTEXT, --config-context=CONFCONTEXT
                          Retrieve a specialized configuration for a given event
                          or context

It is easy to add custom configurations to host-types, contexts and even
specific hosts. ie. if we need to alter /etc/nsswitch.conf which by default
is a common template (all host types) used by all distibution releases:
  /etc/skolesys/default-templates/common/all/rootdir/etc/nsswitch.conf

to something slightly different - it is just a question of placing a copy
of the original in the correct directory and then make the change. 
Here are some examples of where to place the modified nsswitch.conf:

1. All host types
  /etc/skolesys/custom-templates/common/all/rootdir/etc/nsswitch.conf

2. All LTSP server host types
  /etc/skolesys/custom-templates/ltspserver/all/rootdir/etc/nsswitch.conf

3. All workstation host types using (k)ubuntu release codename "feisty"
  /etc/skolesys/custom-templates/workstation/feisty/rootdir/etc/nsswitch.conf

4. Special treatment for host 00:11:22:33:44:55
  /etc/skolesys/host-templates/01:23:45:67:89:ab/all/rootdir/etc/nsswitch.conf

"""

__all__ = ["infocollection","configbuilder","fstabhelpers","apthelpers"]

def _get_exports_list(module):
    try:
        return list(module.__all__)
    except AttributeError:
        return [n for n in dir(module) if n[0] != '_']

