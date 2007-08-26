# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_removeuserswdg.ui'
#
# Created: Sun Aug 26 02:03:26 2007
#      by: PyQt4 UI code generator 4.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_RemoveUsersWdg(object):
    def setupUi(self, RemoveUsersWdg):
        RemoveUsersWdg.setObjectName("RemoveUsersWdg")
        RemoveUsersWdg.resize(QtCore.QSize(QtCore.QRect(0,0,382,351).size()).expandedTo(RemoveUsersWdg.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(RemoveUsersWdg)
        self.gridlayout.setObjectName("gridlayout")

        self.lb_users = QtGui.QListWidget(RemoveUsersWdg)
        self.lb_users.setEnabled(False)
        self.lb_users.setObjectName("lb_users")
        self.gridlayout.addWidget(self.lb_users,0,0,1,3)

        self.chk_backup_home = QtGui.QCheckBox(RemoveUsersWdg)
        self.chk_backup_home.setChecked(True)
        self.chk_backup_home.setObjectName("chk_backup_home")
        self.gridlayout.addWidget(self.chk_backup_home,1,0,1,3)

        self.chk_remove_home = QtGui.QCheckBox(RemoveUsersWdg)
        self.chk_remove_home.setChecked(True)
        self.chk_remove_home.setObjectName("chk_remove_home")
        self.gridlayout.addWidget(self.chk_remove_home,2,0,1,3)

        spacerItem = QtGui.QSpacerItem(131,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,3,0,1,1)

        self.btn_ok = QtGui.QPushButton(RemoveUsersWdg)
        self.btn_ok.setObjectName("btn_ok")
        self.gridlayout.addWidget(self.btn_ok,3,1,1,1)

        self.btn_cancel = QtGui.QPushButton(RemoveUsersWdg)
        self.btn_cancel.setObjectName("btn_cancel")
        self.gridlayout.addWidget(self.btn_cancel,3,2,1,1)

        self.retranslateUi(RemoveUsersWdg)
        QtCore.QMetaObject.connectSlotsByName(RemoveUsersWdg)

    def retranslateUi(self, RemoveUsersWdg):
        RemoveUsersWdg.setWindowTitle(QtGui.QApplication.translate("RemoveUsersWdg", "Remove Users", None, QtGui.QApplication.UnicodeUTF8))
        self.chk_backup_home.setText(QtGui.QApplication.translate("RemoveUsersWdg", "Backup the user home directories", None, QtGui.QApplication.UnicodeUTF8))
        self.chk_remove_home.setText(QtGui.QApplication.translate("RemoveUsersWdg", "Remove the user home directories", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_ok.setText(QtGui.QApplication.translate("RemoveUsersWdg", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_cancel.setText(QtGui.QApplication.translate("RemoveUsersWdg", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

