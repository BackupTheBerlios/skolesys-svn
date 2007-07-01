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
fstab helper classes
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
	# /etc/fstab: static file system information.
	#
	# <file system> <mount point>   <type>  <options>       <dump>  <pass>
	proc    /proc   proc    defaults        0       0
	# /dev/hda7
	UUID=4fc18c48-1746-4416-ab0b-510781a4c323       /       ext3    defaults,errors=remount-ro      0       1
	/dev/hda4       /var/lib/vmware/vmachines       ext3    defaults        0       2
	# /dev/hda4
	# /dev/hda5
	UUID=1cbcce94-ac64-45d0-9948-80daf09e7020       /media/hda5     ext3    defaults        0       2
	# /dev/hda3
	UUID=d8cc665c-fa27-4d6f-9f01-f29c22c0aeb4       none    swap    sw      0       0
	/dev/hdc        /media/cdrom0   utf8,udf,iso9660        user,noauto     0       0
	/dev/hdb        /media/cdrom1   utf8,udf,iso9660        user,noauto     0       0
	/dev/   /media/floppy0  auto    rw,user,noauto  0       0
	>>>
	>>>
	>>> helper.add_entry('/dev/sda1','/media/sda1','vfat','defaults','0','3')
	>>> helper.print_fstab()
	# /etc/fstab: static file system information.
	#
	# <file system> <mount point>   <type>  <options>       <dump>  <pass>
	proc    /proc   proc    defaults        0       0
	# /dev/hda7
	UUID=4fc18c48-1746-4416-ab0b-510781a4c323       /       ext3    defaults,errors=remount-ro      0       1
	/dev/hda4       /var/lib/vmware/vmachines       ext3    defaults        0       2
	# /dev/hda4
	# /dev/hda5
	UUID=1cbcce94-ac64-45d0-9948-80daf09e7020       /media/hda5     ext3    defaults        0       2
	# /dev/hda3
	UUID=d8cc665c-fa27-4d6f-9f01-f29c22c0aeb4       none    swap    sw      0       0
	/dev/hdc        /media/cdrom0   utf8,udf,iso9660        user,noauto     0       0
	/dev/hdb        /media/cdrom1   utf8,udf,iso9660        user,noauto     0       0
	/dev/   /media/floppy0  auto    rw,user,noauto  0       0
	/dev/sda1       /media/sda1     vfat    defaults        0       3
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
		print '\n'.join(self.format_for_output())
		
	def add_entry(self,sourcefs,mountpoint,fstype,options,dump,fsckorder):
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
