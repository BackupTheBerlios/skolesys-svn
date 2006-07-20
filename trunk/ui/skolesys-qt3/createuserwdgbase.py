# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/admin/l4s_admin/createuserwdgbase.ui'
#
# Created: tor jul 20 02:49:58 2006
#      by: The PyQt User Interface Compiler (pyuic) 3.15.1
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class CreateUserWdgBase(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        if not name:
            self.setName("CreateUserWdgBase")


        CreateUserWdgBaseLayout = QGridLayout(self,1,1,0,6,"CreateUserWdgBaseLayout")

        self.ed_lastname = QLineEdit(self,"ed_lastname")

        CreateUserWdgBaseLayout.addWidget(self.ed_lastname,1,1)

        self.ed_firstname = QLineEdit(self,"ed_firstname")

        CreateUserWdgBaseLayout.addWidget(self.ed_firstname,0,1)

        self.textLabel1 = QLabel(self,"textLabel1")

        CreateUserWdgBaseLayout.addWidget(self.textLabel1,0,0)

        self.textLabel3 = QLabel(self,"textLabel3")

        CreateUserWdgBaseLayout.addWidget(self.textLabel3,2,0)

        self.textLabel1_2 = QLabel(self,"textLabel1_2")

        CreateUserWdgBaseLayout.addWidget(self.textLabel1_2,1,0)

        self.ed_login = QLineEdit(self,"ed_login")

        CreateUserWdgBaseLayout.addWidget(self.ed_login,2,1)

        self.m_cmb_usertype = QComboBox(0,self,"m_cmb_usertype")

        CreateUserWdgBaseLayout.addWidget(self.m_cmb_usertype,3,1)

        self.textLabel2 = QLabel(self,"textLabel2")

        CreateUserWdgBaseLayout.addWidget(self.textLabel2,3,0)
        spacer1 = QSpacerItem(20,31,QSizePolicy.Minimum,QSizePolicy.Expanding)
        CreateUserWdgBaseLayout.addItem(spacer1,4,1)

        self.languageChange()

        self.resize(QSize(329,141).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(self.__tr("Form1"))
        self.textLabel1.setText(self.__tr("First name"))
        self.textLabel3.setText(self.__tr("Login"))
        self.textLabel1_2.setText(self.__tr("Last name"))
        self.textLabel2.setText(self.__tr("User type"))


    def __tr(self,s,c = None):
        return qApp.translate("CreateUserWdgBase",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = CreateUserWdgBase()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
