# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_tooltabwdg.ui'
#
# Created: Sun Jul  8 02:19:55 2007
#      by: PyQt4 UI code generator 4.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_ToolTabWdg(object):
    def setupUi(self, ToolTabWdg):
        ToolTabWdg.setObjectName("ToolTabWdg")
        ToolTabWdg.resize(QtCore.QSize(QtCore.QRect(0,0,658,638).size()).expandedTo(ToolTabWdg.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(ToolTabWdg)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        spacerItem = QtGui.QSpacerItem(550,51,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem,0,0,1,1)

        spacerItem1 = QtGui.QSpacerItem(550,71,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem1,5,0,1,1)

        self.frame_3 = QtGui.QFrame(ToolTabWdg)
        self.frame_3.setMaximumSize(QtCore.QSize(550,16777215))
        self.frame_3.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")

        self.gridlayout1 = QtGui.QGridLayout(self.frame_3)
        self.gridlayout1.setMargin(9)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        self.label_7 = QtGui.QLabel(self.frame_3)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(5),QtGui.QSizePolicy.Policy(1))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setFrameShape(QtGui.QFrame.NoFrame)
        self.label_7.setWordWrap(True)
        self.label_7.setObjectName("label_7")
        self.gridlayout1.addWidget(self.label_7,0,1,1,1)

        self.btn_open_fileman = QtGui.QToolButton(self.frame_3)
        self.btn_open_fileman.setMinimumSize(QtCore.QSize(80,80))
        self.btn_open_fileman.setFocusPolicy(QtCore.Qt.NoFocus)
        self.btn_open_fileman.setIconSize(QtCore.QSize(72,72))
        self.btn_open_fileman.setObjectName("btn_open_fileman")
        self.gridlayout1.addWidget(self.btn_open_fileman,0,0,1,1)
        self.gridlayout.addWidget(self.frame_3,4,0,1,1)

        self.frame = QtGui.QFrame(ToolTabWdg)
        self.frame.setMaximumSize(QtCore.QSize(550,16777215))
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.gridlayout2 = QtGui.QGridLayout(self.frame)
        self.gridlayout2.setMargin(9)
        self.gridlayout2.setSpacing(6)
        self.gridlayout2.setObjectName("gridlayout2")

        self.btn_new_user = QtGui.QToolButton(self.frame)
        self.btn_new_user.setMinimumSize(QtCore.QSize(80,80))
        self.btn_new_user.setFocusPolicy(QtCore.Qt.NoFocus)
        self.btn_new_user.setIconSize(QtCore.QSize(72,72))
        self.btn_new_user.setObjectName("btn_new_user")
        self.gridlayout2.addWidget(self.btn_new_user,0,0,1,1)

        self.label = QtGui.QLabel(self.frame)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.gridlayout2.addWidget(self.label,0,1,1,1)
        self.gridlayout.addWidget(self.frame,3,0,1,1)

        self.frame_2 = QtGui.QFrame(ToolTabWdg)
        self.frame_2.setMaximumSize(QtCore.QSize(550,16777215))
        self.frame_2.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")

        self.gridlayout3 = QtGui.QGridLayout(self.frame_2)
        self.gridlayout3.setMargin(9)
        self.gridlayout3.setSpacing(6)
        self.gridlayout3.setObjectName("gridlayout3")

        self.label_4 = QtGui.QLabel(self.frame_2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(5),QtGui.QSizePolicy.Policy(1))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setFrameShape(QtGui.QFrame.NoFrame)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.gridlayout3.addWidget(self.label_4,0,1,1,1)

        self.btn_new_group = QtGui.QToolButton(self.frame_2)
        self.btn_new_group.setMinimumSize(QtCore.QSize(80,80))
        self.btn_new_group.setFocusPolicy(QtCore.Qt.NoFocus)
        self.btn_new_group.setIconSize(QtCore.QSize(72,72))
        self.btn_new_group.setObjectName("btn_new_group")
        self.gridlayout3.addWidget(self.btn_new_group,0,0,1,1)
        self.gridlayout.addWidget(self.frame_2,2,0,1,1)

        self.retranslateUi(ToolTabWdg)
        QtCore.QMetaObject.connectSlotsByName(ToolTabWdg)

    def retranslateUi(self, ToolTabWdg):
        ToolTabWdg.setWindowTitle(QtGui.QApplication.translate("ToolTabWdg", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("ToolTabWdg", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">Filestatistics</span></p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Search through all files created and downloaded by SkoleSYS users. Search for all movie files, audio files etc. based on all users or just a certain user. Use the minimum file size threshold to ignore smaller files.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_open_fileman.setText(QtGui.QApplication.translate("ToolTabWdg", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_new_user.setText(QtGui.QApplication.translate("ToolTabWdg", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ToolTabWdg", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:15pt;\">New User</span></p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">This wizard will take you through the steps of creating a new user. All user resources will be created and the user can login immediately after finalization.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("ToolTabWdg", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">New Group</span></p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Create a new group by following the steps of this wizard. Group resources will be allocated and users can be added as members.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_new_group.setText(QtGui.QApplication.translate("ToolTabWdg", "...", None, QtGui.QApplication.UnicodeUTF8))

