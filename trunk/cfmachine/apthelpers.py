import re

class SourcesList:
	
	def __init__(self,filename=None):
		self.sources_map = self.parse_sources_list(filename)
		self.dirty = False
		
	def parse_sources_list(self,filename):
		"""
		Parse the source.list file used by apt to access debian repositories.
		If no value is passed to filename then /etc/apt/sources.list is default
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
		Add sources to the memory-based sources.list. components should
		be a list of strings.
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
		output = []
		for src_key in self.sources_map.keys():
			src = self.sources_map[src_key]
			output += ["%s\t%s\t%s\t%s" % (src['type'],src['uri'],src['distribution'],' '.join(src['components']))]
		return output
			
	def print_sources_list(self):
		print '\n'.join(self.format_for_output())
			

	def write_sources_list(self,filename=None):
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
