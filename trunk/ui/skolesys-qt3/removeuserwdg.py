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
from removeuserwdgbase import RemoveUserWdgBase
from qt import *

class RemoveUserWdg(RemoveUserWdgBase):
	def __init__(self,conn,uids,parent = None,name = None,fl = 0):
		RemoveUserWdgBase.__init__(self,parent,name,fl)
		self.uids = uids
		for uid in uids:
			self.lb_users.insertItem(uid)
		self.proxy = conn.get_proxy_handle()

	def accept(self):
		answer = QMessageBox.question(self,
			self.tr('Remove user(s)'),
			self.tr('Are you sure you want to perform this remove operation?'),
			QMessageBox.Yes,QMessageBox.No)
		if answer==QMessageBox.No:
			return False
		for uid in self.uids:
			self.proxy.removeuser(uid,self.chb_backup_home.isChecked(),self.chb_remove_home.isChecked())
		return True
