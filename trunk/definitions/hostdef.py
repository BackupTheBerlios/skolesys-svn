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
import re
# SkoleSYS host types

_host_struct = {}

# NOTE: types are canse in-sensetive!
_host_struct['type_id'] = {
	1 : 'mainserver',
	2 : 'ltspserver',
	3 : 'ltspclient',
	4 : 'workstation'}
	
_host_struct['type_text'] = {}
for k,v in _host_struct['type_id'].items():
	exec('%s=%d' % (v.upper(),k))
	_host_struct['type_text'][v.lower()] = k

# tools, validation and sanitychecks

def iptoint(ipaddr):
	ipint = 0
	c = re.compile('^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$')
	m = c.match(ipaddr.strip())
	if m:
		for ipnum_idx in xrange(len(m.groups())):
			ipint += int(m.groups()[ipnum_idx])*(256**(3-ipnum_idx))
		return ipint
	return None
	
def inttoip(ipint):
	return '%d.%d.%d.%d' % ((ipint>>24)&255,(ipint>>16)&255,(ipint>>8)&255,ipint&255)




def check_subnet(subnet_str):
	c = re.compile('^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/(\d{1,2})$')
	subnet_str = subnet_str.strip()
	m = c.match(subnet_str)
	if m:
		return m.groups()
	return None


def check_hostname(hostname):
	c = re.compile('^[a-z0-9]+$')
	hostname = hostname.strip().lower()
	m = c.match(hostname)
	if m:
		return hostname
	return None
	
def check_hwaddr(hwaddr):
	if not hwaddr:
		return None
	c1 = re.compile('^[a-f0-9]{2}:[a-f0-9]{2}:[a-f0-9]{2}:[a-f0-9]{2}:[a-f0-9]{2}:[a-f0-9]{2}$')
	c2 = re.compile('^([a-f0-9]{2})([a-f0-9]{2})([a-f0-9]{2})([a-f0-9]{2})([a-f0-9]{2})([a-f0-9]{2})$')
	hwaddr = hwaddr.strip().lower()
	m = c1.match(hwaddr)
	if m:
		return hwaddr
	m = c2.match(hwaddr)
	if m:
		return ':'.join(m.groups())
	return None
	
def check_ipaddr(ipaddr):
	c = re.compile('^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$')
	ipaddr = ipaddr.strip().lower()
	m = c.match(ipaddr)
	if m:
		for num in m.groups():
			if int(num)<0 or int(num)>255:
				return None
		return ipaddr
	

def hosttype_as_id(hosttype):
	"""
	Convert a host type id (sanity check) or host type text to it's host type id.
	If an int is passed it is regarded as a host type id itself and therefore normally
	just returned as is, but if the value is not valid None is returned.
	"""
	if type(hosttype)==str:
		if _host_struct['type_text'].has_key(hosttype.strip().lower()):
			return _host_struct['type_text'][hosttype.strip().lower()]
	elif type(hosttype) == int:
		if _host_struct['type_id'].has_key(hosttype):
			return hosttype
	else:
		return None

def hosttype_as_text(hosttype):
	"""
	Convert a host type id or host type text (sanity check) to it's host type text.
	If a str is passed it is regarded as a host type text itself and therefore normally
	just returned as is, but if the value is not valid None is returned.
	"""
	if type(hosttype)==str:
		if _host_struct['type_text'].has_key(hosttype.strip().lower()):
			return hosttype.strip().lower()
	elif type(hosttype) == int:
		if _host_struct['type_id'].has_key(hosttype):
			return _host_struct['type_id'][hosttype]
	else:
		return None

def list_hosttypes_by_id():
	return _host_struct['type_id'].keys()

def list_hosttypes_by_text():
	return _host_struct['type_text'].keys()


