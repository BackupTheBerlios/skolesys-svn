# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_creategroupwizard.ui'
#
# Created: Thu Jul 19 19:06:31 2007
#      by: PyQt4 UI code generator 4.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_CreateGroupWizard(object):
    def setupUi(self, CreateGroupWizard):
        CreateGroupWizard.setObjectName("CreateGroupWizard")
        CreateGroupWizard.resize(QtCore.QSize(QtCore.QRect(0,0,435,350).size()).expandedTo(CreateGroupWizard.minimumSizeHint()))

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(5),QtGui.QSizePolicy.Policy(5))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CreateGroupWizard.sizePolicy().hasHeightForWidth())
        CreateGroupWizard.setSizePolicy(sizePolicy)
        CreateGroupWizard.setMinimumSize(QtCore.QSize(0,350))
        CreateGroupWizard.setMaximumSize(QtCore.QSize(16777215,350))

        self.vboxlayout = QtGui.QVBoxLayout(CreateGroupWizard)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.swd_userinfo = QtGui.QStackedWidget(CreateGroupWizard)
        self.swd_userinfo.setObjectName("swd_userinfo")

        self.page = QtGui.QWidget()
        self.page.setObjectName("page")

        self.gridlayout = QtGui.QGridLayout(self.page)
        self.gridlayout.setMargin(0)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        spacerItem = QtGui.QSpacerItem(20,71,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem,5,1,1,1)

        spacerItem1 = QtGui.QSpacerItem(20,71,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem1,0,1,1,1)

        self.label_2 = QtGui.QLabel(self.page)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2,1,1,1,1)

        self.led_groupname = QtGui.QLineEdit(self.page)
        self.led_groupname.setObjectName("led_groupname")
        self.gridlayout.addWidget(self.led_groupname,2,1,1,1)

        self.label = QtGui.QLabel(self.page)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,3,1,1,1)

        self.lbl_names_decoration = QtGui.QLabel(self.page)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_names_decoration.sizePolicy().hasHeightForWidth())
        self.lbl_names_decoration.setSizePolicy(sizePolicy)
        self.lbl_names_decoration.setPixmap(QtGui.QPixmap("art/student.svg"))
        self.lbl_names_decoration.setObjectName("lbl_names_decoration")
        self.gridlayout.addWidget(self.lbl_names_decoration,2,0,4,1)

        self.cmb_grouptype = QtGui.QComboBox(self.page)
        self.cmb_grouptype.setObjectName("cmb_grouptype")
        self.gridlayout.addWidget(self.cmb_grouptype,4,1,1,1)
        self.swd_userinfo.addWidget(self.page)

        self.page_2 = QtGui.QWidget()
        self.page_2.setObjectName("page_2")

        self.gridlayout1 = QtGui.QGridLayout(self.page_2)
        self.gridlayout1.setMargin(0)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        spacerItem2 = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout1.addItem(spacerItem2,3,1,1,1)

        spacerItem3 = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout1.addItem(spacerItem3,0,1,1,1)

        self.ted_description = QtGui.QTextEdit(self.page_2)
        self.ted_description.setObjectName("ted_description")
        self.gridlayout1.addWidget(self.ted_description,2,1,1,1)

        self.label_3 = QtGui.QLabel(self.page_2)
        self.label_3.setObjectName("label_3")
        self.gridlayout1.addWidget(self.label_3,1,1,1,1)

        self.lbl_groups_decoration = QtGui.QLabel(self.page_2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_groups_decoration.sizePolicy().hasHeightForWidth())
        self.lbl_groups_decoration.setSizePolicy(sizePolicy)
        self.lbl_groups_decoration.setPixmap(QtGui.QPixmap("art/student.svg"))
        self.lbl_groups_decoration.setObjectName("lbl_groups_decoration")
        self.gridlayout1.addWidget(self.lbl_groups_decoration,2,0,1,1)
        self.swd_userinfo.addWidget(self.page_2)
        self.vboxlayout.addWidget(self.swd_userinfo)

        self.line = QtGui.QFrame(CreateGroupWizard)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.vboxlayout.addWidget(self.line)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.btn_cancel = QtGui.QPushButton(CreateGroupWizard)
        self.btn_cancel.setObjectName("btn_cancel")
        self.hboxlayout.addWidget(self.btn_cancel)

        spacerItem4 = QtGui.QSpacerItem(35,20,QtGui.QSizePolicy.MinimumExpanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem4)

        self.btn_back = QtGui.QPushButton(CreateGroupWizard)
        self.btn_back.setEnabled(False)
        self.btn_back.setObjectName("btn_back")
        self.hboxlayout.addWidget(self.btn_back)

        self.btn_next = QtGui.QPushButton(CreateGroupWizard)
        self.btn_next.setEnabled(False)
        self.btn_next.setObjectName("btn_next")
        self.hboxlayout.addWidget(self.btn_next)

        spacerItem5 = QtGui.QSpacerItem(16,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem5)

        self.btn_finish = QtGui.QPushButton(CreateGroupWizard)
        self.btn_finish.setEnabled(False)
        self.btn_finish.setObjectName("btn_finish")
        self.hboxlayout.addWidget(self.btn_finish)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.retranslateUi(CreateGroupWizard)
        self.swd_userinfo.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(CreateGroupWizard)
        CreateGroupWizard.setTabOrder(self.led_groupname,self.btn_finish)
        CreateGroupWizard.setTabOrder(self.btn_finish,self.btn_back)
        CreateGroupWizard.setTabOrder(self.btn_back,self.btn_next)
        CreateGroupWizard.setTabOrder(self.btn_next,self.btn_cancel)

    def retranslateUi(self, CreateGroupWizard):
        CreateGroupWizard.setWindowTitle(QtGui.QApplication.translate("CreateGroupWizard", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("CreateGroupWizard", "Group name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("CreateGroupWizard", "Group type:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("CreateGroupWizard", "Description:", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_cancel.setText(QtGui.QApplication.translate("CreateGroupWizard", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_back.setText(QtGui.QApplication.translate("CreateGroupWizard", "< Back", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_next.setText(QtGui.QApplication.translate("CreateGroupWizard", "Next >", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_finish.setText(QtGui.QApplication.translate("CreateGroupWizard", "Finish", None, QtGui.QApplication.UnicodeUTF8))

