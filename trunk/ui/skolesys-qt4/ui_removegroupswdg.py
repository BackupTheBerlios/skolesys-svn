# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_removegroupswdg.ui'
#
# Created: Sun Aug 26 13:54:02 2007
#      by: PyQt4 UI code generator 4.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_RemoveGroupsWdg(object):
    def setupUi(self, RemoveGroupsWdg):
        RemoveGroupsWdg.setObjectName("RemoveGroupsWdg")
        RemoveGroupsWdg.resize(QtCore.QSize(QtCore.QRect(0,0,382,351).size()).expandedTo(RemoveGroupsWdg.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(RemoveGroupsWdg)
        self.gridlayout.setObjectName("gridlayout")

        self.lb_groups = QtGui.QListWidget(RemoveGroupsWdg)
        self.lb_groups.setEnabled(False)
        self.lb_groups.setObjectName("lb_groups")
        self.gridlayout.addWidget(self.lb_groups,0,0,1,3)

        self.chk_backup_home = QtGui.QCheckBox(RemoveGroupsWdg)
        self.chk_backup_home.setChecked(True)
        self.chk_backup_home.setObjectName("chk_backup_home")
        self.gridlayout.addWidget(self.chk_backup_home,1,0,1,3)

        self.chk_remove_home = QtGui.QCheckBox(RemoveGroupsWdg)
        self.chk_remove_home.setChecked(True)
        self.chk_remove_home.setObjectName("chk_remove_home")
        self.gridlayout.addWidget(self.chk_remove_home,2,0,1,3)

        spacerItem = QtGui.QSpacerItem(131,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,3,0,1,1)

        self.btn_ok = QtGui.QPushButton(RemoveGroupsWdg)
        self.btn_ok.setObjectName("btn_ok")
        self.gridlayout.addWidget(self.btn_ok,3,1,1,1)

        self.btn_cancel = QtGui.QPushButton(RemoveGroupsWdg)
        self.btn_cancel.setObjectName("btn_cancel")
        self.gridlayout.addWidget(self.btn_cancel,3,2,1,1)

        self.retranslateUi(RemoveGroupsWdg)
        QtCore.QMetaObject.connectSlotsByName(RemoveGroupsWdg)

    def retranslateUi(self, RemoveGroupsWdg):
        RemoveGroupsWdg.setWindowTitle(QtGui.QApplication.translate("RemoveGroupsWdg", "Remove Groups", None, QtGui.QApplication.UnicodeUTF8))
        self.chk_backup_home.setText(QtGui.QApplication.translate("RemoveGroupsWdg", "Backup the group home directories", None, QtGui.QApplication.UnicodeUTF8))
        self.chk_remove_home.setText(QtGui.QApplication.translate("RemoveGroupsWdg", "Remove the group home directories", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_ok.setText(QtGui.QApplication.translate("RemoveGroupsWdg", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_cancel.setText(QtGui.QApplication.translate("RemoveGroupsWdg", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

