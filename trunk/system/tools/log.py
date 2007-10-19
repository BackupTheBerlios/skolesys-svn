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

__author__ = "Jakob Simon-Gaarde <jakob@skolesys.dk>"

import syslog
from skolesys.lib.conf import conf

cur_loglevel = 0 	# by default logging is off
if conf.has_option('DOMAIN','loglevel'):
	loglevel = conf.get('DOMAIN','loglevel')
	if loglevel.isdigit():
		cur_loglevel = int(loglevel)


def write(msg,loglevel=3,context=None,force=False):
	global cur_loglevel
	if cur_loglevel<loglevel and force==False:
		# Log level filters out this message
		return
	
	ident = "skolesys"
	if context:
		ident = "skolesys-%s" % str(context)

	syslog.openlog(ident)
	syslog.syslog(msg)
	syslog.closelog()
