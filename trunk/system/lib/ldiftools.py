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

from ldif import LDIFParser
from ldaptools import LDAPUtil
from conf import conf
import StringIO

class LDIFImporter(LDIFParser):
	def __init__(self, input):
		LDIFParser.__init__(self, input)
		self.imp_data = []

	def handle(self, dn, entry):
		attributes = [ (k,v) for k,v in entry.items() ]
		self.imp_data += [[dn,attributes]]


def createFromTemplate(host,admin,passwd,tmp_filename,tagdict):
	ldif_test = open(tmp_filename)
	buf = ldif_test.read()
	for tag in tagdict.keys():
		buf = buf.replace(tag,tagdict[tag])

	f=StringIO.StringIO(buf)
	imp = LDIFImporter(f)
	imp.parse()
	
	l = LDAPUtil(host)
	l.bind(admin,passwd)
	
	for dn,attribs in imp.imp_data:
		print dn,attribs
		l.l.add_s(dn,attribs)

if __name__=='__main__':
	host = conf.get('LDAPSERVER','host')
	admin = conf.get('LDAPSERVER','admin')
	passwd = conf.get('LDAPSERVER','passwd')
	tmp_filename = 'skolesys.template.ldif'
	domain = conf.get('DOMAIN','domain_name')
	domain_prefix = domain.split('.')[0]
	domain_suffix = '.'.join(domain.split('.')[1:])
	
	tagdict = {'<domain_prefix>' : domain_prefix, '<domain_suffix>' : domain_suffix}
	print host,admin,passwd,tmp_filename,tagdict
	createFromTemplate(host,admin,passwd,tmp_filename,tagdict)
	
	
