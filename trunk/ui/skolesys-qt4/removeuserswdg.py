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

from PyQt4 import QtCore, QtGui
import ui_removeuserswdg as baseui
import connectionmanager as cm
import ss_mainwindow as mainwin

class RemoveUsersWdg(QtGui.QDialog, baseui.Ui_RemoveUsersWdg):
	
	def __init__(self,users_by_mime,parent):
		QtGui.QDialog.__init__(self,parent)
		self.setupUi(self)
		self.users = users_by_mime
		self.setupWidget()
		self.connect(self.btn_ok,QtCore.SIGNAL('clicked()'),self.accept)
		self.connect(self.btn_cancel,QtCore.SIGNAL('clicked()'),self.reject)

	def setupWidget(self):
		for user in self.users:
			self.lb_users.addItem(QtCore.QString().fromUtf8(user['cn']))

	def accept(self):
		answer = QtGui.QMessageBox.question(self,
			self.tr('Remove user(s)'),
			self.tr('Are you sure you want to perform this remove operation?'),
			QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
		if answer==QtGui.QMessageBox.No:
			return
		proxy = cm.get_proxy_handle()
		for user in self.users:
			proxy.removeuser(user['uid'],self.chk_backup_home.isChecked(),self.chk_remove_home.isChecked())
		
		# Signal user deletion
		mainwin.get_mainwindow().emitUserDeleted('dummy')
		QtGui.QDialog.accept(self)
