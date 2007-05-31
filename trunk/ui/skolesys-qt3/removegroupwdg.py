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
from removegroupwdgbase import RemoveGroupWdgBase
from qt import *

class RemoveGroupWdg(RemoveGroupWdgBase):
	def __init__(self,conn,groupnames,parent = None,name = None,fl = 0):
		RemoveGroupWdgBase.__init__(self,parent,name,fl)
		self.groupnames = groupnames
		for groupname in groupnames:
			self.lb_groupnames.insertItem(QString.fromUtf8(groupname))
		self.proxy = conn.get_proxy_handle()

	def accept(self):
		answer = QMessageBox.question(self,
			self.tr('Remove group(s)'),
			self.tr('Are you sure you want to perform this remove operation?'),
			QMessageBox.Yes,QMessageBox.No)
		if answer==QMessageBox.No:
			return False
		for groupname in self.groupnames:
			self.proxy.removegroup(groupname,self.chb_backup_home.isChecked(),self.chb_remove_home.isChecked())
		return True
