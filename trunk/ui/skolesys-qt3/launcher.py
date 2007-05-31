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
from qt import *
from widgetdialog import WidgetDialog

# User manager
from usermanagerwdg import UserManagerWdg
from createuserwdg import CreateUserWdg
from removeuserwdg import RemoveUserWdg
from addremoveusergroupswdg import AddRemoveUserGroupsWdg

# Group manager
from groupmanagerwdg import GroupManagerWdg
from creategroupwdg import CreateGroupWdg
from removegroupwdg import RemoveGroupWdg
from addremovegroupuserswdg import AddRemoveGroupUsersWdg

from settings import glob_settings

def execUserManager(conn):
	# Setup dialog
	dlg = WidgetDialog(buttons=3,cancel_btn=False)
	dlg.setCaption(qApp.translate("UserManagerWdg","User Manager"))
	dlg.btnCustom1.setText(qApp.translate("UserManagerWdg","Create user..."))
	dlg.btnCustom2.setText(qApp.translate("UserManagerWdg","Remove user(s)..."))
	dlg.btnOK.setText(qApp.translate("UserManagerWdg","Close"))
	
	# Inner widget
	userman = UserManagerWdg(conn,None,"UserManagerWdg")
	dlg.setWidget(userman,True,qApp.translate("UserManagerWdg","Users"))
	QObject.connect(dlg.btnCustom1,SIGNAL("clicked()"),userman.createUser)
	QObject.connect(dlg.btnCustom2,SIGNAL("clicked()"),userman.removeUser)
	
	# Extension
	#a = QFileDialog()
	#dlg.setFoldedExtension(a)
	
	glob_settings.widgetGeometry('skolesys-ui/UserManager',dlg)
	dlg.exec_loop()
	glob_settings.setWidgetGeometry('skolesys-ui/UserManager',dlg)
	
	

def execCreateUser(conn):
	dlg = WidgetDialog()
	dlg.setCaption(qApp.translate("CreateUserWdg","Create User"))
	createuser = CreateUserWdg(conn)
	dlg.setWidget(createuser,True,qApp.translate("CreateUserWdg","User information"))
	glob_settings.widgetGeometry('skolesys-ui/CreateUser',dlg)
	dlg.exec_loop()
	glob_settings.setWidgetGeometry('skolesys-ui/CreateUser',dlg)

def execRemoveUser(conn,uids):
	dlg = WidgetDialog()
	dlg.setCaption(qApp.translate("RemoveUserWdg","Remove User(s)"))
	removeuser = RemoveUserWdg(conn,uids)
	dlg.setWidget(removeuser,True,qApp.translate("CreateUserWdg","User information"))
	glob_settings.widgetGeometry('skolesys-ui/RemoveUser',dlg)
	dlg.exec_loop()
	glob_settings.setWidgetGeometry('skolesys-ui/RemoveUser',dlg)

def execGroupManager(conn):
	# Setup dialog
	dlg = WidgetDialog(buttons=3,cancel_btn=False)
	dlg.setCaption(qApp.translate("GroupManagerWdg","Group Manager"))
	dlg.btnCustom1.setText(qApp.translate("GroupManagerWdg","Create group..."))
	dlg.btnCustom2.setText(qApp.translate("GroupManagerWdg","Remove group(s)..."))
	dlg.btnOK.setText(qApp.translate("GroupManagerWdg","Close"))
	
	# Inner widget
	grpman = GroupManagerWdg(conn,None,"GroupManagerWdg")
	dlg.setWidget(grpman,True,qApp.translate("GroupManagerWdg","Groups"))
	QObject.connect(dlg.btnCustom1,SIGNAL("clicked()"),grpman.createGroup)
	QObject.connect(dlg.btnCustom2,SIGNAL("clicked()"),grpman.removeGroup)
	glob_settings.widgetGeometry('skolesys-ui/GroupManager',dlg)
	dlg.exec_loop()
	glob_settings.setWidgetGeometry('skolesys-ui/GroupManager',dlg)

def execCreateGroup(conn):
	dlg = WidgetDialog()
	dlg.setCaption(qApp.translate("CreateGroupWdg","Create Group"))
	creategroup = CreateGroupWdg(conn)
	dlg.setWidget(creategroup,True,qApp.translate("CreateUserWdg","Group information"))
	glob_settings.widgetGeometry('skolesys-ui/CreateGroup',dlg)
	dlg.exec_loop()
	glob_settings.setWidgetGeometry('skolesys-ui/CreateGroup',dlg)

def execRemoveGroup(conn,groupnames):
	dlg = WidgetDialog()
	dlg.setCaption(qApp.translate("RemoveGroupWdg","Remove Group(s)"))
	removegroup = RemoveGroupWdg(conn,groupnames)
	dlg.setWidget(removegroup,True,qApp.translate("CreateGroupWdg","Group information"))
	glob_settings.widgetGeometry('skolesys-ui/RemoveGroup',dlg)
	dlg.exec_loop()
	glob_settings.setWidgetGeometry('skolesys-ui/RemoveGroup',dlg)

def execAddRemoveUserGroups(conn,uids):
	dlg = WidgetDialog()
	dlg.setCaption(qApp.translate("AddRemoveUserGroupsWdg","Alter Group Memberships"))
	wdg = AddRemoveUserGroupsWdg(conn,uids)
	dlg.setWidget(wdg,True,qApp.translate("AddRemoveUserGroupsWdg","Alter the group membership of the following user(s)"))
	glob_settings.widgetGeometry('skolesys-ui/AddRemoveUserGroups',dlg)
	dlg.exec_loop()
	glob_settings.setWidgetGeometry('skolesys-ui/AddRemoveUserGroups',dlg)

def execAddRemoveGroupUsers(conn,groupnames):
	dlg = WidgetDialog()
	dlg.setCaption(qApp.translate("AddRemoveGroupUsersWdg","Alter Group Members"))
	wdg = AddRemoveGroupUsersWdg(conn,groupnames)
	dlg.setWidget(wdg,True,qApp.translate("AddRemoveGroupUsersWdg","Alter the members of the following group(s)"))
	glob_settings.widgetGeometry('skolesys-ui/AddRemoveGroupUsers',dlg)
	dlg.exec_loop()
	glob_settings.setWidgetGeometry('skolesys-ui/AddRemoveGroupUsers',dlg)
