# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_loginwdg.ui'
#
# Created: Fri Aug  3 08:57:21 2007
#      by: PyQt4 UI code generator 4.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_LoginWdg(object):
    def setupUi(self, LoginWdg):
        LoginWdg.setObjectName("LoginWdg")
        LoginWdg.resize(QtCore.QSize(QtCore.QRect(0,0,274,146).size()).expandedTo(LoginWdg.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(LoginWdg)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.btn_login = QtGui.QPushButton(LoginWdg)
        self.btn_login.setObjectName("btn_login")
        self.gridlayout.addWidget(self.btn_login,1,1,1,1)

        spacerItem = QtGui.QSpacerItem(151,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,1,0,1,1)

        self.groupBox = QtGui.QGroupBox(LoginWdg)
        self.groupBox.setObjectName("groupBox")

        self.gridlayout1 = QtGui.QGridLayout(self.groupBox)
        self.gridlayout1.setMargin(9)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridlayout1.addWidget(self.label_2,1,0,1,1)

        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridlayout1.addWidget(self.label,0,0,1,1)

        self.ed_passwd = QtGui.QLineEdit(self.groupBox)
        self.ed_passwd.setEchoMode(QtGui.QLineEdit.Password)
        self.ed_passwd.setObjectName("ed_passwd")
        self.gridlayout1.addWidget(self.ed_passwd,1,1,1,1)

        self.ed_username = QtGui.QLineEdit(self.groupBox)
        self.ed_username.setObjectName("ed_username")
        self.gridlayout1.addWidget(self.ed_username,0,1,1,1)
        self.gridlayout.addWidget(self.groupBox,0,0,1,2)

        self.retranslateUi(LoginWdg)
        QtCore.QMetaObject.connectSlotsByName(LoginWdg)
        LoginWdg.setTabOrder(self.ed_username,self.ed_passwd)
        LoginWdg.setTabOrder(self.ed_passwd,self.btn_login)

    def retranslateUi(self, LoginWdg):
        LoginWdg.setWindowTitle(QtGui.QApplication.translate("LoginWdg", "Login", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_login.setText(QtGui.QApplication.translate("LoginWdg", "Login", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("LoginWdg", "Type credentials", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("LoginWdg", "Password", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("LoginWdg", "Username", None, QtGui.QApplication.UnicodeUTF8))

