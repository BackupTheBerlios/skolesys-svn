# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_loginwdg.ui'
#
# Created: Sun Aug 26 02:03:25 2007
#      by: PyQt4 UI code generator 4.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_LoginWdg(object):
    def setupUi(self, LoginWdg):
        LoginWdg.setObjectName("LoginWdg")
        LoginWdg.resize(QtCore.QSize(QtCore.QRect(0,0,428,243).size()).expandedTo(LoginWdg.minimumSizeHint()))

        self.label_3 = QtGui.QLabel(LoginWdg)
        self.label_3.setGeometry(QtCore.QRect(10,10,400,108))
        self.label_3.setPixmap(QtGui.QPixmap("art/biglogo.png"))
        self.label_3.setObjectName("label_3")

        self.widget = QtGui.QWidget(LoginWdg)
        self.widget.setGeometry(QtCore.QRect(90,130,228,91))
        self.widget.setObjectName("widget")

        self.gridlayout = QtGui.QGridLayout(self.widget)
        self.gridlayout.setObjectName("gridlayout")

        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,0,0,1,1)

        self.ed_username = QtGui.QLineEdit(self.widget)
        self.ed_username.setObjectName("ed_username")
        self.gridlayout.addWidget(self.ed_username,0,1,1,2)

        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2,1,0,1,1)

        self.ed_passwd = QtGui.QLineEdit(self.widget)
        self.ed_passwd.setEchoMode(QtGui.QLineEdit.Password)
        self.ed_passwd.setObjectName("ed_passwd")
        self.gridlayout.addWidget(self.ed_passwd,1,1,1,2)

        spacerItem = QtGui.QSpacerItem(141,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,2,0,1,2)

        self.btn_login = QtGui.QPushButton(self.widget)
        self.btn_login.setObjectName("btn_login")
        self.gridlayout.addWidget(self.btn_login,2,2,1,1)

        self.retranslateUi(LoginWdg)
        QtCore.QMetaObject.connectSlotsByName(LoginWdg)
        LoginWdg.setTabOrder(self.ed_username,self.ed_passwd)
        LoginWdg.setTabOrder(self.ed_passwd,self.btn_login)

    def retranslateUi(self, LoginWdg):
        LoginWdg.setWindowTitle(QtGui.QApplication.translate("LoginWdg", "Login", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("LoginWdg", "Username", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("LoginWdg", "Password", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_login.setText(QtGui.QApplication.translate("LoginWdg", "Login", None, QtGui.QApplication.UnicodeUTF8))

