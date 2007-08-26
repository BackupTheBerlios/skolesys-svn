# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_addremoveusergroupswdg.ui'
#
# Created: Sun Aug 26 13:54:01 2007
#      by: PyQt4 UI code generator 4.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_AddRemoveUserGroupsWdg(object):
    def setupUi(self, AddRemoveUserGroupsWdg):
        AddRemoveUserGroupsWdg.setObjectName("AddRemoveUserGroupsWdg")
        AddRemoveUserGroupsWdg.resize(QtCore.QSize(QtCore.QRect(0,0,664,770).size()).expandedTo(AddRemoveUserGroupsWdg.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(AddRemoveUserGroupsWdg)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.grp_main = QtGui.QGroupBox(AddRemoveUserGroupsWdg)
        self.grp_main.setObjectName("grp_main")

        self.gridlayout1 = QtGui.QGridLayout(self.grp_main)
        self.gridlayout1.setMargin(9)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        self.trv_remove = EnhancedTreeView(self.grp_main)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(13),QtGui.QSizePolicy.Policy(3))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.trv_remove.sizePolicy().hasHeightForWidth())
        self.trv_remove.setSizePolicy(sizePolicy)
        self.trv_remove.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.trv_remove.setAcceptDrops(True)
        self.trv_remove.setDragEnabled(True)
        self.trv_remove.setAlternatingRowColors(True)
        self.trv_remove.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.trv_remove.setRootIsDecorated(False)
        self.trv_remove.setSortingEnabled(True)
        self.trv_remove.setObjectName("trv_remove")
        self.gridlayout1.addWidget(self.trv_remove,4,1,1,1)

        self.trv_add = EnhancedTreeView(self.grp_main)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(13),QtGui.QSizePolicy.Policy(3))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.trv_add.sizePolicy().hasHeightForWidth())
        self.trv_add.setSizePolicy(sizePolicy)
        self.trv_add.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.trv_add.setAcceptDrops(True)
        self.trv_add.setDragEnabled(True)
        self.trv_add.setAlternatingRowColors(True)
        self.trv_add.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.trv_add.setRootIsDecorated(False)
        self.trv_add.setSortingEnabled(True)
        self.trv_add.setObjectName("trv_add")
        self.gridlayout1.addWidget(self.trv_add,2,1,1,1)

        self.trv_available = EnhancedTreeView(self.grp_main)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(13),QtGui.QSizePolicy.Policy(3))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.trv_available.sizePolicy().hasHeightForWidth())
        self.trv_available.setSizePolicy(sizePolicy)
        self.trv_available.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.trv_available.setAcceptDrops(True)
        self.trv_available.setDragEnabled(True)
        self.trv_available.setAlternatingRowColors(True)
        self.trv_available.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.trv_available.setRootIsDecorated(False)
        self.trv_available.setSortingEnabled(True)
        self.trv_available.setObjectName("trv_available")
        self.gridlayout1.addWidget(self.trv_available,2,0,3,1)

        self.label_3 = QtGui.QLabel(self.grp_main)
        self.label_3.setObjectName("label_3")
        self.gridlayout1.addWidget(self.label_3,1,1,1,1)

        self.label = QtGui.QLabel(self.grp_main)
        self.label.setObjectName("label")
        self.gridlayout1.addWidget(self.label,1,0,1,1)

        self.label_2 = QtGui.QLabel(self.grp_main)
        self.label_2.setObjectName("label_2")
        self.gridlayout1.addWidget(self.label_2,3,1,1,1)

        self.trv_users = EnhancedTreeView(self.grp_main)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(13),QtGui.QSizePolicy.Policy(3))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.trv_users.sizePolicy().hasHeightForWidth())
        self.trv_users.setSizePolicy(sizePolicy)
        self.trv_users.setFocusPolicy(QtCore.Qt.NoFocus)
        self.trv_users.setAlternatingRowColors(True)
        self.trv_users.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.trv_users.setRootIsDecorated(False)
        self.trv_users.setSortingEnabled(True)
        self.trv_users.setObjectName("trv_users")
        self.gridlayout1.addWidget(self.trv_users,0,0,1,2)
        self.gridlayout.addWidget(self.grp_main,0,0,1,3)

        spacerItem = QtGui.QSpacerItem(361,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,1,0,1,1)

        self.btn_ok = QtGui.QPushButton(AddRemoveUserGroupsWdg)
        self.btn_ok.setObjectName("btn_ok")
        self.gridlayout.addWidget(self.btn_ok,1,1,1,1)

        self.btn_cancel = QtGui.QPushButton(AddRemoveUserGroupsWdg)
        self.btn_cancel.setObjectName("btn_cancel")
        self.gridlayout.addWidget(self.btn_cancel,1,2,1,1)

        self.retranslateUi(AddRemoveUserGroupsWdg)
        QtCore.QMetaObject.connectSlotsByName(AddRemoveUserGroupsWdg)
        AddRemoveUserGroupsWdg.setTabOrder(self.trv_available,self.trv_add)
        AddRemoveUserGroupsWdg.setTabOrder(self.trv_add,self.trv_remove)
        AddRemoveUserGroupsWdg.setTabOrder(self.trv_remove,self.btn_ok)
        AddRemoveUserGroupsWdg.setTabOrder(self.btn_ok,self.btn_cancel)

    def retranslateUi(self, AddRemoveUserGroupsWdg):
        AddRemoveUserGroupsWdg.setWindowTitle(QtGui.QApplication.translate("AddRemoveUserGroupsWdg", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.grp_main.setTitle(QtGui.QApplication.translate("AddRemoveUserGroupsWdg", "Modify memberships if following user(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("AddRemoveUserGroupsWdg", "Add membership:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("AddRemoveUserGroupsWdg", "Available groups:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("AddRemoveUserGroupsWdg", "Remove membership:", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_ok.setText(QtGui.QApplication.translate("AddRemoveUserGroupsWdg", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_cancel.setText(QtGui.QApplication.translate("AddRemoveUserGroupsWdg", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

from pyqtui4.enhancedtreeview import EnhancedTreeView
