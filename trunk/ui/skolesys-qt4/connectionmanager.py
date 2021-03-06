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
from PyQt4 import QtCore,QtGui
from skolesys.soap.client import SkoleSYS_Client
import loginwdg
import pickle
import accesstools

class ConnectionManager:
	def __init__(self,host,port):
		self.proxy = SkoleSYS_Client(host,port)
		
	def _get_proxy_handle(self):
		counter = 0
		# Check if it is nessecary to request a new session id
		# the SOAP server may have flushed the session info
		if not self.proxy.test_session_id():
			self.proxy._get_id()
			
		while not self.proxy.test_binded() and counter<3:
				
			username,passwd = loginwdg.get_credentials()
			if username==None:
				# Login was cancelled
				sys.exit(0)
			bindres = self.proxy.bind(username,passwd)
			if type(bindres) == bool and bindres==True:	
				self.binded_user = username
				break

			if type(bindres) == int and bindres==-9999:
				# Acess denied
				accesstools.access_denied_dialog('access.soap.bind')
				sys.exit(0)
			counter+=1
		if counter>=3:
			print "The connection manager has cut this session from further use"
			sys.exit(0)
		return self.proxy

conn = None

def setup_connection(host,port):
	global conn
	conn = ConnectionManager(host,port)

def get_connection():
	global conn
	return conn

def get_binded_user():
	global conn
	if not conn:
		return None
	if not conn.proxy.test_binded():
		return None
	return conn.binded_user


def get_raw_proxy_handle():
	"""
	Get the raw (maybe unbinded/unconnected) proxy object.
	It can be used for calling services that don't require
	special access. Such as servermessages.
	"""
	global conn
	if not conn:
		return None
	return conn.proxy
	

def get_proxy_handle():
	global conn
	if not conn:
		return None
	return conn._get_proxy_handle()

if __name__=='__main__':
	a = QtGui.QApplication(sys.argv)
	cm = ConnectionManager('https://mainserver.localnet',10033)
	if cm.get_proxy_handle():
		print "OK"

