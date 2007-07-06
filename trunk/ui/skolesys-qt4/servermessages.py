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

import connectionmanager as cm
from PyQt4 import QtCore

class ServerMessages:
	def __init__(self,lang):
		self.lang = lang
	
	def tr(self,domain,msg,lang=None):
		if lang == None:
			lang = self.lang
		proxy = cm.get_proxy_handle()
		print lang
		return proxy.tr(domain,msg,lang)

	def q_tr(self,domain,msg,lang=None):
		return QtCore.QString().fromUtf8(self.tr(domain,msg,lang))

server_messages = None
def init_server_messages(lang):
	print lang
	global server_messages
	server_messages = ServerMessages(lang)
	
def get_translator():
	global server_messages
	return server_messages
