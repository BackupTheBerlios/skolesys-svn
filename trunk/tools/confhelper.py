'''
This file is part of the SkoleSYS libraries
Copyright (C) 2007 Jakob Simon-Gaarde <info at skolesys.dk>

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Library General Public
License version 2 as published by the Free Software Foundation.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Library General Public License for more details.

You should have received a copy of the GNU Library General Public License
along with this library; see the file COPYING.LIB.  If not, write to
the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
Boston, MA 02110-1301, USA.
'''
from ConfigParser import ConfigParser
import os

def conf2dict(filename,to_lower=True):
	conf_dict = {}
	if os.path.exists(filename):
		conf = ConfigParser()
		f=open(filename)
		conf.readfp(f)
		f.close()
	else:
		return None
	sections = conf.sections()
	for sec in sections:
		if to_lower:
			s = sec.lower()
		else:
			s = sec
		conf_dict[s] = {}
		for var,val in conf.items(sec):
			if to_lower:
				conf_dict[s][var.lower()] = val
			else:
				conf_dict[s][var] = val
	return conf_dict
