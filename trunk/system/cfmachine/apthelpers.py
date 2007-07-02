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
APT (debian's Advanced Package Tool) related helper classes. This
script is used by the SkoleSYS configuration system cfmachine when
deploying a configuration on a SkoleSYS registered host.
More precisely it is cfinstaller (ss_installer) that executes the
helper:
	
	ss_installer mod_apt_sources controlfile
"""

__author__ = "Jakob Simon-Gaarde <jakob@skolesys.dk>"

import re

class SourcesList:
	"""
	Parse and edit APT sources.list type files.
	
	Usage example:
	
	>>> import skolesys.cfmachine.apthelpers as ah
	>>> sl = ah.SourcesList('/etc/apt/sources.list')
	>>> sl.print_sources_list()
	deb-src http://dk.archive.ubuntu.com/ubuntu/    dapper-backports        main restricted universe multiverse
	deb-src http://dk.archive.ubuntu.com/ubuntu/    dapper-updates  main restricted
	deb     http://archive.skolesys.dk/stable/      dapper  main
	deb-src http://security.ubuntu.com/ubuntu       dapper-security main restricted universe
	deb     http://dk.archive.ubuntu.com/ubuntu/    dapper-updates  main restricted
	deb     http://dk.archive.ubuntu.com/ubuntu/    dapper  main restricted universe
	deb-src http://dk.archive.ubuntu.com/ubuntu/    dapper  main restricted universe
	deb     http://security.ubuntu.com/ubuntu       dapper-security main restricted universe
	deb     http://dk.archive.ubuntu.com/ubuntu/    dapper-backports        main restricted universe multiverse
	>>>
	>>>
	>>> sl.add_source('deb','http://test.domain.com','groovy',['cool','stuff'])
	>>> sl.print_sources_list()
	deb-src http://dk.archive.ubuntu.com/ubuntu/    dapper-backports        main restricted universe multiverse
	deb-src http://dk.archive.ubuntu.com/ubuntu/    dapper-updates  main restricted
	deb     http://archive.skolesys.dk/stable/      dapper  main
	deb-src http://security.ubuntu.com/ubuntu       dapper-security main restricted universe
	deb     http://dk.archive.ubuntu.com/ubuntu/    dapper-updates  main restricted
	deb     http://dk.archive.ubuntu.com/ubuntu/    dapper  main restricted universe
	deb     http://test.domain.com  groovy  cool stuff
	deb-src http://dk.archive.ubuntu.com/ubuntu/    dapper  main restricted universe
	deb     http://security.ubuntu.com/ubuntu       dapper-security main restricted universe
	deb     http://dk.archive.ubuntu.com/ubuntu/    dapper-backports        main restricted universe multiverse
	"""
	
	def __init__(self,filename=None):
		"""
		filename	path to sources.list file
		
		If no filename is parsed it will be attempted to read from 
		/etc/apt/sources.list.
		"""
		self.sources_map = self.parse_sources_list(filename)
		self.dirty = False
		
	def parse_sources_list(self,filename):
		"""
		filename	path to sources.list file
		
		Parse the source.list file used by apt to access debian repositories.
		If no value is passed to filename then /etc/apt/sources.list is default.
		This method parses the source.list file populating a dictionary with
		the source entries.
		The dictionary is returned when the parser has finished.
		"""
		rx_deb = re.compile('\s*(?!#)(deb|deb-src)\s+(\S+)\s+(\S+)\s+(.+)')
		rx_comp_split = re.compile('\s+')
		
		self.filename = filename
		if not filename:
			self.filename = '/etc/apt/sources.list'
		f = open(self.filename)
		deb_lines = f.readlines()
		f.close()
		sources_map = {}
		for l in deb_lines:
			m = rx_deb.match(l)
			
			if m:
				components = m.groups()[-1:][0]
				components = rx_comp_split.split(components.strip())
				
				if not sources_map.has_key(m.groups()[:-1]):
					sources_map[m.groups()[:-1]] = {
						'type':m.groups()[0],
						'uri':m.groups()[1],
						'distribution':m.groups()[2],
						'components':[]}
				for comp in components:
					if not sources_map[m.groups()[:-1]]['components'].count(comp):
						sources_map[m.groups()[:-1]]['components'] += [comp]
		return sources_map	
	
	def add_source(self,typ,uri,distribution,components):
		"""
		typ		"deb" or "deb-src"
		uri		ie. "http://archive.skolesys.dk"
		distribution	ie. "feisty"
		components	List of strings
		
		Add sources to the memory-based sources.list (self.sources_map). 
		components should be a list of strings.
		Duplicate sources will not occur as they are saved in a dictionary.
		"""
		if type(components)==str:
			components = [components]
		if not type(components)==list and not type(components)==tuple:
			raise TypeError,'components most be a list, string or a tuple'
		key = (typ,uri,distribution)
		if not self.sources_map.has_key(key):
			self.sources_map[key] = {
				'type':key[0],
				'uri':key[1],
				'distribution':key[2],
				'components':[]}
		for comp in components:
			if not self.sources_map[key]['components'].count(comp):
				self.dirty = True
				self.sources_map[key]['components'] += [comp]
			
		
	def format_for_output(self):
		"""
		Return a nicely formatted list of strings ready to be written
		into a sources.list file or printed to the screen.
		
		see:	print_sources_list()
				write_sources_list()
		"""
		output = []
		for src_key in self.sources_map.keys():
			src = self.sources_map[src_key]
			output += ["%s\t%s\t%s\t%s" % (src['type'],src['uri'],src['distribution'],' '.join(src['components']))]
		return output
			
	def print_sources_list(self):
		"""
		Print the sources to stdout as they will be
		written to file
		"""
		print '\n'.join(self.format_for_output())
			

	def write_sources_list(self,filename=None):
		"""
		filename	Path to the file to create/overwrite
		
		Write the sources nicely formatted in sources.list format 
		to file.
		"""
		if not filename:
			filename = self.filename
		f = open(filename,'w')
		f.write('\n'.join(self.format_for_output()))
		f.close()
	


if __name__ == '__main__':
	# test
	am = SourcesList()
	am.add_source('deb','http://mainserver.skolesys.local/debian','pilot',['main','nonfree','bla'])
	print am.dirty
	am.print_sources_list()
