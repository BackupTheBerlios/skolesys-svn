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
import ui_usereditwdg as baseui
import pyqtui4.actionrequester as ar
import groupmodel as gmod
import connectionmanager as cm
import pickle
import skolesys.definitions.groupdef as groupdef
import skolesys.definitions.userdef as userdef
import pyqtui4.pluggablemodelhelper as pmh
import ss_mainwindow as mainwin



class UserEditWdg(QtGui.QWidget, baseui.Ui_UserEditWdg,ar.ActionRequester):
	
	def __init__(self,username,parent):
		QtGui.QWidget.__init__(self,parent)
		ar.ActionRequester.__init__(self)
		self.change_info = {}
		self.user_info = {}
		self.gid_add_list = []
		self.gid_rm_list = []
		self.force_close_without_save = False
		self.permissions = cm.get_proxy_handle().list_my_permissions()
		
		self.username = username
		self.setupUi(self)
		
		self.groupmodel = gmod.GroupModel(self.trv_groups)
		self.modelhelper = pmh.PluggableModelHelper(self.groupmodel)
		self.modelhelper.setView(self.trv_groups)
		for colidx in xrange(self.groupmodel.columnCount()):
			self.modelhelper.setColumnReadOnly(colidx)
		
		self.loadUserData()
		self.groupmodel.setAcceptedMimeTypes(['application/x-skolesysgroups-pyobj'])
		
		# Connect buttons
		self.connect(self.btn_apply,QtCore.SIGNAL('clicked()'),self.applyChanges)
		
		# Primary group Combobox connections
		self.connect(self.cmb_primary_group,QtCore.SIGNAL('activated(int)'),self.primaryGroupChanged)
		
		# Connect first name , last name line edits
		self.connect(self.led_firstname,QtCore.SIGNAL('textChanged(const QString&)'),self.firstNameChanged)
		self.connect(self.led_lastname,QtCore.SIGNAL('textChanged(const QString&)'),self.lastNameChanged)

		# group list connections
		self.trv_groups.connectEvent("dropEvent",self.hook_dropOnGroupView)
		self.trv_groups.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.connect(self.trv_groups,QtCore.SIGNAL("customContextMenuRequested(const QPoint&)"),self.groupsContextMenu)
		
		# Connect change signals
		self.connect(mainwin.get_mainwindow(),QtCore.SIGNAL('userMembershipsChanged'),self.updateGroupsView)
		
		# Change password
		self.connect(self.btn_passwd,QtCore.SIGNAL('clicked()'),self.changePassword)
		
		self.tr("teacher","singular")
		self.tr("student","singular")
		self.tr("parent","singular")
		self.tr("other","singular")
		
		self.setupPermissions(cm.get_proxy_handle().list_my_permissions())
			
		self.connect(mainwin.get_mainwindow(),QtCore.SIGNAL('permissionsChanged'),self.setupPermissions)
		
	
	def setupPermissions(self,access_idents):
		self.permissions = access_idents
		may_modify = False
		if access_idents.count('user.modify') or \
		   (access_idents.count('user.self.modify') and cm.get_binded_user()==self.username):
			may_modify = True

		if may_modify:
			self.force_close_without_save = False
			self.setEnabled(True)
		else:
			self.force_close_without_save = True
			self.setEnabled(False)
		
		if access_idents.count('membership.create'):
			self.trv_groups.setEnabled(True)
		else:
			self.trv_groups.setEnabled(False)
		
	
	def isDirty(self):
		for attr,val in self.change_info.items():
			if self.user_info.has_key(attr) and self.user_info[attr]==val:
				self.change_info.pop(attr)
		if len(self.change_info.keys())==0:
			return False
		return True

	def loadUserData(self):
		proxy = cm.get_proxy_handle()
		self.user_info = proxy.list_users(uid=self.username)
		if self.user_info.has_key(self.username):
			self.change_info = {}
			self.user_info = self.user_info[self.username]
			self.lbl_usertype.setText(self.tr(userdef.usertype_as_text(self.user_info['usertype_id']),'singular'))
			self.lbl_username.setText(QtCore.QString().fromUtf8(self.user_info['uid']))
			self.led_firstname.setText(QtCore.QString().fromUtf8(self.user_info['givenName']))
			self.led_lastname.setText(QtCore.QString().fromUtf8(self.user_info['sn']))
			gid_number = int(self.user_info['gidNumber'])
			self.cmb_primary_group.clear()
			for groupname,details in proxy.list_groups(groupdef.grouptype_as_id('primary')).items():
				self.cmb_primary_group.addItem(
					QtCore.QString().fromUtf8(details['displayedName']),
					QtCore.QVariant(details['gidNumber']))
			self.cmb_primary_group.setCurrentIndex(self.cmb_primary_group.findData(QtCore.QVariant(self.user_info['gidNumber'])))
			
		self.updateGroupsView()

	def updateGroupsView(self,uid=None):
		if uid!=None and uid!=self.username:
			return
		self.groupmodel.loadGroups(username=self.username)
		self.user_info['groups_by_name'] = list(self.groupmodel.groupNames())
		self.user_info['groups_by_name'].sort()
		if self.change_info.has_key('groups_by_name'):
			self.change_info.pop('groups_by_name')
		self.trv_groups.resizeColumnsToContent()
		self.btn_apply.setEnabled(self.isDirty())


	def groupsContextMenu(self,pos):
		menu = QtGui.QMenu(self)
		dropaction = menu.addAction(self.tr('Drop membership'))
		if not self.permissions.count('membership.remove'):
			dropaction.setEnabled(False)
		self.connect(dropaction,QtCore.SIGNAL('triggered()'),self.dropMembership)
		menu.exec_(QtGui.QCursor.pos())

	def lastNameChanged(self,txt):
		self.change_info['sn'] = str(txt.toUtf8())
		self.btn_apply.setEnabled(self.isDirty())
			
	
	def firstNameChanged(self,txt):
		self.change_info['givenName'] = str(txt.toUtf8())
		self.btn_apply.setEnabled(self.isDirty())
	
	def primaryGroupChanged(self,idx):
		gid_number = str(self.cmb_primary_group.itemData(self.cmb_primary_group.currentIndex()).toString())
		self.change_info['gidNumber'] = gid_number
		self.btn_apply.setEnabled(self.isDirty())


	def dropMembership(self):
		mimedata = self.groupmodel.generateMimeData(self.trv_groups.selectedIndexes())
		groups = pickle.loads(mimedata['application/x-skolesysgroups-pyobj'])
		for grp in groups:
			self.groupmodel._removeGroup(grp['gid'])
		
		self.change_info['groups_by_name'] = list(self.groupmodel.groupNames())
		self.change_info['groups_by_name'].sort()
		self.btn_apply.setEnabled(self.isDirty())
		self.trv_groups.resizeColumnsToContent()
		

	def hook_dropOnGroupView(self,obj,de):
		dragged_groups = pickle.loads(de.mimeData().data('application/x-skolesysgroups-pyobj'))
		for grp in dragged_groups:
			if grp['grouptype_id']==groupdef.grouptype_as_id('primary'):
				# Hold primary groups clear from secondary memberships
				continue
			self.groupmodel._addGroup(grp['gid'],grp['groupname'],grp['displayed_name'],grp['grouptype_id'])
		
		self.change_info['groups_by_name'] = list(self.groupmodel.groupNames())
		self.change_info['groups_by_name'].sort()
		self.btn_apply.setEnabled(self.isDirty())
		self.trv_groups.resizeColumnsToContent()
		
	def applyChanges(self):
		proxy = cm.get_proxy_handle()
		# Groups
		permissions = proxy.list_my_permissions()
		allow_groupadd = permissions.count('membership.create')
		allow_groupdel = permissions.count('membership.remove')
		if self.change_info.has_key('groups_by_name'):
			groups_before = self.user_info.pop('groups_by_name')
			groups_now = self.change_info.pop('groups_by_name')
			for groupname in groups_now:
				if not groups_before.count(groupname) and allow_groupadd:
					proxy.groupadd(self.username,groupname)
			for groupname in groups_before:
				if not groups_now.count(groupname) and allow_groupdel:
					proxy.groupdel(self.username,groupname)
		
		# Standard info
		givenname,familyname,primarygroup,firstyear = None,None,None,None
		if self.change_info.has_key('givenName'):
			givenname = self.change_info['givenName']
		if self.change_info.has_key('sn'):
			familyname = self.change_info['sn']
		if self.change_info.has_key('gidNumber'):
			primarygroup = self.change_info['gidNumber']
		if self.change_info.has_key('firstSchoolYear'):
			firstyear = self.change_info['firstSchoolYear']
		res = proxy.changeuser(self.username,givenname,familyname,None,primarygroup,firstyear)
		print res
		if res >= 0:
			mainwin.get_mainwindow().emitUserChanged(self.username)
		self.loadUserData()
		self.btn_apply.setEnabled(False)
		
	def closeEvent(self,ce):
		if not self.force_close_without_save and self.isDirty():
			res = QtGui.QMessageBox.question(
				None,self.tr("Close"),self.tr("Changes have been made, do you wish to close without saving?"),
				0x00800000,0x00010000)
			if res==0x00010000:
				ce.setAccepted(False)
		
	def changePassword(self):
		proxy = cm.get_proxy_handle()
		import changepasswordwdg as chpasswd
		passwd = chpasswd.promptForPassword()
		res = proxy.changeuser(self.username,None,None,passwd,None,None)
		print res
		
if __name__ == '__main__':
	import sys
	app = QtGui.QApplication(sys.argv)
	ui = UserEditWdg(conn,None)
	
	ui.show()
	sys.exit(app.exec_())
