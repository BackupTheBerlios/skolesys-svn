# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_changepasswordwdg.ui'
#
# Created: Sat Jul  7 20:29:14 2007
#      by: PyQt4 UI code generator 4.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_ChangePasswordWdg(object):
    def setupUi(self, ChangePasswordWdg):
        ChangePasswordWdg.setObjectName("ChangePasswordWdg")
        ChangePasswordWdg.resize(QtCore.QSize(QtCore.QRect(0,0,400,189).size()).expandedTo(ChangePasswordWdg.minimumSizeHint()))
        ChangePasswordWdg.setMinimumSize(QtCore.QSize(400,189))
        ChangePasswordWdg.setMaximumSize(QtCore.QSize(400,189))

        self.gridlayout = QtGui.QGridLayout(ChangePasswordWdg)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.groupBox = QtGui.QGroupBox(ChangePasswordWdg)
        self.groupBox.setObjectName("groupBox")

        self.gridlayout1 = QtGui.QGridLayout(self.groupBox)
        self.gridlayout1.setMargin(9)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.gridlayout1.addWidget(self.label_3,0,0,1,2)

        self.led_passwd_confirm = QtGui.QLineEdit(self.groupBox)
        self.led_passwd_confirm.setEchoMode(QtGui.QLineEdit.Password)
        self.led_passwd_confirm.setObjectName("led_passwd_confirm")
        self.gridlayout1.addWidget(self.led_passwd_confirm,2,1,1,1)

        self.led_passwd = QtGui.QLineEdit(self.groupBox)
        self.led_passwd.setEchoMode(QtGui.QLineEdit.Password)
        self.led_passwd.setObjectName("led_passwd")
        self.gridlayout1.addWidget(self.led_passwd,1,1,1,1)

        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridlayout1.addWidget(self.label_2,2,0,1,1)

        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridlayout1.addWidget(self.label,1,0,1,1)
        self.gridlayout.addWidget(self.groupBox,0,0,1,3)

        spacerItem = QtGui.QSpacerItem(171,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,1,0,1,1)

        self.btn_cancel = QtGui.QPushButton(ChangePasswordWdg)
        self.btn_cancel.setObjectName("btn_cancel")
        self.gridlayout.addWidget(self.btn_cancel,1,2,1,1)

        self.btn_ok = QtGui.QPushButton(ChangePasswordWdg)
        self.btn_ok.setEnabled(False)
        self.btn_ok.setObjectName("btn_ok")
        self.gridlayout.addWidget(self.btn_ok,1,1,1,1)

        self.retranslateUi(ChangePasswordWdg)
        QtCore.QMetaObject.connectSlotsByName(ChangePasswordWdg)
        ChangePasswordWdg.setTabOrder(self.led_passwd,self.led_passwd_confirm)
        ChangePasswordWdg.setTabOrder(self.led_passwd_confirm,self.btn_ok)
        ChangePasswordWdg.setTabOrder(self.btn_ok,self.btn_cancel)

    def retranslateUi(self, ChangePasswordWdg):
        ChangePasswordWdg.setWindowTitle(QtGui.QApplication.translate("ChangePasswordWdg", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("ChangePasswordWdg", "Input the new password", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("ChangePasswordWdg", "The password must be at least 3 characters of length but the advised length is minimum 8 characters.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("ChangePasswordWdg", "Repeat:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ChangePasswordWdg", "New password:", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_cancel.setText(QtGui.QApplication.translate("ChangePasswordWdg", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_ok.setText(QtGui.QApplication.translate("ChangePasswordWdg", "OK", None, QtGui.QApplication.UnicodeUTF8))

