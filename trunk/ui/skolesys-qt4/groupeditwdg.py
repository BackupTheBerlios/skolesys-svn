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
import ui_groupeditwdg as baseui
import connectionmanager as cm

import usermodel as umod
import pickle
import pyqtui4.pluggablemodelhelper as pmh
import ss_mainwindow as mainwin
import skolesys.definitions.groupdef as groupdef

class GroupEditWdg(QtGui.QWidget, baseui.Ui_GroupEditWdg):
	
	def __init__(self,groupname,parent):
		QtGui.QWidget.__init__(self,parent)
		self.change_info = {}
		self.groupname = groupname
		self.setupUi(self)
		self.setupServiceCombo()
		self.connect(self.btn_apply,QtCore.SIGNAL('clicked()'),self.applyChanges)
		self.connect(self.tbl_serviceoptions.itemDelegate(),QtCore.SIGNAL("dataChanged"),self.serviceOptionChanged)
		self.force_close_without_save = False
		self.permissions = cm.get_proxy_handle().list_my_permissions()
		
		# Setup group model
		self.usermodel = umod.UserModel(self.trv_users)
		self.modelhelper = pmh.PluggableModelHelper(self.usermodel)
		self.modelhelper.setView(self.trv_users)
		for colidx in xrange(self.usermodel.columnCount()):
			self.modelhelper.setColumnReadOnly(colidx)
		
		self.loadGroupData()
		self.usermodel.setAcceptedMimeTypes(['application/x-skolesysusers-pyobj'])
		
		self.connect(self.btn_add_service,QtCore.SIGNAL('clicked()'),self.addService)
		self.connect(self.ted_description,QtCore.SIGNAL('textChanged()'),self.descriptionChanged)
		
		# User list connections
		self.trv_users.connectEvent("dropEvent",self.hook_dropOnUserView)
		self.trv_users.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.connect(self.trv_users,QtCore.SIGNAL("customContextMenuRequested(const QPoint&)"),self.usersContextMenu)

		# Connect change signals
		self.connect(mainwin.get_mainwindow(),QtCore.SIGNAL('groupMembershipsChanged'),self.updateUsersView)
		self.connect(mainwin.get_mainwindow(),QtCore.SIGNAL('permissionsChanged'),self.setupPermissions)
		
		self.setupPermissions(self.permissions)
	
	
	def setupPermissions(self,access_idents):
		self.permissions = access_idents
		if access_idents.count('group.modify'):
			self.force_close_without_save = False
			self.setEnabled(True)
		else:
			self.force_close_without_save = True
			self.setEnabled(False)
		
		# Group members
		if access_idents.count('membership.create'):
			self.trv_users.setEnabled(True)
		else:
			self.trv_users.setEnabled(False)
			
		# Project services add
		if access_idents.count('service.group.attach'):
			self.btn_add_service.setEnabled(True)
		else:
			self.btn_add_service.setEnabled(False)	
		# Project service properties
		if access_idents.count('service.group.property.set'):
			self.tbl_serviceoptions.setEnabled(True)
		else:
			self.tbl_serviceoptions.setEnabled(False)	

	def setupServiceCombo(self):
		proxy = cm.get_proxy_handle()
		
		services_in_use = proxy.list_groupservices(self.groupname)
		if services_in_use!=-1:
			for serv in services_in_use:
				self.cmb_services.addItem(serv,QtCore.QVariant(serv))
		self.connect(self.cmb_services,QtCore.SIGNAL('activated(int)'),self.currentServiceChanged)
		self.currentServiceChanged(self.cmb_services.currentIndex())

	
	def loadGroupData(self):
		proxy = cm.get_proxy_handle()
		res = proxy.list_groups(groupname=self.groupname)
		if res.has_key(self.groupname):
			self.change_info = {}
			self.group_info = res[self.groupname]
			if res[self.groupname].has_key('description'):
				self.ted_description.setPlainText(QtCore.QString.fromUtf8(res[self.groupname]['description']))
			self.lbl_groupname.setText(QtCore.QString.fromUtf8(res[self.groupname]['displayedName']))
			if res[self.groupname]['grouptype_id'] == groupdef.grouptype_as_id('primary'):
				self.grp_services.setEnabled(False)
				self.grp_members.setEnabled(False)
			if res[self.groupname]['grouptype_id'] == groupdef.grouptype_as_id('system'):
				self.grp_services.setEnabled(False)

		self.updateUsersView()

	def updateUsersView(self,groupname=None):
		if groupname!=None and groupname!=self.groupname:
			return

		self.usermodel.loadUsers(groupname=self.groupname)
		self.group_info['users_by_name'] = list(self.usermodel.userNames())
		self.group_info['users_by_name'].sort()
		if self.change_info.has_key('users_by_name'):
			self.change_info.pop('users_by_name')

		self.trv_users.resizeColumnsToContent()
		self.btn_apply.setEnabled(self.isDirty())

	def isDirty(self):
		for attr,val in self.change_info.items():
			if self.group_info.has_key(attr) and self.group_info[attr]==val:
				self.change_info.pop(attr)
		if len(self.change_info.keys())==0 and not self.tbl_serviceoptions.isDirty():
			return False
		return True

	def currentServiceChanged(self,idx):
		if idx==-1:
			return
		service = str(self.cmb_services.itemData(idx).toString())
		self.tbl_serviceoptions.setContext(service,self.groupname)

	def serviceOptionChanged(self):
		self.btn_apply.setEnabled(self.isDirty())
	
	def descriptionChanged(self):
		new_txt = str(self.ted_description.toPlainText().toUtf8())
		if not self.group_info.has_key('description') and new_txt=='':
			self.change_info.pop('description')
		else:
			self.change_info['description'] = str(self.ted_description.toPlainText().toUtf8())
		self.btn_apply.setEnabled(self.isDirty())
	
	def usersContextMenu(self,pos):
		menu = QtGui.QMenu(self)
		dropaction = menu.addAction(self.tr('Drop membership'))
		if not self.permissions.count('membership.remove'):
			dropaction.setEnabled(False)
		self.connect(dropaction,QtCore.SIGNAL('triggered()'),self.dropMembership)
		menu.exec_(QtGui.QCursor.pos())

	def dropMembership(self):
		mimedata = self.usermodel.generateMimeData(self.trv_users.selectedIndexes())
		users = pickle.loads(mimedata['application/x-skolesysusers-pyobj'])
		for user in users:
			self.usermodel._removeUser(user['uidnumber'])
		
		self.change_info['users_by_name'] = list(self.usermodel.userNames())
		self.change_info['users_by_name'].sort()
		self.btn_apply.setEnabled(self.isDirty())
		self.trv_users.resizeColumnsToContent()
		

	def hook_dropOnUserView(self,obj,de):
		dragged_users = pickle.loads(de.mimeData().data('application/x-skolesysusers-pyobj'))
		for user in dragged_users:
			self.usermodel._addUser(user['uidnumber'],user['uid'],user['cn'],user['usertype_id'])
		
		self.change_info['users_by_name'] = list(self.usermodel.userNames())
		self.change_info['users_by_name'].sort()
		self.btn_apply.setEnabled(self.isDirty())
		self.trv_users.resizeColumnsToContent()

	
	def addService(self):
		add_service_dlg = QtGui.QDialog(self)
		gridlayout = QtGui.QGridLayout(add_service_dlg)
        	gridlayout.setMargin(4)
        	gridlayout.setSpacing(4)
		servicelist = QtGui.QListWidget(add_service_dlg)
		gridlayout.addWidget(servicelist,0,0,1,3)
		
		spacer = QtGui.QSpacerItem(100,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
		btn_add = QtGui.QPushButton(add_service_dlg)
		btn_add.setText(self.tr("Add"))
		btn_add.setEnabled(False)
		add_service_dlg.connect(btn_add,QtCore.SIGNAL('clicked()'),add_service_dlg.accept)
		btn_cancel = QtGui.QPushButton(add_service_dlg)
		btn_cancel.setText(self.tr("Cancel"))
		add_service_dlg.connect(btn_cancel,QtCore.SIGNAL('clicked()'),add_service_dlg.reject)
		
		def enableAddButton():
			btn_add.setEnabled(True)
			return
		
		def itemDoubleClicked(item):
			add_service_dlg.accept()
			return
		
		add_service_dlg.connect(servicelist,QtCore.SIGNAL('itemSelectionChanged()'),enableAddButton)
		add_service_dlg.connect(servicelist,QtCore.SIGNAL('itemDoubleClicked(QListWidgetItem*)'),itemDoubleClicked)

		gridlayout.addItem(spacer,1,0,1,1)
		gridlayout.addWidget(btn_add,1,1,1,1)
		gridlayout.addWidget(btn_cancel,1,2,1,1)
		
		proxy = cm.get_proxy_handle()
		all_services = proxy.list_groupservices()
		services_in_use = proxy.list_groupservices(self.groupname)
		for serv in services_in_use:
			all_services.remove(serv)
		
		for serv in all_services:
			servicelist.addItem(serv)
		
		if add_service_dlg.exec_()==QtGui.QDialog.Accepted:
			# OK a service was selected
			service = str(servicelist.currentItem().text())
			res = proxy.attach_groupservice(self.groupname,service)
			print res
			if res>=0:
				self.cmb_services.addItem(service,QtCore.QVariant(service))
				self.currentServiceChanged(self.cmb_services.currentIndex())

	def applyChanges(self):
		proxy = cm.get_proxy_handle()
		permissions = proxy.list_my_permissions()
		allow_groupadd = permissions.count('membership.create')
		allow_groupdel = permissions.count('membership.remove')
		if self.change_info.has_key('users_by_name'):
			users_before = self.group_info.pop('users_by_name')
			users_now = self.change_info.pop('users_by_name')
			for uid in users_now:
				if not users_before.count(uid) and allow_groupadd:
					proxy.groupadd(uid,self.groupname)
			for uid in users_before:
				if not users_now.count(uid)  and allow_groupdel:
					proxy.groupdel(uid,self.groupname)
		
		description = None
		if self.change_info.has_key('description'):
			description = self.change_info['description']
			
		res = 0
		if description != None:
			res = proxy.changegroup(self.groupname,description)
			
		if res >= 0:
			mainwin.get_mainwindow().emitGroupChanged(self.groupname)
		
		if self.tbl_serviceoptions.isDirty():
			self.tbl_serviceoptions.applyChanges()
		self.loadGroupData()
		self.btn_apply.setEnabled(False)


		

	def closeEvent(self,ce):
		if not self.force_close_without_save and self.isDirty():
			res = QtGui.QMessageBox.question(
				None,self.tr("Close"),self.tr("Changes have been made, do you wish to close without saving?"),
				0x00800000,0x00010000)
			if res==0x00010000:
				ce.setAccepted(False)



if __name__ == '__main__':
	import sys
	app = QtGui.QApplication(sys.argv)
	ui = GroupEditWdg(None,None)
	
	from skolesys.soap.client import SkoleSYS_Client
	cli = SkoleSYS_Client('https://mainserver.skolesys.local',8443)
	options = cli.list_groupservice_options_available('servgrp1','webservice')
	ui.tbl_serviceoptions.setOptions(options)
	ui.tbl_serviceoptions.cli = cli
	ui.show()
	sys.exit(app.exec_())
