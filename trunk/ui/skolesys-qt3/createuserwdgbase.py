# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/refsvindinge.dk/jakob@refsvindinge.dk/Projects/l4s_admin/createuserwdgbase.ui'
#
# Created: fre jul 21 03:03:01 2006
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

        self.textLabel1 = QLabel(self,"textLabel1")

        CreateUserWdgBaseLayout.addWidget(self.textLabel1,1,0)

        self.ed_firstname = QLineEdit(self,"ed_firstname")

        CreateUserWdgBaseLayout.addMultiCellWidget(self.ed_firstname,1,1,1,2)

        self.textLabel2 = QLabel(self,"textLabel2")

        CreateUserWdgBaseLayout.addWidget(self.textLabel2,0,0)

        self.cmb_usertype = QComboBox(0,self,"cmb_usertype")

        CreateUserWdgBaseLayout.addMultiCellWidget(self.cmb_usertype,0,0,1,2)

        self.ed_lastname = QLineEdit(self,"ed_lastname")

        CreateUserWdgBaseLayout.addMultiCellWidget(self.ed_lastname,2,2,1,2)
        spacer1 = QSpacerItem(20,16,QSizePolicy.Minimum,QSizePolicy.Expanding)
        CreateUserWdgBaseLayout.addItem(spacer1,6,1)

        self.lbl_domain_name = QLabel(self,"lbl_domain_name")

        CreateUserWdgBaseLayout.addWidget(self.lbl_domain_name,4,2)

        self.textLabel1_2 = QLabel(self,"textLabel1_2")

        CreateUserWdgBaseLayout.addWidget(self.textLabel1_2,2,0)

        self.line1 = QFrame(self,"line1")
        self.line1.setFrameShape(QFrame.HLine)
        self.line1.setFrameShadow(QFrame.Sunken)
        self.line1.setFrameShape(QFrame.HLine)

        CreateUserWdgBaseLayout.addMultiCellWidget(self.line1,3,3,0,2)

        self.ed_passwd = QLineEdit(self,"ed_passwd")
        self.ed_passwd.setEchoMode(QLineEdit.Password)

        CreateUserWdgBaseLayout.addMultiCellWidget(self.ed_passwd,5,5,1,2)

        self.textLabel3 = QLabel(self,"textLabel3")

        CreateUserWdgBaseLayout.addWidget(self.textLabel3,4,0)

        self.ed_login = QLineEdit(self,"ed_login")

        CreateUserWdgBaseLayout.addWidget(self.ed_login,4,1)

        self.textLabel1_3 = QLabel(self,"textLabel1_3")

        CreateUserWdgBaseLayout.addWidget(self.textLabel1_3,5,0)

        self.languageChange()

        self.resize(QSize(373,172).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.setTabOrder(self.cmb_usertype,self.ed_firstname)
        self.setTabOrder(self.ed_firstname,self.ed_lastname)
        self.setTabOrder(self.ed_lastname,self.ed_login)
        self.setTabOrder(self.ed_login,self.ed_passwd)


    def languageChange(self):
        self.setCaption(self.__tr("Form1"))
        self.textLabel1.setText(self.__tr("First name"))
        self.textLabel2.setText(self.__tr("User type"))
        self.lbl_domain_name.setText(QString.null)
        self.textLabel1_2.setText(self.__tr("Last name"))
        self.textLabel3.setText(self.__tr("Login"))
        self.textLabel1_3.setText(self.__tr("Password"))


    def __tr(self,s,c = None):
        return qApp.translate("CreateUserWdgBase",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = CreateUserWdgBase()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
