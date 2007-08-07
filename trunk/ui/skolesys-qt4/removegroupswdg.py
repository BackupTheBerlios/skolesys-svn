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
import ui_removegroupswdg as baseui
import connectionmanager as cm
import ss_mainwindow as mainwin

class RemoveGroupsWdg(QtGui.QDialog, baseui.Ui_RemoveGroupsWdg):
	
	def __init__(self,groups_by_mime,parent):
		QtGui.QDialog.__init__(self,parent)
		self.setupUi(self)
		self.groups = groups_by_mime
		self.setupWidget()
		self.connect(self.btn_ok,QtCore.SIGNAL('clicked()'),self.accept)
		self.connect(self.btn_cancel,QtCore.SIGNAL('clicked()'),self.reject)

	def setupWidget(self):
		for group in self.groups:
			self.lb_groups.addItem(QtCore.QString().fromUtf8(group['displayed_name']))

	def accept(self):
		answer = QtGui.QMessageBox.question(self,
			self.tr('Remove group(s)'),
			self.tr('Are you sure you want to perform this remove operation?'),
			QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
		if answer==QtGui.QMessageBox.No:
			return
		proxy = cm.get_proxy_handle()
		for group in self.groups:
			proxy.removegroup(group['groupname'],self.chk_backup_home.isChecked(),self.chk_remove_home.isChecked())
		
		# Signal group deletion
		mainwin.get_mainwindow().emitGroupDeleted('dummy')
		QtGui.QDialog.accept(self)
