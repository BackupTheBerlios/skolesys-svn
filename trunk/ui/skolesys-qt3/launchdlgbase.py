# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/refsvindinge.dk/jakob@refsvindinge.dk/Projects/l4s_admin/launchdlgbase.ui'
#
# Created: lør jul 29 00:46:43 2006
#      by: The PyQt User Interface Compiler (pyuic) 3.15.1
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class LaunchDlgBase(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("LaunchDlgBase")


        LaunchDlgBaseLayout = QVBoxLayout(self,6,6,"LaunchDlgBaseLayout")

        self.pushButton1 = QPushButton(self,"pushButton1")
        LaunchDlgBaseLayout.addWidget(self.pushButton1)

        self.pushButton2 = QPushButton(self,"pushButton2")
        LaunchDlgBaseLayout.addWidget(self.pushButton2)
        spacer1 = QSpacerItem(21,60,QSizePolicy.Minimum,QSizePolicy.Expanding)
        LaunchDlgBaseLayout.addItem(spacer1)

        self.languageChange()

        self.resize(QSize(141,154).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.pushButton1,SIGNAL("clicked()"),self.userManager)
        self.connect(self.pushButton2,SIGNAL("clicked()"),self.groupManager)


    def languageChange(self):
        self.setCaption(self.__tr("Form"))
        self.pushButton1.setText(self.__tr("User Manager"))
        self.pushButton2.setText(self.__tr("Group Manager"))


    def userManager(self):
        print "LaunchDlgBase.userManager(): Not implemented yet"

    def groupManager(self):
        print "LaunchDlgBase.groupManager(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("LaunchDlgBase",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = LaunchDlgBase()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()