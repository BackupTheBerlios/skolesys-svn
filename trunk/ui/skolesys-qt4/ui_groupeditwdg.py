# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_groupeditwdg.ui'
#
# Created: Sun Jul  8 11:01:52 2007
#      by: PyQt4 UI code generator 4.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_GroupEditWdg(object):
    def setupUi(self, GroupEditWdg):
        GroupEditWdg.setObjectName("GroupEditWdg")
        GroupEditWdg.resize(QtCore.QSize(QtCore.QRect(0,0,541,613).size()).expandedTo(GroupEditWdg.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(GroupEditWdg)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.splitter = QtGui.QSplitter(GroupEditWdg)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")

        self.grp_members = QtGui.QGroupBox(self.splitter)
        self.grp_members.setObjectName("grp_members")

        self.gridlayout1 = QtGui.QGridLayout(self.grp_members)
        self.gridlayout1.setMargin(9)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        self.trv_users = EnhancedTreeView(self.grp_members)
        self.trv_users.setAcceptDrops(True)
        self.trv_users.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.trv_users.setRootIsDecorated(False)
        self.trv_users.setSortingEnabled(True)
        self.trv_users.setObjectName("trv_users")
        self.gridlayout1.addWidget(self.trv_users,0,0,1,1)

        self.grp_services = QtGui.QGroupBox(self.splitter)
        self.grp_services.setObjectName("grp_services")

        self.gridlayout2 = QtGui.QGridLayout(self.grp_services)
        self.gridlayout2.setMargin(9)
        self.gridlayout2.setSpacing(6)
        self.gridlayout2.setObjectName("gridlayout2")

        self.btn_add_service = QtGui.QToolButton(self.grp_services)
        self.btn_add_service.setObjectName("btn_add_service")
        self.gridlayout2.addWidget(self.btn_add_service,0,1,1,1)

        self.cmb_services = QtGui.QComboBox(self.grp_services)
        self.cmb_services.setObjectName("cmb_services")
        self.gridlayout2.addWidget(self.cmb_services,0,0,1,1)

        self.tbl_serviceoptions = OptionsTableView(self.grp_services)
        self.tbl_serviceoptions.setAlternatingRowColors(True)
        self.tbl_serviceoptions.setRootIsDecorated(False)
        self.tbl_serviceoptions.setObjectName("tbl_serviceoptions")
        self.gridlayout2.addWidget(self.tbl_serviceoptions,1,0,1,2)
        self.gridlayout.addWidget(self.splitter,3,0,1,3)

        self.label_2 = QtGui.QLabel(GroupEditWdg)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(5),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2,1,0,1,3)

        self.lbl_groupname = QtGui.QLabel(GroupEditWdg)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(5),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_groupname.sizePolicy().hasHeightForWidth())
        self.lbl_groupname.setSizePolicy(sizePolicy)
        self.lbl_groupname.setObjectName("lbl_groupname")
        self.gridlayout.addWidget(self.lbl_groupname,0,1,1,2)

        self.ted_description = QtGui.QTextEdit(GroupEditWdg)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7),QtGui.QSizePolicy.Policy(7))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ted_description.sizePolicy().hasHeightForWidth())
        self.ted_description.setSizePolicy(sizePolicy)
        self.ted_description.setObjectName("ted_description")
        self.gridlayout.addWidget(self.ted_description,2,0,1,3)

        self.label = QtGui.QLabel(GroupEditWdg)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,0,0,1,1)

        self.btn_apply = QtGui.QPushButton(GroupEditWdg)
        self.btn_apply.setEnabled(False)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_apply.sizePolicy().hasHeightForWidth())
        self.btn_apply.setSizePolicy(sizePolicy)
        self.btn_apply.setObjectName("btn_apply")
        self.gridlayout.addWidget(self.btn_apply,4,2,1,1)

        spacerItem = QtGui.QSpacerItem(421,27,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,4,0,1,2)

        self.retranslateUi(GroupEditWdg)
        QtCore.QMetaObject.connectSlotsByName(GroupEditWdg)

    def retranslateUi(self, GroupEditWdg):
        GroupEditWdg.setWindowTitle(QtGui.QApplication.translate("GroupEditWdg", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.grp_members.setTitle(QtGui.QApplication.translate("GroupEditWdg", "Members", None, QtGui.QApplication.UnicodeUTF8))
        self.grp_services.setTitle(QtGui.QApplication.translate("GroupEditWdg", "Group services", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_add_service.setText(QtGui.QApplication.translate("GroupEditWdg", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("GroupEditWdg", "Description:", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_groupname.setText(QtGui.QApplication.translate("GroupEditWdg", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("GroupEditWdg", "Group Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_apply.setText(QtGui.QApplication.translate("GroupEditWdg", "Apply", None, QtGui.QApplication.UnicodeUTF8))

from optionstableview import OptionsTableView
from pyqtui4.enhancedtreeview import EnhancedTreeView
