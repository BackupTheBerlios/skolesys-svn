# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_groupviewwdg.ui'
#
# Created: Sun Aug 26 13:54:01 2007
#      by: PyQt4 UI code generator 4.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_GroupViewWdg(object):
    def setupUi(self, GroupViewWdg):
        GroupViewWdg.setObjectName("GroupViewWdg")
        GroupViewWdg.resize(QtCore.QSize(QtCore.QRect(0,0,338,300).size()).expandedTo(GroupViewWdg.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(GroupViewWdg)
        self.gridlayout.setMargin(4)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName("gridlayout")

        self.trv_grouplist = EnhancedTreeView(GroupViewWdg)
        self.trv_grouplist.setDragEnabled(True)
        self.trv_grouplist.setAlternatingRowColors(True)
        self.trv_grouplist.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.trv_grouplist.setRootIsDecorated(False)
        self.trv_grouplist.setSortingEnabled(True)
        self.trv_grouplist.setObjectName("trv_grouplist")
        self.gridlayout.addWidget(self.trv_grouplist,2,0,1,3)

        spacerItem = QtGui.QSpacerItem(16,22,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,1,1,1,1)

        self.label_2 = QtGui.QLabel(GroupViewWdg)
        self.label_2.setMaximumSize(QtCore.QSize(16777215,15))
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2,0,2,1,1)

        self.cmb_grouptype_filter_2 = QtGui.QComboBox(GroupViewWdg)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(3),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmb_grouptype_filter_2.sizePolicy().hasHeightForWidth())
        self.cmb_grouptype_filter_2.setSizePolicy(sizePolicy)
        self.cmb_grouptype_filter_2.setObjectName("cmb_grouptype_filter_2")
        self.gridlayout.addWidget(self.cmb_grouptype_filter_2,1,2,1,1)

        self.cmb_grouptype_filter = QtGui.QComboBox(GroupViewWdg)
        self.cmb_grouptype_filter.setObjectName("cmb_grouptype_filter")
        self.gridlayout.addWidget(self.cmb_grouptype_filter,1,0,1,1)

        self.label = QtGui.QLabel(GroupViewWdg)
        self.label.setMaximumSize(QtCore.QSize(16777215,15))
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,0,0,1,1)

        self.retranslateUi(GroupViewWdg)
        QtCore.QMetaObject.connectSlotsByName(GroupViewWdg)

    def retranslateUi(self, GroupViewWdg):
        GroupViewWdg.setWindowTitle(QtGui.QApplication.translate("GroupViewWdg", "Group View", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("GroupViewWdg", "User filter", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("GroupViewWdg", "Group type", None, QtGui.QApplication.UnicodeUTF8))

from pyqtui4.enhancedtreeview import EnhancedTreeView
