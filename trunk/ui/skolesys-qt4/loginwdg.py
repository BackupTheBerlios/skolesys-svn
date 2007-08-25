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
import ui_loginwdg as baseui
import pyqtui4.qt4tools as qt4tools
import pyqtui4.actionrequester as ar
import paths


class LoginWdg(QtGui.QDialog, baseui.Ui_LoginWdg):
	
	def __init__(self,parent):
		QtGui.QWidget.__init__(self,parent)
		self.setupUi(self)
		self.connect(self.btn_login,QtCore.SIGNAL("clicked()"),self.accept)
		self.connect(self.ed_username,QtCore.SIGNAL("returnPressed()"),self.ed_passwd.setFocus)
		self.connect(self.ed_passwd,QtCore.SIGNAL("returnPressed()"),self.accept)
		self.btn_login.setDefault(False)
		self.btn_login.setAutoDefault(False)
		self.setFixedSize(self.size())
		
	
def get_credentials():
	ui = LoginWdg(None)
	if ui.exec_()==QtGui.QDialog.Accepted:
		return (str(ui.ed_username.text().toUtf8()),str(ui.ed_passwd.text().toUtf8()))
	else:
		return None,None

if __name__ == '__main__':
	import sys
	app = QtGui.QApplication(sys.argv)
	ui = LoginWdg(None)
	
	ui.show()
	sys.exit(app.exec_())
