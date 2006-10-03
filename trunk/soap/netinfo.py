import socket
import fcntl
import struct
import re,os


def if2ip(ifname):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		return socket.inet_ntoa(fcntl.ioctl(
			s.fileno(),
			0x8915,  # SIOCGIFADDR
			struct.pack('256s', ifname[:15])
		)[20:24])
	except:
		return None
 
def ip2hwaddr(ip):
	try:
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
		rx_newif=re.compile('^(\w+)')
		rx_hwaddr=re.compile('^(\w+).+([0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2})')
		rx_inet_addr=re.compile('^.+inet addr:(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})')
		o = os.popen('ifconfig')
		out = o.readlines()
		o.close()
		
		ip_maps = {}
		cur_if = None
		cur_hwaddr = None
		for l in out:
			m = rx_newif.match(l)
			if m:
				cur_hwaddr = None
			m = rx_hwaddr.match(l)
			if m:
				cur_if = m.groups()[0]
				cur_hwaddr = m.groups()[1]
			m = rx_inet_addr.match(l)
			if m and cur_hwaddr:
				ip_maps[m.groups()[0]] = cur_hwaddr
		
		if ip_maps.has_key(ip.strip()):
			return ip_maps[ip.strip()]
		
	except:
		pass
	return None
