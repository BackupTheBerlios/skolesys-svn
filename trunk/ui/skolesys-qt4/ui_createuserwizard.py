# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_createuserwizard.ui'
#
# Created: Tue Feb 27 23:56:55 2007
#      by: PyQt4 UI code generator 4.0.1
#
# WARNING! All changes made in this file will be lost!

import sys
from pyqtui4.enhancedtreeview import EnhancedTreeView
from PyQt4 import QtCore, QtGui

class Ui_CreateUserWizard(object):
    def setupUi(self, CreateUserWizard):
        CreateUserWizard.setObjectName("CreateUserWizard")
        CreateUserWizard.resize(QtCore.QSize(QtCore.QRect(0,0,437,350).size()).expandedTo(CreateUserWizard.minimumSizeHint()))

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(5),QtGui.QSizePolicy.Policy(5))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CreateUserWizard.sizePolicy().hasHeightForWidth())
        CreateUserWizard.setSizePolicy(sizePolicy)
        CreateUserWizard.setMinimumSize(QtCore.QSize(0,350))
        CreateUserWizard.setMaximumSize(QtCore.QSize(16777215,350))

        self.vboxlayout = QtGui.QVBoxLayout(CreateUserWizard)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.swd_userinfo = QtGui.QStackedWidget(CreateUserWizard)
        self.swd_userinfo.setObjectName("swd_userinfo")

        self.page = QtGui.QWidget()
        self.page.setObjectName("page")

        self.gridlayout = QtGui.QGridLayout(self.page)
        self.gridlayout.setMargin(0)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.label_4 = QtGui.QLabel(self.page)
        self.label_4.setObjectName("label_4")
        self.gridlayout.addWidget(self.label_4,5,2,1,1)

        self.sbx_first_school_year = QtGui.QSpinBox(self.page)
        self.sbx_first_school_year.setEnabled(False)
        self.sbx_first_school_year.setMaximum(2020)
        self.sbx_first_school_year.setMinimum(1996)
        self.sbx_first_school_year.setObjectName("sbx_first_school_year")
        self.gridlayout.addWidget(self.sbx_first_school_year,6,2,1,1)

        spacerItem = QtGui.QSpacerItem(20,41,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem,0,1,1,1)

        spacerItem1 = QtGui.QSpacerItem(20,41,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem1,7,1,1,1)

        self.led_given_name = QtGui.QLineEdit(self.page)
        self.led_given_name.setObjectName("led_given_name")
        self.gridlayout.addWidget(self.led_given_name,2,1,1,2)

        self.label_2 = QtGui.QLabel(self.page)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2,1,1,1,2)

        self.label = QtGui.QLabel(self.page)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,3,1,1,2)

        self.led_family_name = QtGui.QLineEdit(self.page)
        self.led_family_name.setObjectName("led_family_name")
        self.gridlayout.addWidget(self.led_family_name,4,1,1,2)

        self.cmb_usertype = QtGui.QComboBox(self.page)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(3),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmb_usertype.sizePolicy().hasHeightForWidth())
        self.cmb_usertype.setSizePolicy(sizePolicy)
        self.cmb_usertype.setObjectName("cmb_usertype")
        self.gridlayout.addWidget(self.cmb_usertype,6,1,1,1)

        self.label_3 = QtGui.QLabel(self.page)
        self.label_3.setObjectName("label_3")
        self.gridlayout.addWidget(self.label_3,5,1,1,1)

        self.lbl_names_decoration = QtGui.QLabel(self.page)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_names_decoration.sizePolicy().hasHeightForWidth())
        self.lbl_names_decoration.setSizePolicy(sizePolicy)
        self.lbl_names_decoration.setPixmap(QtGui.QPixmap("art/student.svg"))
        self.lbl_names_decoration.setObjectName("lbl_names_decoration")
        self.gridlayout.addWidget(self.lbl_names_decoration,1,0,6,1)
        self.swd_userinfo.addWidget(self.page)

        self.page_2 = QtGui.QWidget()
        self.page_2.setObjectName("page_2")

        self.gridlayout1 = QtGui.QGridLayout(self.page_2)
        self.gridlayout1.setMargin(0)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        self.btn_add_groups = QtGui.QToolButton(self.page_2)
        self.btn_add_groups.setObjectName("btn_add_groups")
        self.gridlayout1.addWidget(self.btn_add_groups,3,2,1,1)

        spacerItem2 = QtGui.QSpacerItem(20,25,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout1.addItem(spacerItem2,5,1,1,2)

        self.label_6 = QtGui.QLabel(self.page_2)
        self.label_6.setObjectName("label_6")
        self.gridlayout1.addWidget(self.label_6,3,1,1,1)

        self.trv_groups = EnhancedTreeView(self.page_2)
        self.trv_groups.setAcceptDrops(True)
        self.trv_groups.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.trv_groups.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.trv_groups.setRootIsDecorated(False)
        self.trv_groups.setItemsExpandable(False)
        self.trv_groups.setObjectName("trv_groups")
        self.gridlayout1.addWidget(self.trv_groups,4,1,1,2)

        self.lbl_groups_decoration = QtGui.QLabel(self.page_2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_groups_decoration.sizePolicy().hasHeightForWidth())
        self.lbl_groups_decoration.setSizePolicy(sizePolicy)
        self.lbl_groups_decoration.setPixmap(QtGui.QPixmap("art/student.svg"))
        self.lbl_groups_decoration.setObjectName("lbl_groups_decoration")
        self.gridlayout1.addWidget(self.lbl_groups_decoration,4,0,1,1)

        self.label_5 = QtGui.QLabel(self.page_2)
        self.label_5.setObjectName("label_5")
        self.gridlayout1.addWidget(self.label_5,1,1,1,2)

        self.cmb_primary_group = QtGui.QComboBox(self.page_2)
        self.cmb_primary_group.setObjectName("cmb_primary_group")
        self.gridlayout1.addWidget(self.cmb_primary_group,2,1,1,2)

        spacerItem3 = QtGui.QSpacerItem(20,25,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout1.addItem(spacerItem3,0,1,1,2)
        self.swd_userinfo.addWidget(self.page_2)

        self.page_3 = QtGui.QWidget()
        self.page_3.setObjectName("page_3")

        self.gridlayout2 = QtGui.QGridLayout(self.page_3)
        self.gridlayout2.setMargin(0)
        self.gridlayout2.setSpacing(6)
        self.gridlayout2.setObjectName("gridlayout2")

        spacerItem4 = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout2.addItem(spacerItem4,0,1,1,1)

        spacerItem5 = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout2.addItem(spacerItem5,7,1,1,1)

        self.led_passwd_confirm = QtGui.QLineEdit(self.page_3)
        self.led_passwd_confirm.setEchoMode(QtGui.QLineEdit.Password)
        self.led_passwd_confirm.setObjectName("led_passwd_confirm")
        self.gridlayout2.addWidget(self.led_passwd_confirm,6,1,1,1)

        self.label_7 = QtGui.QLabel(self.page_3)
        self.label_7.setObjectName("label_7")
        self.gridlayout2.addWidget(self.label_7,5,1,1,1)

        self.led_passwd = QtGui.QLineEdit(self.page_3)
        self.led_passwd.setEchoMode(QtGui.QLineEdit.Password)
        self.led_passwd.setObjectName("led_passwd")
        self.gridlayout2.addWidget(self.led_passwd,4,1,1,1)

        self.label_8 = QtGui.QLabel(self.page_3)
        self.label_8.setObjectName("label_8")
        self.gridlayout2.addWidget(self.label_8,3,1,1,1)

        self.led_login = QtGui.QLineEdit(self.page_3)
        self.led_login.setObjectName("led_login")
        self.gridlayout2.addWidget(self.led_login,2,1,1,1)

        self.label_9 = QtGui.QLabel(self.page_3)
        self.label_9.setObjectName("label_9")
        self.gridlayout2.addWidget(self.label_9,1,1,1,1)

        self.lbl_login_decoration = QtGui.QLabel(self.page_3)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_login_decoration.sizePolicy().hasHeightForWidth())
        self.lbl_login_decoration.setSizePolicy(sizePolicy)
        self.lbl_login_decoration.setPixmap(QtGui.QPixmap("art/student.svg"))
        self.lbl_login_decoration.setObjectName("lbl_login_decoration")
        self.gridlayout2.addWidget(self.lbl_login_decoration,2,0,5,1)
        self.swd_userinfo.addWidget(self.page_3)
        self.vboxlayout.addWidget(self.swd_userinfo)

        self.line = QtGui.QFrame(CreateUserWizard)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.vboxlayout.addWidget(self.line)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.btn_cancel = QtGui.QPushButton(CreateUserWizard)
        self.btn_cancel.setObjectName("btn_cancel")
        self.hboxlayout.addWidget(self.btn_cancel)

        spacerItem6 = QtGui.QSpacerItem(35,20,QtGui.QSizePolicy.MinimumExpanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem6)

        self.btn_back = QtGui.QPushButton(CreateUserWizard)
        self.btn_back.setEnabled(False)
        self.btn_back.setObjectName("btn_back")
        self.hboxlayout.addWidget(self.btn_back)

        self.btn_next = QtGui.QPushButton(CreateUserWizard)
        self.btn_next.setEnabled(False)
        self.btn_next.setObjectName("btn_next")
        self.hboxlayout.addWidget(self.btn_next)

        spacerItem7 = QtGui.QSpacerItem(16,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem7)

        self.btn_finish = QtGui.QPushButton(CreateUserWizard)
        self.btn_finish.setEnabled(False)
        self.btn_finish.setObjectName("btn_finish")
        self.hboxlayout.addWidget(self.btn_finish)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.retranslateUi(CreateUserWizard)
        self.swd_userinfo.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(CreateUserWizard)
        CreateUserWizard.setTabOrder(self.led_given_name,self.led_family_name)
        CreateUserWizard.setTabOrder(self.led_family_name,self.cmb_usertype)
        CreateUserWizard.setTabOrder(self.cmb_usertype,self.sbx_first_school_year)
        CreateUserWizard.setTabOrder(self.sbx_first_school_year,self.cmb_primary_group)
        CreateUserWizard.setTabOrder(self.cmb_primary_group,self.btn_add_groups)
        CreateUserWizard.setTabOrder(self.btn_add_groups,self.trv_groups)
        CreateUserWizard.setTabOrder(self.trv_groups,self.led_login)
        CreateUserWizard.setTabOrder(self.led_login,self.led_passwd)
        CreateUserWizard.setTabOrder(self.led_passwd,self.led_passwd_confirm)
        CreateUserWizard.setTabOrder(self.led_passwd_confirm,self.btn_finish)
        CreateUserWizard.setTabOrder(self.btn_finish,self.btn_back)
        CreateUserWizard.setTabOrder(self.btn_back,self.btn_next)
        CreateUserWizard.setTabOrder(self.btn_next,self.btn_cancel)

    def retranslateUi(self, CreateUserWizard):
        CreateUserWizard.setWindowTitle(QtGui.QApplication.translate("CreateUserWizard", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("CreateUserWizard", "First school year:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("CreateUserWizard", "Given name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("CreateUserWizard", "Family name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("CreateUserWizard", "User type:", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_add_groups.setText(QtGui.QApplication.translate("CreateUserWizard", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("CreateUserWizard", "Secondary groups:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("CreateUserWizard", "Primary groups:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("CreateUserWizard", "Confirm password:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("CreateUserWizard", "User password:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("CreateUserWizard", "User\'s login name:", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_cancel.setText(QtGui.QApplication.translate("CreateUserWizard", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_back.setText(QtGui.QApplication.translate("CreateUserWizard", "< Back", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_next.setText(QtGui.QApplication.translate("CreateUserWizard", "Next >", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_finish.setText(QtGui.QApplication.translate("CreateUserWizard", "Finish", None, QtGui.QApplication.UnicodeUTF8))
