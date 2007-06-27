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

import os.path
from ConfigParser import ConfigParser
if os.path.exists('./skolesys.conf'):
	conf = ConfigParser()
	conf.readfp(open('./skolesys.conf'))
	
elif os.path.exists('/etc/skolesys/skolesys.conf'):
	conf = ConfigParser()
	conf.readfp(open('/etc/skolesys/skolesys.conf'))
else:
	print "skolesys.conf could be read"

