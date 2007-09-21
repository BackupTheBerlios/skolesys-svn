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
import ui_changepasswordwdg as baseui


class ChangePasswordWdg(QtGui.QDialog, baseui.Ui_ChangePasswordWdg):
	
	def __init__(self,parent):
		QtGui.QDialog.__init__(self,parent)
		self.setupUi(self)
		self.connect(self.led_passwd,QtCore.SIGNAL('textChanged(const QString&)'),self.textChanged)
		self.connect(self.led_passwd_confirm,QtCore.SIGNAL('textChanged(const QString&)'),self.textChanged)
		self.connect(self.btn_ok,QtCore.SIGNAL('clicked()'),self.accept)
		self.connect(self.btn_cancel,QtCore.SIGNAL('clicked()'),self.reject)
		
	def textChanged(self,txt):
		if len(str(self.led_passwd.text().toUtf8()))>=5 and self.led_passwd.text() == self.led_passwd_confirm.text():
			self.btn_ok.setEnabled(True)
		else:
			self.btn_ok.setEnabled(False)

def promptForPassword():
	ui = ChangePasswordWdg(None)
	res = ui.exec_()
	passwd = None
	if res == QtGui.QDialog.Accepted:
		passwd = str(ui.led_passwd.text().toUtf8())
	return passwd
	

if __name__ == '__main__':
	import sys
	app = QtGui.QApplication(sys.argv)
	ui = ChangePasswordWdg(None)
	
	ui.show()
	sys.exit(app.exec_())
