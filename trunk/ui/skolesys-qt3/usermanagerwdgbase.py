# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/refsvindinge.dk/jakob@refsvindinge.dk/Projects/l4s_admin/usermanagerwdgbase.ui'
#
# Created: lør jul 29 00:46:42 2006
#      by: The PyQt User Interface Compiler (pyuic) 3.15.1
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class UserManagerWdgBase(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        if not name:
            self.setName("UserManagerWdgBase")


        UserManagerWdgBaseLayout = QGridLayout(self,1,1,0,6,"UserManagerWdgBaseLayout")

        self.m_cb_usertype_filter = QComboBox(0,self,"m_cb_usertype_filter")

        UserManagerWdgBaseLayout.addWidget(self.m_cb_usertype_filter,0,1)

        self.m_lv_userlist = QListView(self,"m_lv_userlist")
        self.m_lv_userlist.setSelectionMode(QListView.Extended)
        self.m_lv_userlist.setAllColumnsShowFocus(1)
        self.m_lv_userlist.setShowSortIndicator(1)

        UserManagerWdgBaseLayout.addMultiCellWidget(self.m_lv_userlist,1,1,0,2)
        spacer1 = QSpacerItem(123,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        UserManagerWdgBaseLayout.addItem(spacer1,0,2)

        self.textLabel1 = QLabel(self,"textLabel1")

        UserManagerWdgBaseLayout.addWidget(self.textLabel1,0,0)

        self.languageChange()

        self.resize(QSize(386,202).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.m_cb_usertype_filter,SIGNAL("activated(int)"),self.slotFilterActivated)

        self.setTabOrder(self.m_cb_usertype_filter,self.m_lv_userlist)


    def languageChange(self):
        self.setCaption(self.__tr("Form2"))
        self.textLabel1.setText(self.__tr("User type filter"))


    def slotFilterActivated(self,a0):
        print "UserManagerWdgBase.slotFilterActivated(int): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("UserManagerWdgBase",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = UserManagerWdgBase()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
