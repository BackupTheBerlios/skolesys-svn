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
import ui_userviewwdg as ui_uvwdg
import usermodel as umod
import skolesys.definitions.userdef as userdef
import connectionmanager as cm
import pickle
import accesstools
import pyqtui4.pluggablemodelhelper as pmh
import ss_mainwindow as mainwin


class UserViewWdg(QtGui.QWidget, ui_uvwdg.Ui_UserViewWdg):
	
	def __init__(self,parent):
		QtGui.QWidget.__init__(self,parent)
		
		self.proxy = cm.get_proxy_handle()
		self.setupUi(self)
		self.setupModel()
		self.setupUserTypeCombo()
		self.setupUserView()
		self.setupGroupFilterCombo()
		self.updateUserView()
		
		self.trv_userlist.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.connect(self.trv_userlist,QtCore.SIGNAL("customContextMenuRequested(const QPoint&)"),self.userlistContextMenu)
		self.connect(self.trv_userlist,QtCore.SIGNAL("itemDoubleClicked(QTreeWidgetItem *,int)"),self.doubleClickEdit)
		
		self.connect(self.sbx_firstschoolyear_min,QtCore.SIGNAL("valueChanged(int)"),self.updateUserView)
		self.connect(self.sbx_firstschoolyear_max,QtCore.SIGNAL("valueChanged(int)"),self.updateUserView)
		
		# Recieve notice on altered, deleted or changed users
		self.connect(mainwin.get_mainwindow(),QtCore.SIGNAL("userChanged"),self.updateUserView)
		self.connect(mainwin.get_mainwindow(),QtCore.SIGNAL("userDeleted"),self.updateUserView)
		self.connect(mainwin.get_mainwindow(),QtCore.SIGNAL("userCreated"),self.updateUserView)


	def userlistContextMenu(self,pos):
		menu = QtGui.QMenu(self)
		editaction = menu.addAction(self.tr('Edit selected users...'))
		self.connect(editaction,QtCore.SIGNAL('triggered()'),self.editUsers)
		editaction = menu.addAction(self.tr('Edit memberships...'))
		self.connect(editaction,QtCore.SIGNAL('triggered()'),self.editMemberships)
		menu.addSeparator()
		editaction = menu.addAction(self.tr('Delete users...'))
		self.connect(editaction,QtCore.SIGNAL('triggered()'),self.deleteUsers)
		menu.exec_(QtGui.QCursor.pos())

	def doubleClickEdit(self,item):
		import ss_mainwindow as ss_mainwin
		idx = self.trv_userlist.currentIndex()
		mimedata = self.usermodel.generateMimeData([idx])
		for u in pickle.loads(mimedata['application/x-skolesysusers-pyobj']):
			ss_mainwin.get_mainwindow().editUser(u['uid'])
		
	def editMemberships(self):
		# Check if the user has propper permissions and present a nice message if not
		# This is ofcourse also checked on the server side.
		if not accesstools.check_permission_multi_or(('membership.create','membership.remove')):
			return

		mimedata = self.usermodel.generateMimeData(self.trv_userlist.selectedIndexes())
		users = pickle.loads(mimedata['application/x-skolesysusers-pyobj'])
		if not len(users):
			# No users selected
			return
		
		import addremoveusergroupswdg as memberships
		m = memberships.AddRemoveUserGroupsWdg(users,self)
		m.exec_()
		

	def editUsers(self):
		import ss_mainwindow as ss_mainwin
		mimedata = self.usermodel.generateMimeData(self.trv_userlist.selectedIndexes())
		for u in pickle.loads(mimedata['application/x-skolesysusers-pyobj']):
			ss_mainwin.get_mainwindow().editUser(u['uid'])
			
	def deleteUsers(self):
		mimedata = self.usermodel.generateMimeData(self.trv_userlist.selectedIndexes())
		users = pickle.loads(mimedata['application/x-skolesysusers-pyobj'])
		if not len(users):
			# No users selected
			return
		
		import removeuserswdg
		m = removeuserswdg.RemoveUsersWdg(users,self)
		m.exec_()
		
	def setupModel(self):
		self.usermodel = umod.UserModel(self.trv_userlist)
		self.modelhelper = pmh.PluggableModelHelper(self.usermodel)
		self.modelhelper.setView(self.trv_userlist)
		for colidx in xrange(self.usermodel.columnCount()):
			self.modelhelper.setColumnReadOnly(colidx)

		
	def setupUserView(self):
		self.trv_userlist.setColumnHidden(self.usermodel.columninfo['uidnumber']['columnindex'],True)
		#self.trv_userlist.setColumnHidden(self.usermodel.columninfo['uid']['columnindex'],True)
	
	def setupUserTypeCombo(self):
		self.tr("teacher","plural")
		self.tr("student","plural")
		self.tr("parent","plural")
		self.tr("other","plural")
		usertypeids = userdef.list_usertypes_by_id()
		self.cmb_usertype_filter.addItem(self.tr("All","plural users"),QtCore.QVariant(-1))
		for i in usertypeids:
			self.cmb_usertype_filter.addItem(
				self.tr(userdef.usertype_as_text(i),"plural"),
				QtCore.QVariant(i))
		self.connect(self.cmb_usertype_filter,QtCore.SIGNAL('activated(int)'),self.updateUserView)
	
	def setupGroupFilterCombo(self):
		all_groups = self.proxy.list_groups(None)
		self.cmb_groupfilter.clear()
		self.cmb_groupfilter.addItem(self.tr('All',"plural groups"),QtCore.QVariant(''))
		groupnames = all_groups.keys()
		groupnames.sort()
		for group in groupnames:
			self.cmb_groupfilter.addItem(QtCore.QString.fromUtf8(all_groups[group]['displayedName']),QtCore.QVariant(group))
		self.connect(self.cmb_groupfilter,QtCore.SIGNAL('activated(int)'),self.updateUserView)
	
	
	def updateUserView(self):
		usertype_id = None
		groupfilter = None
		idx = self.cmb_usertype_filter.currentIndex()
		if idx > -1:
			usertype_id,ok = self.cmb_usertype_filter.itemData(idx).toInt()
			if usertype_id == -1:
				usertype_id = None
	
		idx = self.cmb_groupfilter.currentIndex()
		if idx > -1:
			groupfilter = str(self.cmb_groupfilter.itemData(idx).toString().toUtf8())
			if groupfilter=='':
				# Group filter set to "All"
				groupfilter = None
		
		min_grade,max_grade = None,None
		if usertype_id==userdef.usertype_as_id('student'):
			self.lbl_gradefilter.setEnabled(True)
			self.lbl_gradefilter_to.setEnabled(True)
			self.sbx_firstschoolyear_min.setEnabled(True)
			self.sbx_firstschoolyear_max.setEnabled(True)
			min_grade = self.sbx_firstschoolyear_min.value()
			max_grade = self.sbx_firstschoolyear_max.value()
		else:
			self.lbl_gradefilter.setEnabled(False)
			self.lbl_gradefilter_to.setEnabled(False)
			self.sbx_firstschoolyear_min.setEnabled(False)
			self.sbx_firstschoolyear_max.setEnabled(False)

		self.usermodel.loadUsers(usertype_id=usertype_id,groupname=groupfilter,min_grade=min_grade,max_grade=max_grade)
			
		for colidx in xrange(self.usermodel.columnCount()):
			self.trv_userlist.resizeColumnToContents(colidx)

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
	cm.setup_connection('https://mainserver.localnet',10033)
	ui = UserViewWdg(None)
	print ui.usermodel.userNames()
	
	ui.show()
	sys.exit(app.exec_())
