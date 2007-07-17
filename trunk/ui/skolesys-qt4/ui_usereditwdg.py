# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_usereditwdg.ui'
#
# Created: Sun Jul  8 11:01:53 2007
#      by: PyQt4 UI code generator 4.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_UserEditWdg(object):
    def setupUi(self, UserEditWdg):
        UserEditWdg.setObjectName("UserEditWdg")
        UserEditWdg.resize(QtCore.QSize(QtCore.QRect(0,0,392,476).size()).expandedTo(UserEditWdg.minimumSizeHint()))
        UserEditWdg.setAcceptDrops(True)

        self.gridlayout = QtGui.QGridLayout(UserEditWdg)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        spacerItem = QtGui.QSpacerItem(20,16,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Fixed)
        self.gridlayout.addItem(spacerItem,6,1,1,2)

        self.btn_apply = QtGui.QPushButton(UserEditWdg)
        self.btn_apply.setEnabled(False)
        self.btn_apply.setObjectName("btn_apply")
        self.gridlayout.addWidget(self.btn_apply,9,3,1,1)

        self.label_6 = QtGui.QLabel(UserEditWdg)
        self.label_6.setObjectName("label_6")
        self.gridlayout.addWidget(self.label_6,5,0,1,1)

        self.label_5 = QtGui.QLabel(UserEditWdg)
        self.label_5.setObjectName("label_5")
        self.gridlayout.addWidget(self.label_5,4,0,1,1)

        self.label_4 = QtGui.QLabel(UserEditWdg)
        self.label_4.setObjectName("label_4")
        self.gridlayout.addWidget(self.label_4,3,0,1,1)

        self.label_3 = QtGui.QLabel(UserEditWdg)
        self.label_3.setEnabled(False)
        self.label_3.setObjectName("label_3")
        self.gridlayout.addWidget(self.label_3,2,0,1,1)

        self.label_7 = QtGui.QLabel(UserEditWdg)
        self.label_7.setObjectName("label_7")
        self.gridlayout.addWidget(self.label_7,1,0,1,1)

        self.label_2 = QtGui.QLabel(UserEditWdg)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2,0,0,1,1)

        self.btn_passwd = QtGui.QPushButton(UserEditWdg)
        self.btn_passwd.setObjectName("btn_passwd")
        self.gridlayout.addWidget(self.btn_passwd,9,0,1,2)

        self.lbl_usertype = QtGui.QLabel(UserEditWdg)
        self.lbl_usertype.setObjectName("lbl_usertype")
        self.gridlayout.addWidget(self.lbl_usertype,0,1,1,3)

        self.lbl_username = QtGui.QLabel(UserEditWdg)
        self.lbl_username.setObjectName("lbl_username")
        self.gridlayout.addWidget(self.lbl_username,1,1,1,3)

        self.sbx_first_school_year = QtGui.QSpinBox(UserEditWdg)
        self.sbx_first_school_year.setEnabled(False)
        self.sbx_first_school_year.setMaximum(2050)
        self.sbx_first_school_year.setMinimum(1990)
        self.sbx_first_school_year.setProperty("value",QtCore.QVariant(1990))
        self.sbx_first_school_year.setObjectName("sbx_first_school_year")
        self.gridlayout.addWidget(self.sbx_first_school_year,2,1,1,3)

        self.led_firstname = QtGui.QLineEdit(UserEditWdg)
        self.led_firstname.setObjectName("led_firstname")
        self.gridlayout.addWidget(self.led_firstname,3,1,1,3)

        self.led_lastname = QtGui.QLineEdit(UserEditWdg)
        self.led_lastname.setObjectName("led_lastname")
        self.gridlayout.addWidget(self.led_lastname,4,1,1,3)

        self.cmb_primary_group = QtGui.QComboBox(UserEditWdg)
        self.cmb_primary_group.setObjectName("cmb_primary_group")
        self.gridlayout.addWidget(self.cmb_primary_group,5,1,1,3)

        self.label = QtGui.QLabel(UserEditWdg)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,7,0,1,4)

        spacerItem1 = QtGui.QSpacerItem(161,27,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem1,9,2,1,1)

        self.trv_groups = EnhancedTreeView(UserEditWdg)
        self.trv_groups.setAcceptDrops(True)
        self.trv_groups.setAlternatingRowColors(True)
        self.trv_groups.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.trv_groups.setRootIsDecorated(False)
        self.trv_groups.setSortingEnabled(True)
        self.trv_groups.setObjectName("trv_groups")
        self.gridlayout.addWidget(self.trv_groups,8,0,1,4)

        self.retranslateUi(UserEditWdg)
        QtCore.QMetaObject.connectSlotsByName(UserEditWdg)
        UserEditWdg.setTabOrder(self.sbx_first_school_year,self.led_firstname)
        UserEditWdg.setTabOrder(self.led_firstname,self.led_lastname)
        UserEditWdg.setTabOrder(self.led_lastname,self.cmb_primary_group)
        UserEditWdg.setTabOrder(self.cmb_primary_group,self.trv_groups)
        UserEditWdg.setTabOrder(self.trv_groups,self.btn_passwd)
        UserEditWdg.setTabOrder(self.btn_passwd,self.btn_apply)

    def retranslateUi(self, UserEditWdg):
        UserEditWdg.setWindowTitle(QtGui.QApplication.translate("UserEditWdg", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_apply.setText(QtGui.QApplication.translate("UserEditWdg", "Apply", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("UserEditWdg", "Primary group:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("UserEditWdg", "Last name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("UserEditWdg", "First name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("UserEditWdg", "First school year:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("UserEditWdg", "Login name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("UserEditWdg", "User type:", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_passwd.setText(QtGui.QApplication.translate("UserEditWdg", "Change password...", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_usertype.setText(QtGui.QApplication.translate("UserEditWdg", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_username.setText(QtGui.QApplication.translate("UserEditWdg", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("UserEditWdg", "Secondary groups:", None, QtGui.QApplication.UnicodeUTF8))

from pyqtui4.enhancedtreeview import EnhancedTreeView
