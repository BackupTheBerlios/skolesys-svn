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
# coding=UTF-8

def system_nicefy_string(instr):
	replacemap = {
		'æ':'ae', 'ø': 'oe', 'å': 'aa',
		'Æ':'Ae', 'Ø': 'Oe', 'Å': 'Aa',
		' ': ''}
	import re
	c=re.compile('[-\.\w]+')
	nice_chars = c.findall(instr)
	ugly_chars = c.split(instr)
	assemble = ''
	for idx in xrange(len(ugly_chars)):
		nicefied_ugly_chars = ugly_chars[idx]
		
		# nicefy some system viewed ugly characters
		for ugly,nicer in replacemap.items():
			nicefied_ugly_chars = nicefied_ugly_chars.replace(ugly,nicer)
		nice_chars2 = c.findall(nicefied_ugly_chars)
		nicefied_ugly_chars=''.join(nice_chars2)
		
		assemble += nicefied_ugly_chars
		if len(nice_chars) > idx:
			assemble += nice_chars[idx]
			
	return assemble[:16]
