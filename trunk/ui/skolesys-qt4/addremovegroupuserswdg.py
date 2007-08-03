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
import ui_addremovegroupuserswdg as baseui
import groupmodel as gmod
import usermodel as umod
import connectionmanager as cm
import pyqtui4.pluggablemodelhelper as pmh
import ss_mainwindow as mainwin
import skolesys.definitions.groupdef as groupdef
import pickle
import accesstools


class AddRemoveGroupUsersWdg(QtGui.QDialog, baseui.Ui_AddRemoveGroupUsersWdg):
	
	def __init__(self,groups_by_mime,parent):
		QtGui.QDialog.__init__(self,parent)
		self.setupUi(self)
		self.groups = groups_by_mime
		self.setupModels()
		self.btn_ok.setEnabled(False)
		self.connect(self.btn_ok,QtCore.SIGNAL('clicked()'),self.accept)
		self.connect(self.btn_cancel,QtCore.SIGNAL('clicked()'),self.reject)
		
		# Setup Permissions
		if not accesstools.check_permission('membership.create',False):
			self.trv_add.setEnabled(False)
		if not accesstools.check_permission('membership.remove',False):
			self.trv_remove.setEnabled(False)
		
		
	def setupModels(self):
		
		self.groupmodel = gmod.GroupModel(self.trv_groups)
		group_modelhelper = pmh.PluggableModelHelper(self.groupmodel)
		group_modelhelper.setView(self.trv_groups)
		for colidx in xrange(self.groupmodel.columnCount()):
			group_modelhelper.setColumnReadOnly(colidx)
		for grp in self.groups:
			if grp['grouptype_id']==groupdef.grouptype_as_id('primary'):
				# Primary groups should remain primary groups
				continue
			self.groupmodel._addGroup(grp['gid'],grp['groupname'],grp['displayed_name'],grp['grouptype_id'])

		self.trv_groups.resizeColumnsToContent()

		self.avail_usermodel = umod.UserModel(self.trv_available)
		avail_modelhelper = pmh.PluggableModelHelper(self.avail_usermodel)
		avail_modelhelper.setView(self.trv_available)
		# Hide some columns
		self.trv_available.setColumnHidden(self.avail_usermodel.columninfo['uidnumber']['columnindex'],True)
		# Add groups
		for colidx in xrange(self.avail_usermodel.columnCount()):
			avail_modelhelper.setColumnReadOnly(colidx)
		self.avail_usermodel.loadUsers()
		self.trv_available.connectEvent("dropEvent",self.hook_dropOnAvailView)
		self.trv_available.resizeColumnsToContent()
		self.avail_usermodel.setAcceptedMimeTypes(['application/x-skolesysusers-pyobj'])
		
		self.add_usermodel = umod.UserModel(self.trv_add)
		add_modelhelper = pmh.PluggableModelHelper(self.add_usermodel)
		add_modelhelper.setView(self.trv_add)
		# Hide some columns
		self.trv_add.setColumnHidden(self.add_usermodel.columninfo['uidnumber']['columnindex'],True)
		# Add groups
		for colidx in xrange(self.add_usermodel.columnCount()):
			add_modelhelper.setColumnReadOnly(colidx)
		self.trv_add.connectEvent("dropEvent",self.hook_dropOnAddView)
		self.add_usermodel.setAcceptedMimeTypes(['application/x-skolesysusers-pyobj'])

		self.remove_usermodel = umod.UserModel(self.trv_remove)
		remove_modelhelper = pmh.PluggableModelHelper(self.remove_usermodel)
		remove_modelhelper.setView(self.trv_remove)
		# Hide some columns
		self.trv_remove.setColumnHidden(self.remove_usermodel.columninfo['uidnumber']['columnindex'],True)
		# Add groups
		for colidx in xrange(self.remove_usermodel.columnCount()):
			remove_modelhelper.setColumnReadOnly(colidx)
		self.trv_remove.connectEvent("dropEvent",self.hook_dropOnRemoveView)
		self.remove_usermodel.setAcceptedMimeTypes(['application/x-skolesysusers-pyobj'])
		
		
	def isDirty(self):
		if len(self.add_usermodel.users.keys()) or \
		   len(self.remove_usermodel.users.keys()):
			return True
		return False	
		
	def hook_dropOnAddView(self,obj,de):
		dragged_users = pickle.loads(de.mimeData().data('application/x-skolesysusers-pyobj'))
		for user in dragged_users:
			self.add_usermodel._addUser(user['uidnumber'],user['uid'],user['cn'],user['usertype_id'])
			self.remove_usermodel._removeUser(user['uidnumber'])
			self.avail_usermodel._removeUser(user['uidnumber'])
		
		self.trv_add.resizeColumnsToContent()
		self.btn_ok.setEnabled(self.isDirty())


	def hook_dropOnRemoveView(self,obj,de):
		dragged_users = pickle.loads(de.mimeData().data('application/x-skolesysusers-pyobj'))
		for user in dragged_users:
			self.remove_usermodel._addUser(user['uidnumber'],user['uid'],user['cn'],user['usertype_id'])
			self.add_usermodel._removeUser(user['uidnumber'])
			self.avail_usermodel._removeUser(user['uidnumber'])

		self.trv_remove.resizeColumnsToContent()
		self.btn_ok.setEnabled(self.isDirty())

	def hook_dropOnAvailView(self,obj,de):
		dragged_users = pickle.loads(de.mimeData().data('application/x-skolesysusers-pyobj'))
		for user in dragged_users:
			self.avail_usermodel._addUser(user['uidnumber'],user['uid'],user['cn'],user['usertype_id'])
			self.add_usermodel._removeUser(user['uidnumber'])
			self.remove_usermodel._removeUser(user['uidnumber'])

		self.trv_available.resizeColumnsToContent()
		self.btn_ok.setEnabled(self.isDirty())
		
	def accept(self):
		progress = QtGui.QProgressDialog(self.tr("Applying membership changes..."),self.tr("Cancel"),0,100)
		progress.setWindowModality(QtCore.Qt.WindowModal)
		progress.show()
		
		groups = self.groupmodel.groupNames()
		add_users = self.add_usermodel.userNames()
		del_users = self.remove_usermodel.userNames()
		touched_groups = {}
		touched_users = {}
		proxy = cm.get_proxy_handle()

		steps = len(del_users)*len(groups) + len(add_users)*len(groups)
		step_factor = 100.0/steps
		step = 0
		
		if accesstools.check_permission('membership.create',False):
			for uid in add_users:
				for grp in groups:
					proxy.groupadd(uid,grp)
					touched_users[uid] = 1
					touched_groups[grp] = 1
					progress.setValue(int(step*step_factor))
					step+=1
			
		if accesstools.check_permission('membership.remove',False):
			for uid in del_users:
				for grp in groups:
					proxy.groupdel(uid,grp)
					touched_users[uid] = 1
					touched_groups[grp] = 1
					progress.setValue(int(step*step_factor))
					step+=1
		
		for uid in touched_users.keys():
			mainwin.get_mainwindow().emitUserMembershipsChanged(uid)
		for grp in touched_groups.keys():
			mainwin.get_mainwindow().emitGroupMembershipsChanged(grp)
		progress.setValue(100)
		QtGui.QDialog.accept(self)



if __name__ == '__main__':
	import sys
	app = QtGui.QApplication(sys.argv)
	ui = AddRemoveUserGroupsWdg(None)
	
	ui.show()
	sys.exit(app.exec_())
