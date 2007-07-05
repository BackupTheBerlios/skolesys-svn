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
import ui_tooltabwdg as baseui
import pyqtui4.qt4tools as qt4tools
import pyqtui4.actionrequester as ar
import ss_mainwindow as mainwin
import paths
import connectionmanager as cm

class ToolTabWdg(QtGui.QWidget, baseui.Ui_ToolTabWdg,ar.ActionRequester):
	
	def __init__(self,parent):
		QtGui.QWidget.__init__(self,parent)
		ar.ActionRequester.__init__(self)
		self.setupUi(self)
		self.btn_new_user.setIcon(QtGui.QIcon(qt4tools.svg2pixmap(paths.path_to('art/new_user.svg'),72,72)))
		self.connect(self.btn_new_user,QtCore.SIGNAL("clicked()"),self.execCreateUserWizard)
		self.connect(self.btn_new_group,QtCore.SIGNAL("clicked()"),self.execCreateGroupWizard)
		self.connect(self.btn_open_fileman,QtCore.SIGNAL("clicked()"),self.openFileManager)
		self.connect(mainwin.get_mainwindow(),QtCore.SIGNAL("permissionsChanged"),self.setupPermissions)
		self.btn_new_group.setIcon(QtGui.QIcon(qt4tools.svg2pixmap(paths.path_to('art/new_group.svg'),72,72)))
		self.setupPermissions(cm.get_proxy_handle().list_my_permissions())
		
		
	def execCreateUserWizard(self):
		import ss_mainwindow as mainwin
		mainwin.get_mainwindow().execCreateUserWizard()

	def execCreateGroupWizard(self):
		import ss_mainwindow as mainwin
		mainwin.get_mainwindow().execCreateGroupWizard()
	
	def openFileManager(self):
		import ss_mainwindow as mainwin
		mainwin.get_mainwindow().openFileManager()
	
	def setupPermissions(self,access_idents):
		button_map_perm = {
			self.btn_new_user : 'user.create',
			self.btn_new_group : 'group.create',
			self.btn_open_fileman : 'filestats.browse'
		}
		for btn,acc_ident in button_map_perm.items():
			if not access_idents.count(acc_ident):
				btn.setDisabled(True)
			else:
				btn.setDisabled(False)
				