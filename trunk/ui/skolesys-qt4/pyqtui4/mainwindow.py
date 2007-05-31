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
import sys
from PyQt4 import QtCore, QtGui
import actionhandler as ah
import qt4tools
import actionrequester as ar

class MainWindow(QtGui.QMainWindow, ah.ActionHandler):
	
	
	def __init__(self,parent,custom_central_widget=None):
		QtGui.QMainWindow.__init__(self,parent)
		ah.ActionHandler.__init__(self)
		self.toolbars = {}
		self.popupmenus = {}
		self.toolbar_is_custom = {}
		self.current_active_window = None
		self.context_caption = ""

		if custom_central_widget:
			self.setCentralWidget(custom_central_widget)
		else:
			self.workspace = QtGui.QWorkspace(self)
			self.setCentralWidget(self.workspace)
			QtCore.QObject.connect(self.workspace,QtCore.SIGNAL("windowActivated(QWidget*)"),self.slotWindowActivated)
	

  	def addMenuGroup(self,group_key,menu_title):
		if not self.popupmenus.has_key(group_key):
			self.popupmenus[group_key] = self.menuBar().addMenu( menu_title )
			return True
		return False
	
	def insertMenuItem(self,group_key,action_key):
		action = self.action(action_key)
		if action and self.popupmenus.has_key(group_key):
			self.popupmenus[group_key].addAction(action)
			return True
		return False
	
	def insertMenuSeparator(self,group_key):
		if self.popupmenus.has_key(group_key):
			self.popupmenus[group_key].addSeparator()
			return True
		return False
	
	def menu(self,group_key):
		if self.popupmenus.has_key(group_key):
			return self.popupmenus[group_key]
		


	def addToolBar(self,toolbar_key,text,custom=True,dock=QtCore.Qt.TopToolBarArea):
		if not self.toolbars.has_key(toolbar_key):
			new_toolbar = QtGui.QToolBar(text,self)
			self.toolbars[toolbar_key] = new_toolbar
			QtGui.QMainWindow.addToolBar(self,dock,new_toolbar)
			self.toolbar_is_custom[toolbar_key] = custom
	
	def insertToolBarButton(self,toolbar_key,action_key):
		action = self.action(action_key)
		if action and self.toolbars.has_key(toolbar_key):
			self.toolbars[toolbar_key].addAction(action)
			return True
		return False
	
	def insertToolBarSeparator(self,toolbar_key):
		if self.toolbars.has_key(toolbar_key):
			self.toolbars[toolbar_key].addSeparator()
			return True
		return False
		
	def toolBarKeys(self,custom_only=False):
		toolbar_keys = []
		for toolbar_key,iscustom in self.toolbar_is_custom.items():
			if custom_only and iscustom:
				toolbar_keys += [toolbar_key]
			elif not custom_only:
				toolbar_keys += [toolbar_key]
		return toolbar_keys

	def toolBarWidget(self,toolbar_key):
		if self.toolbars.has_key(toolbar_key):
			return self.toolbars[toolbar_key]

	def slotWindowActivated(self,wdg):
		if self.current_active_window:
			print self.current_active_window
			self.uninstallConnectionMap(self.current_active_window)
		
		if wdg:
			self.context_caption = wdg.windowTitle()
			
		if self.installConnectionMap(wdg):
			self.current_active_window = wdg
		else:
			self.context_caption = ""

	
class TestDockWdg(QtGui.QListView,ar.ActionRequester):
	def __init__(self,parent):
		QtGui.QListView.__init__(self,parent)
		ar.ActionRequester.__init__(self)
	
	def slotTriggerTest(self):
		print "Signal recieved on: " + self.accessibleName()

	def slotToggleTest(self,toggled):
		state = "Not checked"
		if toggled:
			state = "checked"
		print "Signal recieved on: " + self.accessibleName() + " (%s)" % state

if __name__=='__main__':
	app = QtGui.QApplication(sys.argv)
	mainwin = MainWindow(None)
	
	
	pix = qt4tools.svg2pixmap('art/tast.svg',64,64,'test.png','PNG')
	
	mainwin.addAction("testact1","test Action",pixmap=pix)
	mainwin.addAction("testact2","test Action",action_group="Gruppe1")
	mainwin.addAction("testact3","test Action",action_group="Gruppe1")
	mainwin.addAction("testact4","test Action",action_group="Gruppe2")
	
	a=TestDockWdg(mainwin.workspace)
	a.setAccessibleName("D1")
	#print a.slotTest
	a.addConnection(mainwin.action("testact1"),a.slotTriggerTest)
	mainwin.workspace.addWindow(a)
	
	b=TestDockWdg(mainwin.workspace)
	b.setAccessibleName("D2")
	b.addConnection(mainwin.action("testact1"),b.slotToggleTest,True)
	mainwin.workspace.addWindow(b)

	b=TestDockWdg(mainwin.workspace)
	b.setAccessibleName("D3")
	b.addConnection(mainwin.action("testact1"),b.slotToggleTest,True)
	mainwin.workspace.addWindow(b)
	
	b=TestDockWdg(mainwin.workspace)
	b.setAccessibleName("D4")
	b.addConnection(mainwin.action("testact1"),b.slotToggleTest,True)
	mainwin.workspace.addWindow(b)
	
	mainwin.addMenuGroup('file','File')
	mainwin.addMenuGroup('edit','Edit')
	mainwin.addToolBar('main','Main tools',False)
	mainwin.addToolBar('user_tools','User tools',True)
	mainwin.addToolBar('group_tools','Group tools',True)
	
	
	
	mainwin.insertToolBarButton("main","testact1")
	mainwin.insertToolBarButton("main","testact2")
	mainwin.insertToolBarSeparator("main")
	mainwin.insertToolBarButton("main","testact3")
	mainwin.insertMenuItem("file","testact1")
	mainwin.insertMenuItem("file","testact2")
	mainwin.insertMenuSeparator("file")
	mainwin.insertMenuItem("file","testact3")
	mainwin.insertMenuItem("file","testact4")
	
	workspace = mainwin.workspace
	
	dockwdg = QtGui.QDockWidget("Brugere",workspace)
	dockwdg.setFeatures(QtGui.QDockWidget.DockWidgetClosable | QtGui.QDockWidget.DockWidgetMovable)
	dockwdg.setWidget(TestDockWdg(dockwdg))
	mainwin.addDockWidget(QtCore.Qt.LeftDockWidgetArea,dockwdg)

	dockwdg = QtGui.QDockWidget("Grupper",workspace)
	dockwdg.setFeatures(QtGui.QDockWidget.DockWidgetClosable | QtGui.QDockWidget.DockWidgetMovable)
	dockwdg.setWidget(QtGui.QListView(dockwdg))
	mainwin.addDockWidget(QtCore.Qt.LeftDockWidgetArea,dockwdg)

	dockwdg = QtGui.QDockWidget("Tjenester",workspace)
	dockwdg.setFeatures(QtGui.QDockWidget.DockWidgetClosable | QtGui.QDockWidget.DockWidgetMovable)
	dockwdg.setWidget(QtGui.QListView(dockwdg))
	mainwin.addDockWidget(QtCore.Qt.LeftDockWidgetArea,dockwdg)

	dockwdg = QtGui.QDockWidget("Statistik",workspace)
	dockwdg.setFeatures(QtGui.QDockWidget.DockWidgetClosable | QtGui.QDockWidget.DockWidgetMovable)
	dockwdg.setWidget(QtGui.QListView(dockwdg))
	mainwin.addDockWidget(QtCore.Qt.RightDockWidgetArea,dockwdg)

	dockwdg = QtGui.QDockWidget("Andet",workspace)
	dockwdg.setFeatures(QtGui.QDockWidget.DockWidgetClosable | QtGui.QDockWidget.DockWidgetMovable)
	dockwdg.setWidget(QtGui.QListView(dockwdg))
	mainwin.addDockWidget(QtCore.Qt.RightDockWidgetArea,dockwdg)


	mainwin.show()
	sys.exit(app.exec_())
