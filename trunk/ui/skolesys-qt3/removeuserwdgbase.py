# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/refsvindinge.dk/jakob@refsvindinge.dk/Projects/l4s_admin/removeuserwdgbase.ui'
#
# Created: lør jul 29 00:46:44 2006
#      by: The PyQt User Interface Compiler (pyuic) 3.15.1
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class RemoveUserWdgBase(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        if not name:
            self.setName("RemoveUserWdgBase")


        RemoveUserWdgBaseLayout = QVBoxLayout(self,0,6,"RemoveUserWdgBaseLayout")

        self.lb_users = QListBox(self,"lb_users")
        RemoveUserWdgBaseLayout.addWidget(self.lb_users)

        self.chb_backup_home = QCheckBox(self,"chb_backup_home")
        self.chb_backup_home.setChecked(1)
        RemoveUserWdgBaseLayout.addWidget(self.chb_backup_home)

        self.chb_remove_home = QCheckBox(self,"chb_remove_home")
        self.chb_remove_home.setChecked(1)
        RemoveUserWdgBaseLayout.addWidget(self.chb_remove_home)

        self.languageChange()

        self.resize(QSize(331,185).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.setTabOrder(self.chb_backup_home,self.chb_remove_home)


    def languageChange(self):
        self.setCaption(self.__tr("Form"))
        self.chb_backup_home.setText(self.__tr("Backup the user home directories"))
        self.chb_remove_home.setText(self.__tr("Remove the user home directories"))


    def __tr(self,s,c = None):
        return qApp.translate("RemoveUserWdgBase",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = RemoveUserWdgBase()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
