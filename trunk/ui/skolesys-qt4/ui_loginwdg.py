# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_loginwdg.ui'
#
# Created: Sun Aug 26 00:46:23 2007
#      by: PyQt4 UI code generator 4.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_LoginWdg(object):
    def setupUi(self, LoginWdg):
        LoginWdg.setObjectName("LoginWdg")
        LoginWdg.resize(QtCore.QSize(QtCore.QRect(0,0,428,243).size()).expandedTo(LoginWdg.minimumSizeHint()))

        self.btn_login = QtGui.QPushButton(LoginWdg)
        self.btn_login.setGeometry(QtCore.QRect(240,190,75,27))
        self.btn_login.setObjectName("btn_login")

        self.label_2 = QtGui.QLabel(LoginWdg)
        self.label_2.setGeometry(QtCore.QRect(83,160,61,23))
        self.label_2.setObjectName("label_2")

        self.ed_passwd = QtGui.QLineEdit(LoginWdg)
        self.ed_passwd.setGeometry(QtCore.QRect(150,160,167,23))
        self.ed_passwd.setEchoMode(QtGui.QLineEdit.Password)
        self.ed_passwd.setObjectName("ed_passwd")

        self.label = QtGui.QLabel(LoginWdg)
        self.label.setGeometry(QtCore.QRect(83,129,61,23))
        self.label.setObjectName("label")

        self.ed_username = QtGui.QLineEdit(LoginWdg)
        self.ed_username.setGeometry(QtCore.QRect(150,129,167,23))
        self.ed_username.setObjectName("ed_username")

        self.label_3 = QtGui.QLabel(LoginWdg)
        self.label_3.setGeometry(QtCore.QRect(10,10,400,108))
        self.label_3.setPixmap(QtGui.QPixmap("art/biglogo.png"))
        self.label_3.setObjectName("label_3")

        self.retranslateUi(LoginWdg)
        QtCore.QMetaObject.connectSlotsByName(LoginWdg)
        LoginWdg.setTabOrder(self.ed_username,self.ed_passwd)
        LoginWdg.setTabOrder(self.ed_passwd,self.btn_login)

    def retranslateUi(self, LoginWdg):
        LoginWdg.setWindowTitle(QtGui.QApplication.translate("LoginWdg", "Login", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_login.setText(QtGui.QApplication.translate("LoginWdg", "Login", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("LoginWdg", "Password", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("LoginWdg", "Username", None, QtGui.QApplication.UnicodeUTF8))

