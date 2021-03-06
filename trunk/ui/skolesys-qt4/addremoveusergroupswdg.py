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
import ui_addremoveusergroupswdg as baseui
import groupmodel as gmod
import usermodel as umod
import connectionmanager as cm
import pyqtui4.pluggablemodelhelper as pmh
import ss_mainwindow as mainwin
import skolesys.definitions.groupdef as groupdef
import pickle
import accesstools

class WorkerThread(QtCore.QThread):
	def __init__(self,func,parent):
		QtCore.QThread.__init__(self,parent)
		self.func = func
		
	def run(self):
		self.func()


class AddRemoveUserGroupsWdg(QtGui.QDialog, baseui.Ui_AddRemoveUserGroupsWdg):
	
	def __init__(self,users_by_mime,parent):
		QtGui.QDialog.__init__(self,parent)
		self.setupUi(self)
		self.users = users_by_mime
		self.setupModels()
		self.btn_ok.setEnabled(False)
		self.connect(self.btn_ok,QtCore.SIGNAL('clicked()'),self.accept)
		self.connect(self.btn_cancel,QtCore.SIGNAL('clicked()'),self.reject)
		
		# Setup permissions
		if not accesstools.check_permission('membership.create',False):
			self.trv_add.setEnabled(False)
		if not accesstools.check_permission('membership.remove',False):
			self.trv_remove.setEnabled(False)

		
	def setupModels(self):
		
		self.usermodel = umod.UserModel(self.trv_users)
		user_modelhelper = pmh.PluggableModelHelper(self.usermodel)
		user_modelhelper.setView(self.trv_users)
		for colidx in xrange(self.usermodel.columnCount()):
			user_modelhelper.setColumnReadOnly(colidx)
		for user in self.users:
			self.usermodel._addUser(user['uidnumber'],user['uid'],user['cn'],user['usertype_id'])

		self.trv_users.resizeColumnsToContent()

		self.avail_groupmodel = gmod.GroupModel(self.trv_available)
		avail_modelhelper = pmh.PluggableModelHelper(self.avail_groupmodel)
		avail_modelhelper.setView(self.trv_available)
		# Hide some columns
		self.trv_available.setColumnHidden(self.avail_groupmodel.columninfo['gid']['columnindex'],True)
		self.trv_available.setColumnHidden(self.avail_groupmodel.columninfo['groupname']['columnindex'],True)
		# Add groups
		for colidx in xrange(self.avail_groupmodel.columnCount()):
			avail_modelhelper.setColumnReadOnly(colidx)
		self.avail_groupmodel.exclude_grouptype_ids = [groupdef.grouptype_as_id('primary')]
		self.avail_groupmodel.loadGroups()
		self.trv_available.connectEvent("dropEvent",self.hook_dropOnAvailView)
		self.trv_available.resizeColumnsToContent()
		self.avail_groupmodel.setAcceptedMimeTypes(['application/x-skolesysgroups-pyobj'])
		
		self.add_groupmodel = gmod.GroupModel(self.trv_add)
		add_modelhelper = pmh.PluggableModelHelper(self.add_groupmodel)
		add_modelhelper.setView(self.trv_add)
		# Hide some columns
		self.trv_add.setColumnHidden(self.add_groupmodel.columninfo['gid']['columnindex'],True)
		self.trv_add.setColumnHidden(self.add_groupmodel.columninfo['groupname']['columnindex'],True)
		# Add groups
		for colidx in xrange(self.add_groupmodel.columnCount()):
			add_modelhelper.setColumnReadOnly(colidx)
		self.trv_add.connectEvent("dropEvent",self.hook_dropOnAddView)
		self.add_groupmodel.setAcceptedMimeTypes(['application/x-skolesysgroups-pyobj'])

		self.remove_groupmodel = gmod.GroupModel(self.trv_remove)
		remove_modelhelper = pmh.PluggableModelHelper(self.remove_groupmodel)
		remove_modelhelper.setView(self.trv_remove)
		# Hide some columns
		self.trv_remove.setColumnHidden(self.remove_groupmodel.columninfo['gid']['columnindex'],True)
		self.trv_remove.setColumnHidden(self.remove_groupmodel.columninfo['groupname']['columnindex'],True)
		# Add groups
		for colidx in xrange(self.remove_groupmodel.columnCount()):
			remove_modelhelper.setColumnReadOnly(colidx)
		self.trv_remove.connectEvent("dropEvent",self.hook_dropOnRemoveView)
		self.remove_groupmodel.setAcceptedMimeTypes(['application/x-skolesysgroups-pyobj'])
		
		
	def isDirty(self):
		if len(self.add_groupmodel.groups.keys()) or \
		   len(self.remove_groupmodel.groups.keys()):
			return True
		return False	
		
	def hook_dropOnAddView(self,obj,de):
		dragged_groups = pickle.loads(de.mimeData().data('application/x-skolesysgroups-pyobj'))
		for grp in dragged_groups:
			self.add_groupmodel._addGroup(grp['gid'],grp['groupname'],grp['displayed_name'],grp['grouptype_id'])
			self.remove_groupmodel._removeGroup(grp['gid'])
			self.avail_groupmodel._removeGroup(grp['gid'])
		
		self.trv_add.resizeColumnsToContent()
		self.btn_ok.setEnabled(self.isDirty())


	def hook_dropOnRemoveView(self,obj,de):
		dragged_groups = pickle.loads(de.mimeData().data('application/x-skolesysgroups-pyobj'))
		for grp in dragged_groups:
			self.remove_groupmodel._addGroup(grp['gid'],grp['groupname'],grp['displayed_name'],grp['grouptype_id'])
			self.add_groupmodel._removeGroup(grp['gid'])
			self.avail_groupmodel._removeGroup(grp['gid'])

		self.trv_remove.resizeColumnsToContent()
		self.btn_ok.setEnabled(self.isDirty())

	def hook_dropOnAvailView(self,obj,de):
		dragged_groups = pickle.loads(de.mimeData().data('application/x-skolesysgroups-pyobj'))
		for grp in dragged_groups:
			self.avail_groupmodel._addGroup(grp['gid'],grp['groupname'],grp['displayed_name'],grp['grouptype_id'])
			self.add_groupmodel._removeGroup(grp['gid'])
			self.remove_groupmodel._removeGroup(grp['gid'])

		self.trv_available.resizeColumnsToContent()
		self.btn_ok.setEnabled(self.isDirty())
		
	def accept(self):
		progress = QtGui.QProgressDialog(self.tr("Applying membership changes..."),self.tr("Cancel"),0,100)
		progress.setWindowModality(QtCore.Qt.WindowModal)
		progress.show()
		users = self.usermodel.userNames()
		add_groups = self.add_groupmodel.groupNames()
		del_groups = self.remove_groupmodel.groupNames()
		touched_groups = {}
		touched_users = {}
		proxy = cm.get_proxy_handle()

		steps = len(del_groups)*len(users) + len(add_groups)*len(users)
		step_factor = 100.0/steps
		step = 0

		if accesstools.check_permission('membership.create',False):
			for grp in add_groups:
				for uid in users:
					proxy.groupadd(uid,grp)
					touched_users[uid] = 1
					touched_groups[grp] = 1
					progress.setValue(int(step*step_factor))
					step+=1
			
		if accesstools.check_permission('membership.remove',False):
			for grp in del_groups:
				for uid in users:
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
