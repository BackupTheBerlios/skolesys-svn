# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_filemanagerwdg.ui'
#
# Created: Sun Aug 26 00:46:22 2007
#      by: PyQt4 UI code generator 4.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_FileManagerWdg(object):
    def setupUi(self, FileManagerWdg):
        FileManagerWdg.setObjectName("FileManagerWdg")
        FileManagerWdg.resize(QtCore.QSize(QtCore.QRect(0,0,626,524).size()).expandedTo(FileManagerWdg.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(FileManagerWdg)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.groupBox = QtGui.QGroupBox(FileManagerWdg)
        self.groupBox.setObjectName("groupBox")

        self.gridlayout1 = QtGui.QGridLayout(self.groupBox)
        self.gridlayout1.setMargin(9)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        spacerItem = QtGui.QSpacerItem(221,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem,2,1,1,1)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.label_4 = QtGui.QLabel(self.groupBox)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(5),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.hboxlayout.addWidget(self.label_4)

        self.sbx_kb_minsize = QtGui.QSpinBox(self.groupBox)
        self.sbx_kb_minsize.setMaximum(1023)
        self.sbx_kb_minsize.setObjectName("sbx_kb_minsize")
        self.hboxlayout.addWidget(self.sbx_kb_minsize)

        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.hboxlayout.addWidget(self.label_5)

        self.sbx_mb_minsize = QtGui.QSpinBox(self.groupBox)
        self.sbx_mb_minsize.setMaximum(1023)
        self.sbx_mb_minsize.setObjectName("sbx_mb_minsize")
        self.hboxlayout.addWidget(self.sbx_mb_minsize)

        self.label_6 = QtGui.QLabel(self.groupBox)
        self.label_6.setObjectName("label_6")
        self.hboxlayout.addWidget(self.label_6)

        self.lbl_minsize_threshold = QtGui.QLabel(self.groupBox)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(5),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_minsize_threshold.sizePolicy().hasHeightForWidth())
        self.lbl_minsize_threshold.setSizePolicy(sizePolicy)
        self.lbl_minsize_threshold.setObjectName("lbl_minsize_threshold")
        self.hboxlayout.addWidget(self.lbl_minsize_threshold)
        self.gridlayout1.addLayout(self.hboxlayout,2,0,1,1)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.label = QtGui.QLabel(self.groupBox)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(5))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.hboxlayout1.addWidget(self.label)

        self.cmb_userfilter = QtGui.QComboBox(self.groupBox)
        self.cmb_userfilter.setObjectName("cmb_userfilter")
        self.hboxlayout1.addWidget(self.cmb_userfilter)

        self.label_2 = QtGui.QLabel(self.groupBox)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(5))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.hboxlayout1.addWidget(self.label_2)

        self.cmb_groupfilter = QtGui.QComboBox(self.groupBox)
        self.cmb_groupfilter.setObjectName("cmb_groupfilter")
        self.hboxlayout1.addWidget(self.cmb_groupfilter)

        self.label_3 = QtGui.QLabel(self.groupBox)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(5))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.hboxlayout1.addWidget(self.label_3)

        self.cmb_contenttypefilter = QtGui.QComboBox(self.groupBox)
        self.cmb_contenttypefilter.setObjectName("cmb_contenttypefilter")
        self.hboxlayout1.addWidget(self.cmb_contenttypefilter)
        self.gridlayout1.addLayout(self.hboxlayout1,0,0,1,2)

        self.trv_files = EnhancedTreeView(self.groupBox)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(13),QtGui.QSizePolicy.Policy(7))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.trv_files.sizePolicy().hasHeightForWidth())
        self.trv_files.setSizePolicy(sizePolicy)
        self.trv_files.setAlternatingRowColors(True)
        self.trv_files.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.trv_files.setRootIsDecorated(False)
        self.trv_files.setSortingEnabled(True)
        self.trv_files.setObjectName("trv_files")
        self.gridlayout1.addWidget(self.trv_files,1,0,1,2)
        self.gridlayout.addWidget(self.groupBox,0,0,1,4)

        spacerItem1 = QtGui.QSpacerItem(421,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem1,1,2,1,1)

        self.btn_close = QtGui.QPushButton(FileManagerWdg)
        self.btn_close.setObjectName("btn_close")
        self.gridlayout.addWidget(self.btn_close,1,3,1,1)

        self.btn_backup = QtGui.QPushButton(FileManagerWdg)
        self.btn_backup.setObjectName("btn_backup")
        self.gridlayout.addWidget(self.btn_backup,1,1,1,1)

        self.btn_delete = QtGui.QPushButton(FileManagerWdg)
        self.btn_delete.setObjectName("btn_delete")
        self.gridlayout.addWidget(self.btn_delete,1,0,1,1)

        self.retranslateUi(FileManagerWdg)
        QtCore.QMetaObject.connectSlotsByName(FileManagerWdg)

    def retranslateUi(self, FileManagerWdg):
        FileManagerWdg.setWindowTitle(QtGui.QApplication.translate("FileManagerWdg", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("FileManagerWdg", "File View", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("FileManagerWdg", "Minimum file size threshold:", None, QtGui.QApplication.UnicodeUTF8))
        self.sbx_kb_minsize.setSuffix(QtGui.QApplication.translate("FileManagerWdg", " KB", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("FileManagerWdg", "  +  ", None, QtGui.QApplication.UnicodeUTF8))
        self.sbx_mb_minsize.setSuffix(QtGui.QApplication.translate("FileManagerWdg", " MB", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("FileManagerWdg", "  =  ", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_minsize_threshold.setText(QtGui.QApplication.translate("FileManagerWdg", "0 KB", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("FileManagerWdg", "User:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("FileManagerWdg", "Group:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("FileManagerWdg", "Content type:", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_close.setText(QtGui.QApplication.translate("FileManagerWdg", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_backup.setText(QtGui.QApplication.translate("FileManagerWdg", "Backup...", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_delete.setText(QtGui.QApplication.translate("FileManagerWdg", "Delete", None, QtGui.QApplication.UnicodeUTF8))

from pyqtui4.enhancedtreeview import EnhancedTreeView
