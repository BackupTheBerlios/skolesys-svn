import socket
import fcntl
import struct
import re,os


def if2ip(ifname):
	try:
		# local interface
		ifmap,hwaddrmap,ipmap = parse_ifconfig()
		return ifmap[ifname.strip()]['inet_addr']
		
	except:
		pass
	return None
 
def ip2if(ip):
	try:
		# local interface
		ifmap,hwaddrmap,ipmap = parse_ifconfig()
		return ipmap[ip.strip()]['if']
		
	except:
		pass
	return None

def ip2hwaddr(ip):
	try:
		# Remote interface
		arp = open('/proc/net/arp')
		lines = arp.readlines()
		arp.close()
		c=re.compile('^(\S+)\s+\S+\s+\S+\s+(\S+)')
		for l in lines[1:]:
			m=c.match(l)
			if m and m.groups()[0]==ip:
				return m.groups()[1]
	except:
		pass
	try:
		# local interface
		ifmap,hwaddrmap,ipmap = parse_ifconfig()
		return ipmap[ip.strip()]['hwaddr']
		
	except:
		pass
	return None


def parse_ifconfig():
	rx_newif=re.compile('^(\w+)')
	rx_hwaddr=re.compile('^(\w+).+([0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2})')
	rx_inet_addr=re.compile('^.+inet addr:(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})')
	if os.path.exists('/sbin/ifconfig'):
		o = os.popen('/sbin/ifconfig')
	elif os.path.exists('/usr/sbin/ifconfig'):
		o = os.popen('/usr/sbin/ifconfig')
	else:
		o = os.popen('ifconfig')
	out = o.readlines()
	o.close()
	
	if_map = {}
	hwaddr_map = {}
	inet_addr_map = {}
	cur_if = None
	cur_hwaddr = None
	cur_ip = None
	for l in out:
		m = rx_newif.match(l)
		if m:
			if cur_if:
				if_map[cur_if] = {
					'hwaddr': cur_hwaddr,
					'inet_addr': cur_ip}
				if cur_hwaddr:
					hwaddr_map[cur_hwaddr] = {
						'if': cur_if,
						'inet_addr': cur_ip}
				if cur_ip:
					inet_addr_map[cur_ip] = {
						'if': cur_if,
						'hwaddr': cur_hwaddr}
			cur_hwaddr = None
			cur_ip = None
			cur_if = m.groups()[0]
			
		m = rx_hwaddr.match(l)
		if m:
			cur_hwaddr = m.groups()[1]
			
		m = rx_inet_addr.match(l)
		if m:
			cur_ip = m.groups()[0]
			
	if cur_if:
		if_map[cur_if] = {
			'hwaddr': cur_hwaddr,
			'inet_addr': cur_ip}
		if cur_hwaddr:
			hwaddr_map[cur_hwaddr] = {
				'if': cur_if,
				'inet_addr': cur_ip}
		if cur_ip:
			inet_addr_map[cur_ip] = {
				'if': cur_if,
				'hwaddr': cur_hwaddr}
			
	return if_map,hwaddr_map,inet_addr_map