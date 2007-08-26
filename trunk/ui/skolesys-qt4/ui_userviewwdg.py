# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_userviewwdg.ui'
#
# Created: Sun Aug 26 13:54:01 2007
#      by: PyQt4 UI code generator 4.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_UserViewWdg(object):
    def setupUi(self, UserViewWdg):
        UserViewWdg.setObjectName("UserViewWdg")
        UserViewWdg.resize(QtCore.QSize(QtCore.QRect(0,0,500,392).size()).expandedTo(UserViewWdg.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(UserViewWdg)
        self.gridlayout.setMargin(4)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName("gridlayout")

        self.trv_userlist = EnhancedTreeView(UserViewWdg)
        self.trv_userlist.setDragEnabled(True)
        self.trv_userlist.setAlternatingRowColors(True)
        self.trv_userlist.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.trv_userlist.setRootIsDecorated(False)
        self.trv_userlist.setSortingEnabled(True)
        self.trv_userlist.setObjectName("trv_userlist")
        self.gridlayout.addWidget(self.trv_userlist,2,0,1,7)

        self.label_4 = QtGui.QLabel(UserViewWdg)
        self.label_4.setMaximumSize(QtCore.QSize(16777215,15))
        self.label_4.setObjectName("label_4")
        self.gridlayout.addWidget(self.label_4,0,6,1,1)

        self.cmb_groupfilter = QtGui.QComboBox(UserViewWdg)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(3),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmb_groupfilter.sizePolicy().hasHeightForWidth())
        self.cmb_groupfilter.setSizePolicy(sizePolicy)
        self.cmb_groupfilter.setObjectName("cmb_groupfilter")
        self.gridlayout.addWidget(self.cmb_groupfilter,1,6,1,1)

        self.label = QtGui.QLabel(UserViewWdg)
        self.label.setMaximumSize(QtCore.QSize(16777215,15))
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,0,0,1,1)

        self.cmb_usertype_filter = QtGui.QComboBox(UserViewWdg)
        self.cmb_usertype_filter.setObjectName("cmb_usertype_filter")
        self.gridlayout.addWidget(self.cmb_usertype_filter,1,0,1,1)

        self.lbl_gradefilter = QtGui.QLabel(UserViewWdg)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(5),QtGui.QSizePolicy.Policy(5))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_gradefilter.sizePolicy().hasHeightForWidth())
        self.lbl_gradefilter.setSizePolicy(sizePolicy)
        self.lbl_gradefilter.setMaximumSize(QtCore.QSize(16777215,15))
        self.lbl_gradefilter.setMargin(0)
        self.lbl_gradefilter.setObjectName("lbl_gradefilter")
        self.gridlayout.addWidget(self.lbl_gradefilter,0,2,1,3)

        self.lbl_gradefilter_to = QtGui.QLabel(UserViewWdg)
        self.lbl_gradefilter_to.setObjectName("lbl_gradefilter_to")
        self.gridlayout.addWidget(self.lbl_gradefilter_to,1,3,1,1)

        self.sbx_firstschoolyear_max = QtGui.QSpinBox(UserViewWdg)
        self.sbx_firstschoolyear_max.setMaximum(12)
        self.sbx_firstschoolyear_max.setProperty("value",QtCore.QVariant(12))
        self.sbx_firstschoolyear_max.setObjectName("sbx_firstschoolyear_max")
        self.gridlayout.addWidget(self.sbx_firstschoolyear_max,1,4,1,1)

        self.sbx_firstschoolyear_min = QtGui.QSpinBox(UserViewWdg)
        self.sbx_firstschoolyear_min.setMaximum(12)
        self.sbx_firstschoolyear_min.setObjectName("sbx_firstschoolyear_min")
        self.gridlayout.addWidget(self.sbx_firstschoolyear_min,1,2,1,1)

        spacerItem = QtGui.QSpacerItem(16,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,1,1,1,1)

        spacerItem1 = QtGui.QSpacerItem(16,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem1,1,5,1,1)

        self.retranslateUi(UserViewWdg)
        QtCore.QMetaObject.connectSlotsByName(UserViewWdg)

    def retranslateUi(self, UserViewWdg):
        UserViewWdg.setWindowTitle(QtGui.QApplication.translate("UserViewWdg", "Group View", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("UserViewWdg", "Group filter", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("UserViewWdg", "User type", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_gradefilter.setText(QtGui.QApplication.translate("UserViewWdg", "Class year", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_gradefilter_to.setText(QtGui.QApplication.translate("UserViewWdg", "to", None, QtGui.QApplication.UnicodeUTF8))

from pyqtui4.enhancedtreeview import EnhancedTreeView
