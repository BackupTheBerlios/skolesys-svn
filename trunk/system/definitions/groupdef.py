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

##### Groups ######
# Group types
_group_struct = {}

# NOTE: types are canse in-sensetive!
_group_struct['type_id'] = {
	1 : 'primary',
	2 : 'system',
	3 : 'service'}
	
_group_struct['type_text'] = {}
for k,v in _group_struct['type_id'].items():
	exec('G_%s=%d' % (v.upper(),k))
	_group_struct['type_text'][v.lower()] = k

def grouptype_as_id(grouptype):
	"""
	Convert a group type id (sanity check) or group type text to it's group type id.
	If an int is passed it is regarded as a group type id itself and therefore normally
	just returned as is, but if the value is not valid None is returned.
	"""
	if type(grouptype)==str:
		if _group_struct['type_text'].has_key(grouptype.strip().lower()):
			return _group_struct['type_text'][grouptype.strip().lower()]
	elif type(grouptype) == int:
		if _group_struct['type_id'].has_key(grouptype):
			return grouptype
	else:
		return None

def grouptype_as_text(grouptype):
	"""
	Convert a group type id or group type text (sanity check) to it's group type text.
	If a str is passed it is regarded as a group type text itself and therefore normally
	just returned as is, but if the value is not valid None is returned.
	"""
	if type(grouptype)==str:
		if _group_struct['type_text'].has_key(grouptype.strip().lower()):
			return grouptype.strip().lower()
	elif type(grouptype) == int:
		if _group_struct['type_id'].has_key(grouptype):
			return _group_struct['type_id'][grouptype]
	else:
		return None

def list_grouptypes_by_id():
	return _group_struct['type_id'].keys()

def list_grouptypes_by_text():
	return _group_struct['type_text'].keys()

del k
del v