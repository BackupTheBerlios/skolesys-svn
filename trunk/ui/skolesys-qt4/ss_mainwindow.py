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

from PyQt4 import QtCore,QtGui
import pyqtui4.mainwindow as mainwin
import pyqtui4.qt4tools as qt4tools
import skolesys.definitions.userdef as userdef
import skolesys.definitions.groupdef as groupdef
import connectionmanager as cm
import os
import paths
import accesstools

class ss_MainWindow(mainwin.MainWindow):
	def __init__(self,parent):
		self.setupCentralTabWidget()
		mainwin.MainWindow.__init__(self,parent,self.tabwidget)
		
		self.old_access_idents = []
		self.groupview = None
		self.userview = None
		self.filemanager = None
		self.accessmanager = None
		self.useredits = {}
		self.groupedits = {}
		self.setupActions()
		self.setupMenus()
		self.setupToolBars()
		self.startPermissionMonitor()
		
		self.btn_closetab = QtGui.QToolButton(self.tabwidget)
		self.btn_closetab.setAutoRaise(True)
		self.btn_closetab.setIcon(QtGui.QIcon(qt4tools.svg2pixmap(paths.path_to('art/close.svg'),10,10)))
		self.connect(self.btn_closetab,QtCore.SIGNAL('clicked()'),self.removeTab)
		self.tabwidget.setCornerWidget(self.btn_closetab)
		self.setWindowIcon(QtGui.QIcon(qt4tools.svg2pixmap(paths.path_to('art/logo-non-gradient.svg'),10,10)))
		self.setupPermissions(cm.get_proxy_handle().list_my_permissions())


	def setupActions(self):
		# Actions
		
		a = self.addAction('import_users',self.tr('Import users...'))
		self.connect(a,QtCore.SIGNAL('triggered()'),self.importUsers)
		a.setDisabled(True)
		
		a = self.addAction('export_users',self.tr('Export users...'))
		self.connect(a,QtCore.SIGNAL('triggered()'),self.exportUsers)
		a.setDisabled(True)
		
		a = self.addAction('export_groups',self.tr('Export groups...'))
		self.connect(a,QtCore.SIGNAL('triggered()'),self.exportGroups)
		a.setDisabled(True)

		a = self.addAction('exit',self.tr('Exit'))
		self.connect(a,QtCore.SIGNAL('triggered()'),self.close)
			
		a = self.addAction('open_filemanager',self.tr('File manager'))
		self.connect(a,QtCore.SIGNAL('triggered()'),self.openFileManager)
		a.setIcon(QtGui.QIcon(qt4tools.svg2pixmap(paths.path_to('art/stats.svg'),16,16)))

		a = self.addAction('exec_creategroupwizard',self.tr('Create group...'))
		self.connect(a,QtCore.SIGNAL('triggered()'),self.execCreateGroupWizard)
		a.setIcon(QtGui.QIcon(qt4tools.svg2pixmap(paths.path_to('art/new_group.svg'),16,16)))

		a = self.addAction('exec_createuserwizard',self.tr('Create user...'))
		self.connect(a,QtCore.SIGNAL('triggered()'),self.execCreateUserWizard)
		a.setIcon(QtGui.QIcon(qt4tools.svg2pixmap(paths.path_to('art/new_user.svg'),16,16)))

		a = self.addAction('exec_accessmanager',self.tr('Access Manager...'))
		self.connect(a,QtCore.SIGNAL('triggered()'),self.execAccessManager)
		a.setIcon(QtGui.QIcon(qt4tools.svg2pixmap(paths.path_to('art/access.svg'),16,16)))

		a = self.addAction('show_users',self.tr('Show Users'))
		a.setCheckable(True)
		self.connect(a,QtCore.SIGNAL('toggled(bool)'),self.showUserView)
		
		a = self.addAction('show_groups',self.tr('Show Groups'))
		a.setCheckable(True)
		self.connect(a,QtCore.SIGNAL('toggled(bool)'),self.showGroupView)
		
		self.connect(self,QtCore.SIGNAL('permissionsChanged'),self.setupPermissions)
		
		
	def removeTab(self,idx=None):
		"""
		Remove the tab at index idx gracefully. If idx is not passed to removeTab
		the current tab is attempted to be removed. First tab cannot be removed.
		If a tab was removed the index of the tab is returned, otherwise None
		"""
		if idx==None:
			idx = self.tabwidget.currentIndex()
		wdg = self.tabwidget.widget(idx)
		if idx>0:
			if wdg.close():
				if self.useredits.has_key(wdg):
					self.useredits.pop(self.useredits[wdg])
					self.useredits.pop(wdg)
				if self.groupedits.has_key(wdg):
					self.groupedits.pop(self.groupedits[wdg])
					self.groupedits.pop(wdg)
				if self.filemanager==wdg:
					self.filemanager = None
				self.tabwidget.removeTab(idx)
				del wdg
				return idx
		return None

	def removeTabByWidget(self,wdg):
		"""
		Remove the tab at index idx gracefully. If idx is not passed to removeTab
		the current tab is attempted to be removed. First tab cannot be removed.
		If a tab was removed the index of the tab is returned, otherwise None
		"""
		if not wdg:
			return
		idx = self.tabwidget.indexOf(wdg)
		if idx<0:
			return
		self.removeTab(idx)

	def setupCentralTabWidget(self):
		self.tabwidget = QtGui.QTabWidget(None)

	def setupMenus(self):
		self.addMenuGroup('file',self.tr('File'))
		self.insertMenuItem('file','import_users')
		self.insertMenuSeparator('file')
		self.insertMenuItem('file','export_users')
		self.insertMenuItem('file','export_groups')
		self.insertMenuSeparator('file')
		self.insertMenuItem('file','exit')
		
		self.addMenuGroup('view',self.tr('View'))
		self.insertMenuItem('view','show_groups')
		self.insertMenuItem('view','show_users')

		self.addMenuGroup('tools',self.tr('Tools'))
		self.insertMenuItem('tools','open_filemanager')
		self.insertMenuItem('tools','exec_createuserwizard')
		self.insertMenuItem('tools','exec_creategroupwizard')
		self.insertMenuSeparator('tools')
		self.insertMenuItem('tools','exec_accessmanager')

	def setupToolBars(self):
		self.addToolBar('tools',self.tr('Tools'))
		self.insertToolBarButton('tools','exec_createuserwizard')
		self.insertToolBarButton('tools','exec_creategroupwizard')
		self.addToolBar('views',self.tr('Views'),dock=QtCore.Qt.TopToolBarArea)
		self.insertToolBarButton('views','show_users')
		self.insertToolBarButton('views','show_groups')

	def insertDockWidget(self,wdg,title,dock_area=QtCore.Qt.LeftDockWidgetArea):
		dockwdg = QtGui.QDockWidget(title,self)
		dockwdg.setFeatures(QtGui.QDockWidget.DockWidgetClosable | QtGui.QDockWidget.DockWidgetMovable)
		dockwdg.setWidget(wdg)
		self.addDockWidget(dock_area,dockwdg)
		return dockwdg

	def insertWorkspaceWidget(self,wdg,title):
		wdg.setParent(self.workspace)
		wdg.setAccessibleName(title)
		self.workspace.addWindow(wdg)
	
	def setupViews(self):
		import tooltabwdg as tooltab
		import groupviewwdg as groupview
		import userviewwdg as userview
		
		self.groupview = groupview.GroupViewWdg(None)
		self.connect(self.groupview,QtCore.SIGNAL('viewShown'),self.action('show_groups').setChecked)
		self.groupviewdock = self.insertDockWidget(self.groupview,self.tr("Groups"))
		self.userview = userview.UserViewWdg(None)
		self.connect(self.userview,QtCore.SIGNAL('viewShown'),self.action('show_users').setChecked)
		self.userviewdock = self.insertDockWidget(self.userview,self.tr("Users"))
		
		tooltab = tooltab.ToolTabWdg(self.tabwidget)
		self.tabwidget.addTab(tooltab,QtGui.QIcon(qt4tools.svg2pixmap(paths.path_to('art/kfm_home.svg'),16,16)),self.tr('Home'))

	def showUserView(self,checked):
		if self.userview == None:
			return
		if checked:
			self.userviewdock.show()
		else:
			self.userviewdock.hide()
	
	def showGroupView(self,checked):
		if self.groupview == None:
			return
		if checked:
			self.groupviewdock.show()
		else:
			self.groupviewdock.hide()

	def editUser(self,uid):
		# Check if the user has propper permissions and present a nice message if not
		# This is ofcourse also checked on the server side.
		may_open = False
		if uid==cm.get_binded_user() and accesstools.check_permission('user.self.modify',False):
			may_open = True
		elif accesstools.check_permission_multi_or(('user.modify','user.view')):
			may_open = True

		if may_open == False:
			return
		
		if self.useredits.has_key(uid):
			self.tabwidget.setCurrentWidget(self.useredits[uid])
			return
		import usereditwdg as usered
		useredit = usered.UserEditWdg(uid,self.tabwidget)
		self.useredits[useredit] = uid
		self.useredits[uid] = useredit
		tab_title = useredit.led_firstname.text()+" "+useredit.led_lastname.text()
		
		usericon = paths.path_to('art/student.svg')
		if os.path.exists(paths.path_to('art/%s.svg') % userdef.usertype_as_text(useredit.user_info['usertype_id'])):
			usericon = paths.path_to('art/%s.svg') % userdef.usertype_as_text(useredit.user_info['usertype_id'])
		self.tabwidget.addTab(useredit,QtGui.QIcon(qt4tools.svg2pixmap(usericon,32,32)),tab_title)
		self.tabwidget.setCurrentWidget(useredit)
		
	def closeUserEdits(self,selfmod=False):
		"""
		Close all user edit tabs
		"""
		useredits = list(self.useredits.keys())
		for usered in useredits:
			if type(usered) == str:
				continue
			if selfmod and usered.username==cm.get_binded_user():
				continue
			usered.force_close_without_save = True
			self.removeTabByWidget(usered)

		
	def editGroup(self,groupname,displayed_name):
		# Check if the user has propper permissions and present a nice message if not
		# This is ofcourse also checked on the server side.
		if not accesstools.check_permission_multi_or(('group.modify','group.view')):
			return
		if self.groupedits.has_key(groupname):
			self.tabwidget.setCurrentWidget(self.groupedits[groupname])
			return
		import groupeditwdg as grouped
		groupedit = grouped.GroupEditWdg(groupname,self.tabwidget)
		self.groupedits[groupedit] = groupname
		self.groupedits[groupname] = groupedit
		tab_title = QtCore.QString.fromUtf8(displayed_name) #groupedit.led_firstname.text()+" "+groupedit.led_lastname.text()
		self.tabwidget.addTab(groupedit,QtGui.QIcon(qt4tools.svg2pixmap(paths.path_to('art/group.svg'),16,16)),tab_title)
		self.tabwidget.setCurrentWidget(groupedit)
		
	def closeGroupEdits(self):
		groupedits = list(self.groupedits.keys())
		for grouped in groupedits:
			if type(grouped) == str:
				continue
			grouped.force_close_without_save = True
			self.removeTabByWidget(grouped)
	
	
	# Tools
	
	def importUsers(self):
		pass
	
	def exportUsers(self):
		pass
	
	def exportGroups(self):
		pass
	
	def execCreateUserWizard(self):
		# Check if the user has propper permissions and present a nice message if not
		# This is ofcourse also checked on the server side.
		if not accesstools.check_permission('user.create'):
			return
		
		import createuserwizard as cuw
		wiz = cuw.CreateUserWizard(self)
		wiz.exec_()

	def execCreateGroupWizard(self):
		# Check if the user has propper permissions and present a nice message if not
		# This is ofcourse also checked on the server side.
		if not accesstools.check_permission('group.create'):
			return

		import creategroupwizard as cgw
		wiz = cgw.CreateGroupWizard(self)
		wiz.exec_()
	
	def execAccessManager(self):
		# Check if the user has propper permissions and present a nice message if not
		# This is ofcourse also checked on the server side.
		if not accesstools.check_permission('access.granter'):
			return

		import accessmanagerwdg as amwdg
		if not self.accessmanager:
			self.accessmanager = amwdg.AccessManagerWdg(self)
		self.accessmanager.exec_()
		
	def openFileManager(self):
		# Check if the user has propper permissions and present a nice message if not
		# This is ofcourse also checked on the server side.
		if not accesstools.check_permission('file.browse'):
			return
		
		if self.filemanager!=None:
			self.tabwidget.setCurrentWidget(self.filemanager)
			return

		import filemanagerwdg as fileman
		self.filemanager = fileman.FileManagerWdg(self.tabwidget)
		tab_title = self.tr("File manager")
		self.tabwidget.addTab(self.filemanager,QtGui.QIcon(qt4tools.svg2pixmap(paths.path_to('art/stats.svg'),16,16)),tab_title)
		self.tabwidget.setCurrentWidget(self.filemanager)
		
		


	
	def closeEvent(self,ce):
		while self.tabwidget.count()>1:
			if self.removeTab(self.tabwidget.count()-1) == None:
				ce.setAccepted(False)
				break
	
	# Permissions
	def startPermissionMonitor(self):
		perm_timer = QtCore.QTimer(self);
		self.connect(perm_timer, QtCore.SIGNAL('timeout()'), self.checkPermissions);
		perm_timer.start(5000);
	
	def checkPermissions(self):
		conn = cm.get_connection()
		if conn==None:
			print "No connection"
			return
		if not conn.proxy.test_binded():
			print "Not binded"
			return
		access_idents = conn.proxy.list_my_permissions()
		if not self.old_access_idents == access_idents:
			print "permissions_changed"
			self.old_access_idents = access_idents
			self.emitPermissionsChanged(access_idents)
		
	def setupPermissions(self,access_idents):
		action_map_perm = {
			'import_users' : 'user.create',
			'export_users' : 'user.view',
			'export_groups' : 'group.view',
			'open_filemanager' : 'file.browse',
			'exec_creategroupwizard' : 'group.create',
			'exec_createuserwizard' : 'user.create',
			'exec_accessmanager' : 'access.granter'
		}
		for action_key,acc_ident in action_map_perm.items():
			if not access_idents.count(acc_ident):
				self.action(action_key).setDisabled(True)
			else:
				self.action(action_key).setDisabled(False)
		
		if accesstools.check_permission_multi_or(('user.modify','user.view'),False)==False:
			# No access to users allowed
			self.closeUserEdits(accesstools.check_permission('user.self.modify',False))
		
		if accesstools.check_permission_multi_or(('group.modify','group.view'),False)==False:
			# No access to users allowed
			self.closeGroupEdits()
	
		if accesstools.check_permission('file.browse',False)==False:
			# No access to users allowed
			self.removeTabByWidget(self.filemanager)
			
	# Signal events
	
	# Users
	def emitUserCreated(self,uid):
		self.emit(QtCore.SIGNAL("userCreated"),uid)

	def emitUserChanged(self,uid):
		self.emit(QtCore.SIGNAL("userChanged"),uid)
	
	def emitUserDeleted(self,uid):
		self.emit(QtCore.SIGNAL("userDeleted"),uid)

	def emitUserMembershipsChanged(self,uid):
		self.emit(QtCore.SIGNAL("userMembershipsChanged"),uid)
	
	# Groups
	def emitGroupCreated(self,groupname):
		self.emit(QtCore.SIGNAL("groupCreated"),groupname)

	def emitGroupChanged(self,groupname):
		self.emit(QtCore.SIGNAL("groupChanged"),groupname)
	
	def emitGroupDeleted(self,groupname):
		self.emit(QtCore.SIGNAL("groupDeleted"),groupname)

	def emitGroupMembershipsChanged(self,groupname):
		self.emit(QtCore.SIGNAL("groupMembershipsChanged"),groupname)
		
	def emitPermissionsChanged(self,access_idents):
		self.emit(QtCore.SIGNAL("permissionsChanged"),access_idents)

singleton_mainwindow = None

def get_mainwindow():
	global singleton_mainwindow
	if singleton_mainwindow==None:
		singleton_mainwindow = ss_MainWindow(None)
	return singleton_mainwindow
