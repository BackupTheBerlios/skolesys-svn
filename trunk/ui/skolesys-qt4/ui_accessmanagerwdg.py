# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_accessmanagerwdg.ui'
#
# Created: Sun Jul  8 11:01:53 2007
#      by: PyQt4 UI code generator 4.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_AccessManagerWdg(object):
    def setupUi(self, AccessManagerWdg):
        AccessManagerWdg.setObjectName("AccessManagerWdg")
        AccessManagerWdg.resize(QtCore.QSize(QtCore.QRect(0,0,709,563).size()).expandedTo(AccessManagerWdg.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(AccessManagerWdg)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.splitter = QtGui.QSplitter(AccessManagerWdg)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")

        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")

        self.vboxlayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.vboxlayout.setMargin(0)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.label_2 = QtGui.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.vboxlayout.addWidget(self.label_2)

        self.trv_userlist = EnhancedTreeView(self.layoutWidget)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(1),QtGui.QSizePolicy.Policy(7))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.trv_userlist.sizePolicy().hasHeightForWidth())
        self.trv_userlist.setSizePolicy(sizePolicy)
        self.trv_userlist.setAlternatingRowColors(True)
        self.trv_userlist.setRootIsDecorated(False)
        self.trv_userlist.setObjectName("trv_userlist")
        self.vboxlayout.addWidget(self.trv_userlist)

        self.layoutWidget1 = QtGui.QWidget(self.splitter)
        self.layoutWidget1.setObjectName("layoutWidget1")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.layoutWidget1)
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.label = QtGui.QLabel(self.layoutWidget1)
        self.label.setObjectName("label")
        self.vboxlayout1.addWidget(self.label)

        self.trw_access_idents = QtGui.QTreeWidget(self.layoutWidget1)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(3),QtGui.QSizePolicy.Policy(7))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.trw_access_idents.sizePolicy().hasHeightForWidth())
        self.trw_access_idents.setSizePolicy(sizePolicy)
        self.trw_access_idents.setAlternatingRowColors(True)
        self.trw_access_idents.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.trw_access_idents.setObjectName("trw_access_idents")
        self.vboxlayout1.addWidget(self.trw_access_idents)
        self.gridlayout.addWidget(self.splitter,0,0,1,1)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        spacerItem = QtGui.QSpacerItem(391,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)

        self.btn_close = QtGui.QPushButton(AccessManagerWdg)
        self.btn_close.setObjectName("btn_close")
        self.hboxlayout.addWidget(self.btn_close)
        self.gridlayout.addLayout(self.hboxlayout,1,0,1,1)

        self.retranslateUi(AccessManagerWdg)
        QtCore.QMetaObject.connectSlotsByName(AccessManagerWdg)

    def retranslateUi(self, AccessManagerWdg):
        AccessManagerWdg.setWindowTitle(QtGui.QApplication.translate("AccessManagerWdg", "Access Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("AccessManagerWdg", "Users:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("AccessManagerWdg", "Permissions:", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_close.setText(QtGui.QApplication.translate("AccessManagerWdg", "Close", None, QtGui.QApplication.UnicodeUTF8))

from pyqtui4.enhancedtreeview import EnhancedTreeView
