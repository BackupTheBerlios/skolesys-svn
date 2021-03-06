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
import sys
from qt import *
from skolesys.soap.client import SkoleSYS_Client
import pickle

class ConnectionManager:
	def __init__(self,host,port):
		self.proxy = SkoleSYS_Client(host,port)
		
	def get_proxy_handle(self):
		counter = 0
		while not self.proxy.test_binded() and counter<3:
			passwd = QInputDialog.getText(qApp.translate("General","SkoleSYS Administration"), qApp.translate("General","Enter administrator password"), QLineEdit.Password)
			if passwd[1]==False:
				sys.exit(0)
			if self.proxy.bind(str(passwd[0].utf8())):
				break
			counter+=1
		if counter>=3:
			print "The connection manager has cut this session from further use"
			sys.exit(0)
		return self.proxy

if __name__=='__main__':
	a = QApplication(sys.argv)
	cm = ConnectionManager('https://mainserver.localnet',10033)
	if cm.get_proxy_handle():
		print "OK"

