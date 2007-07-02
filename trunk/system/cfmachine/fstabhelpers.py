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
fstab helper classes used by cfinstaller (ss_installer) to update the
fstab on SkoleSYS registered hosts that recieve their configuration via
the ss_getconf script.
More precisely it is cfinstaller (ss_installer) that executes the
helper:
	
	ss_installer mod_fstab controlfile

"""

__author__ = "Jakob Simon-Gaarde <jakob@skolesys.dk>"

import re

class Fstab:
	"""
	Parse and edit APT /etc/fstab type files.
	
	Usage example:
	>>> import skolesys.cfmachine.fstabhelpers as fh
	>>> helper = fh.Fstab('/etc/fstab')
	>>> helper.print_fstab()
	proc            /proc                       proc                defaults                    0   0
	/dev/hda5       /                           ext3                defaults,errors=remount-ro  0   1
	/dev/hda4       /var/lib/vmware/vmachines   ext3                defaults                    0   2
	# /dev/hda3
	/dev/hda2       none                       swap                 sw                          0   0
	/dev/hdc        /media/cdrom0               utf8,udf,iso9660    user,noauto                 0   0
	/dev/hdb        /media/cdrom1               utf8,udf,iso9660    user,noauto                 0   0
	>>>
	>>>
	>>> helper.add_entry('/dev/sda1','/media/sda1','vfat','defaults','0','3')
	>>> helper.print_fstab()
	proc            /proc                       proc                defaults                    0   0
	/dev/hda5       /                           ext3                defaults,errors=remount-ro  0   1
	/dev/hda4       /var/lib/vmware/vmachines   ext3                defaults                    0   2
	# /dev/hda3
	/dev/hda2       none                       swap                 sw                          0   0
	/dev/hdc        /media/cdrom0               utf8,udf,iso9660    user,noauto                 0   0
	/dev/hdb        /media/cdrom1               utf8,udf,iso9660    user,noauto                 0   0
	/dev/sda1       /media/sda1                 vfat                defaults                    0   3
"""	
	def __init__(self,filename=None):
		"""
		filename	path to fstab file
		
		If no filename is parsed it will be attempted to read from 
		/etc/fstab
		"""		
		self.mount_map = self.parse_fstab(filename)

	def parse_fstab(self,filename):
		"""
		filename	path to sources.list file
		
		Parse the fstab file used for defining static information about filesystems
		If no value is passed to filename then /etc/fstab is used by default.
		This method parses the fstab file populating a dictionary with the
		mount points and mount options.
		The dictionary is returned when the parser has finished.
		"""
		self.dirty = False
		rx_mountpoint = re.compile('^\s*(?!#)(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s*$')
		
		self.filename = filename
		if not filename:
			self.filename = '/etc/fstab'
		f = open(self.filename)
		mount_lines = f.readlines()
		f.close()
		mount_map = {}
		self.order = 0
		dummy_key = 0
		for l in mount_lines:
			m = rx_mountpoint.match(l)
			if m:
				mount_map[(m.groups()[:2])] = {
					'sourcefs': m.groups()[0],
					'mountpoint': m.groups()[1],
					'fstype': m.groups()[2],
					'options': m.groups()[3],
					'dump': m.groups()[4],
					'fsckorder': m.groups()[5],
					'order': self.order,
					'linetype':'mnt'}
			else:
				mount_map[dummy_key] = {
					'text': l.strip(),
					'order': self.order,
					'linetype':'other'}
			dummy_key += 1
			self.order += 1
			
		return mount_map
					
	def format_for_output(self):
		"""
		Return a nicely formatted list of strings ready to be written
		into the fstab file or printed to the screen.
		
		see:	print_fstab()
				write_fstab()
		"""
		output = []
		for mnt_key in self.mount_map.keys():
			mnt = self.mount_map[mnt_key]
			if mnt['linetype'] == 'mnt':
				output += [[mnt['order'],"%s\t%s\t%s\t%s\t%s\t%s" % (mnt['sourcefs'],mnt['mountpoint'],mnt['fstype'],mnt['options'],mnt['dump'],mnt['fsckorder'])]]
			else:
				output += [[mnt['order'],mnt['text']]]
		final_out = []
		output.sort()
		for mnt in output:
			final_out += [mnt[1]]
		
		return final_out
			
	def print_fstab(self):
		"""
		Print the filesystem mountpoints to stdout as they will be
		written to file
		"""
		print '\n'.join(self.format_for_output())
		
	def add_entry(self,sourcefs,mountpoint,fstype,options='defaults',dump='0',fsckorder='0'):
		"""
		sourcefs	The filesystem to be mounted (ie. '/dev/hda2')
		mountpoint	The point to where the filesystem should be mounted (ie. '/home/erik/data')
		fstype		Filesystem type (ie. 'vfat', 'ext2', 'ext3')
		options 	Mount with following filesystem options (def: 'defaults')
		dump 		Dump can be used for scheduled backups with the dump command (def: '0')
		fsckorder 	Set the order in which a filesystem should be checked with the fsck command (def: '0')
		
		Add filesystems to the memory-based fstab (self.mount_map). Duplicate 
		sourcefs/mountpoint combinations will not occur as they are saved in a 
		dictionary.
		"""
		order = self.order
		if self.mount_map.has_key((sourcefs,mountpoint)):
			order = self.mount_map[(sourcefs,mountpoint)]['order']
		else:
			self.order += 1
			self.dirty = True
			
		self.mount_map[(sourcefs,mountpoint)] = {
			'sourcefs': sourcefs,
			'mountpoint': mountpoint,
			'fstype': fstype,
			'options': options,
			'dump': dump,
			'fsckorder': fsckorder,
			'order': order,
			'linetype':'mnt'}
			
	def write_fstab(self,filename=None):
		"""
		filename	Path to the file to create/overwrite
		
		Write the filesystem mountpoints nicely formatted in fstab format 
		to file.
		"""
		if not filename:
			filename = self.filename
		f = open(filename,'w')
		f.write('\n'.join(self.format_for_output())+'\n')
		f.close()

if __name__ == '__main__':
	# test
	a=Fstab()
	a.add_entry('mainserver.skolesys.local:/skolesys', '/skolesys','nfs','defaults','0','0')
	a.print_fstab()
	a.write_fstab()
