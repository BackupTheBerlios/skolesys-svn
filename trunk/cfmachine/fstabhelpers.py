import re

class Fstab:

	def __init__(self,filename=None):
		self.mount_map = self.parse_fstab(filename)

	def parse_fstab(self,filename):
		"""
		Parse the fstab file.
		If no value is passed to filename then /etc/apt/sources.list is default
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
