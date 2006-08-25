import socket
import fcntl
import struct
import re


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
	return None
