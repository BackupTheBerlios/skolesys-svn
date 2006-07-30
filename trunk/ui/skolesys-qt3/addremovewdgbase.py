# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/refsvindinge.dk/jakob@refsvindinge.dk/Projects/l4s_admin/addremovewdgbase.ui'
#
# Created: lør jul 29 10:16:20 2006
#      by: The PyQt User Interface Compiler (pyuic) 3.15.1
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *
import inspect
import os.path


class AddRemoveWdgBase(QWidget):
	def __init__(self,parent = None,name = None,fl = 0):
		QWidget.__init__(self,parent,name,fl)

		basepath = os.path.split(__file__)[0]
		if not name:
			self.setName("AddRemoveWdgBase")

		self.mainlayout = QGridLayout(self,1,1,11,6,"self.mainlayout")

		self.lb_subjects = QListBox(self,"lb_subjects")
		self.lb_subjects.setSelectionMode(QListBox.NoSelection)
		self.lb_subjects.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.MinimumExpanding)
		self.mainlayout.addMultiCellWidget(self.lb_subjects,0,0,0,2)
		
		self.lb_add = QListBox(self,"lb_add")
		self.lb_add.setSelectionMode(QListBox.Extended)
		self.mainlayout.addMultiCellWidget(self.lb_add,2,4,2,2)

		self.lb_remove = QListBox(self,"lb_remove")
		self.lb_remove.setSelectionMode(QListBox.Extended)
		self.mainlayout.addMultiCellWidget(self.lb_remove,6,8,2,2)

		self.add_label = QLabel(self,"add_label")
		self.mainlayout.addWidget(self.add_label,1,2)

		self.remove_label = QLabel(self,"remove_label")
		self.mainlayout.addWidget(self.remove_label,5,2)

		# Add buttons
		self.btn_add_add = QToolButton(self,"btn_add_add")
		self.mainlayout.addWidget(self.btn_add_add,2,1)
		self.btn_remove_add = QToolButton(self,"btn_remove_add")
		self.mainlayout.addWidget(self.btn_remove_add,3,1)

		# Remove buttons
		self.btn_add_remove = QToolButton(self,"btn_add_remove")
		self.mainlayout.addWidget(self.btn_add_remove,6,1)
		self.btn_remove_remove = QToolButton(self,"btn_remove_remove")
		self.mainlayout.addWidget(self.btn_remove_remove,7,1)

		self.connect(self.btn_remove_add,SIGNAL("clicked()"),self.removeFromAddClicked)
		self.connect(self.btn_remove_remove,SIGNAL("clicked()"),self.removeFromRemoveClicked)

		spacer1 = QSpacerItem(20,51,QSizePolicy.Minimum,QSizePolicy.Expanding)
		self.mainlayout.addItem(spacer1,4,1)
		spacer2 = QSpacerItem(20,51,QSizePolicy.Minimum,QSizePolicy.Expanding)
		self.mainlayout.addItem(spacer2,8,1)

		self.languageChange()

		pix = QPixmap()
		pix.load("%s/green_left.png" % basepath,"PNG")
		self.btn_remove_remove.setIconSet(QIconSet(pix))
		self.btn_remove_add.setIconSet(QIconSet(pix))
		pix.load("%s/green_right.png" % basepath,"PNG")
		self.btn_add_add.setIconSet(QIconSet(pix))
		self.btn_add_remove.setIconSet(QIconSet(pix))


		self.resize(QSize(216,286).expandedTo(self.minimumSizeHint()))
		self.clearWState(Qt.WState_Polished)


	def languageChange(self):
		pass
	
	def __tr(self,s,c = None):
		return qApp.translate("AddRemoveWdgBase",s,c)

	def removeFromListbox(self,lb_rmbox):
		rm_items = []
		# Find the selected item indexes
		for idx in xrange(lb_rmbox.count()):
			if lb_rmbox.isSelected(idx):
				rm_items += [idx]
		
		# Remove the items
		rm_items.reverse()
		for idx in rm_items:
			lb_rmbox.removeItem(idx)

	def removeFromAddClicked(self):
		self.removeFromListbox(self.lb_add)

	def removeFromRemoveClicked(self):
		self.removeFromListbox(self.lb_remove)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = AddRemoveWdgBase()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
