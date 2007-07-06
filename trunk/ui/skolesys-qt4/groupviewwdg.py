'''
This file is part of the SkoleSYS libraries
Copyright (C) 2007 Jakob Simon-Gaarde <info at skolesys.dk>

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Library General Public
License version 2 as published by the Free Software Foundation.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Library General Public License for more details.

You should have received a copy of the GNU Library General Public License
along with this library; see the file COPYING.LIB.  If not, write to
the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
Boston, MA 02110-1301, USA.
'''

from PyQt4 import QtCore, QtGui
import ui_groupviewwdg as ui_gvwdg
import groupmodel as gmod
import skolesys.definitions.groupdef as groupdef
import connectionmanager as cm
import pyqtui4.pluggablemodelhelper as pmh
import pickle
import ss_mainwindow as mainwin


class GroupViewWdg(QtGui.QWidget, ui_gvwdg.Ui_GroupViewWdg):
	
	def __init__(self,parent):
		QtGui.QWidget.__init__(self,parent)
		
		self.proxy = cm.get_proxy_handle()
		self.setupUi(self)
		self.setupModel()
		self.setupGroupTypeCombo()
		self.setupGroupView()
		self.updateGroupView()
		
		self.trv_grouplist.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.connect(self.trv_grouplist,QtCore.SIGNAL("customContextMenuRequested(const QPoint&)"),self.grouplistContextMenu)
		self.connect(self.trv_grouplist,QtCore.SIGNAL("itemDoubleClicked(QTreeWidgetItem *,int)"),self.doubleClickEdit)
		
		# Recieve notice on altered, deleted or changed groups
		self.connect(mainwin.get_mainwindow(),QtCore.SIGNAL("groupChanged"),self.updateGroupView)
		self.connect(mainwin.get_mainwindow(),QtCore.SIGNAL("groupDeleted"),self.updateGroupView)
		self.connect(mainwin.get_mainwindow(),QtCore.SIGNAL("groupCreated"),self.updateGroupView)
	
	def grouplistContextMenu(self,pos):
		menu = QtGui.QMenu(self)
		editaction = menu.addAction(self.tr('Edit selected groups...'))
		self.connect(editaction,QtCore.SIGNAL('triggered()'),self.editGroups)
		editaction = menu.addAction(self.tr('Edit memberships...'))
		self.connect(editaction,QtCore.SIGNAL('triggered()'),self.editMemberships)
		menu.exec_(QtGui.QCursor.pos())

	
	def setupModel(self):
		self.groupmodel = gmod.GroupModel(self.trv_grouplist)
		self.modelhelper = pmh.PluggableModelHelper(self.groupmodel)
		self.modelhelper.setView(self.trv_grouplist)
		for colidx in xrange(self.groupmodel.columnCount()):
			self.modelhelper.setColumnReadOnly(colidx)
		
	def doubleClickEdit(self,item):
		import ss_mainwindow as ss_mainwin
		idx = self.trv_grouplist.currentIndex()
		mimedata = self.groupmodel.generateMimeData([idx])
		for g in pickle.loads(mimedata['application/x-skolesysgroups-pyobj']):
			ss_mainwin.get_mainwindow().editGroup(g['groupname'],g['displayed_name'])

	def editGroups(self):
		import ss_mainwindow as ss_mainwin
		mimedata = self.groupmodel.generateMimeData(self.trv_grouplist.selectedIndexes())
		for g in pickle.loads(mimedata['application/x-skolesysgroups-pyobj']):
			ss_mainwin.get_mainwindow().editGroup(g['groupname'],g['displayed_name'])

	def editMemberships(self):
		mimedata = self.groupmodel.generateMimeData(self.trv_grouplist.selectedIndexes())
		groups = pickle.loads(mimedata['application/x-skolesysgroups-pyobj'])
		if not len(groups):
			# No users selected
			return
		
		import addremovegroupuserswdg as memberships
		m = memberships.AddRemoveGroupUsersWdg(groups,self)
		m.exec_()

	def setupGroupView(self):
		self.trv_grouplist.setColumnHidden(self.groupmodel.columninfo['gid']['columnindex'],True)
		self.trv_grouplist.setColumnHidden(self.groupmodel.columninfo['groupname']['columnindex'],True)
	
	def setupGroupTypeCombo(self):
		self.tr("primary","plural")
		self.tr("system","plural")
		self.tr("service","plural")
		grouptypeids = groupdef.list_grouptypes_by_id()
		self.cmb_grouptype_filter.addItem(self.tr("All","plural"),QtCore.QVariant(-1))
		for i in grouptypeids:
			self.cmb_grouptype_filter.addItem(
				self.tr(groupdef.grouptype_as_text(i),"plural"),
				QtCore.QVariant(i))
		self.connect(self.cmb_grouptype_filter,QtCore.SIGNAL('activated(int)'),self.updateGroupView)
	
	def updateGroupView(self):
		idx = self.cmb_grouptype_filter.currentIndex()
		if idx > -1:
			grouptype_id,ok = self.cmb_grouptype_filter.itemData(idx).toInt()
			if grouptype_id==-1:
				grouptype_id = None
	
			self.groupmodel.loadGroups(grouptype_id=grouptype_id)
		for colidx in xrange(self.groupmodel.columnCount()):
			self.trv_grouplist.resizeColumnToContents(colidx)
			
	def hideEvent(self,he):
		self.emit(QtCore.SIGNAL("viewShown"),False)
		self.emit(QtCore.SIGNAL("viewHidden"),True)
		QtGui.QWidget.hideEvent(self,he)

	def showEvent(self,se):
		self.emit(QtCore.SIGNAL("viewShown"),True)
		self.emit(QtCore.SIGNAL("viewHidden"),False)
		QtGui.QWidget.showEvent(self,se)


if __name__ == '__main__':
	import sys
	app = QtGui.QApplication(sys.argv)
	trans = QtCore.QTranslator()
	trans.load('skolesys-qt4_da.qm')
	app.installTranslator(trans)
	cm.setup_connection('https://mainserver.skolesys.local',8443)
	ui = GroupViewWdg(None)
	
	ui.show()
	sys.exit(app.exec_())
