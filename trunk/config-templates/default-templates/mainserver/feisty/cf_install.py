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
apt_source_entries = [
	{'type':'deb','uri':'http://archive.skolesys.dk/$[conf.cfmachine.package_group]','distribution':'feisty','components':['main']},
        {'type':'deb','uri':'http://archive.ubuntu.com/ubuntu/','distribution':'feisty','components':['main','restricted','universe']},
        {'type':'deb-src','uri':'http://archive.ubuntu.com/ubuntu/','distribution':'feisty','components':['main','restricted','universe']},
        {'type':'deb','uri':'http://archive.ubuntu.com/ubuntu/','distribution':'feisty-backports','components':['main','restricted','universe','multiverse']},
        {'type':'deb-src','uri':'http://archive.ubuntu.com/ubuntu/','distribution':'feisty-backports','components':['main','restricted','universe','multiverse']},
        {'type':'deb','uri':'http://security.ubuntu.com/ubuntu','distribution':'feisty-security','components':['main','restricted','universe']},
        {'type':'deb-src','uri':'http://security.ubuntu.com/ubuntu','distribution':'feisty-security','components':['main','restricted','universe']}]

fstab_entries = []
	
packagelist_files = [
	'default-packages','custom-packages']

copy_files_rootdir = \
	'rootdir'

hostname = \
	'$reciever.hostName'

kick_daemons = [
	'/etc/init.d/networking restart',
	'/etc/init.d/dhcp3-server restart',
	'/etc/init.d/nfs-kernel-server restart',
	'/etc/init.d/nfs-common restart',
	'/etc/init.d/samba restart',
	'/etc/init.d/dnsmasq restart',
	'/etc/init.d/apache2 restart',
	'/etc/init.d/skolesysd restart']
