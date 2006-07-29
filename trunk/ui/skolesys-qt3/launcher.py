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
	dlg.exec_loop()

def execCreateUser(conn):
	dlg = WidgetDialog()
	dlg.setCaption(qApp.translate("CreateUserWdg","Create User"))
	createuser = CreateUserWdg(conn)
	dlg.setWidget(createuser,True,qApp.translate("CreateUserWdg","User information"))
	dlg.exec_loop()

def execRemoveUser(conn,uids):
	dlg = WidgetDialog()
	dlg.setCaption(qApp.translate("RemoveUserWdg","Remove User(s)"))
	removeuser = RemoveUserWdg(conn,uids)
	dlg.setWidget(removeuser,True,qApp.translate("CreateUserWdg","User information"))
	dlg.exec_loop()

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
	dlg.exec_loop()

def execCreateGroup(conn):
	dlg = WidgetDialog()
	dlg.setCaption(qApp.translate("CreateGroupWdg","Create Group"))
	creategroup = CreateGroupWdg(conn)
	dlg.setWidget(creategroup,True,qApp.translate("CreateUserWdg","Group information"))
	dlg.exec_loop()

def execRemoveGroup(conn,groupnames):
	dlg = WidgetDialog()
	dlg.setCaption(qApp.translate("RemoveGroupWdg","Remove Group(s)"))
	removegroup = RemoveGroupWdg(conn,groupnames)
	dlg.setWidget(removegroup,True,qApp.translate("CreateGroupWdg","Group information"))
	dlg.exec_loop()

def execAddRemoveUserGroups(conn,uids):
	dlg = WidgetDialog()
	dlg.setCaption(qApp.translate("AddRemoveUserGroupsWdg","Alter Group Memberships"))
	wdg = AddRemoveUserGroupsWdg(conn,uids)
	dlg.setWidget(wdg,True,qApp.translate("AddRemoveUserGroupsWdg","Alter the group membership of the following user(s)"))
	dlg.exec_loop()

def execAddRemoveGroupUsers(conn,groupnames):
	dlg = WidgetDialog()
	dlg.setCaption(qApp.translate("AddRemoveGroupUsersWdg","Alter Group Members"))
	wdg = AddRemoveGroupUsersWdg(conn,groupnames)
	dlg.setWidget(wdg,True,qApp.translate("AddRemoveGroupUsersWdg","Alter the members of the following group(s)"))
	dlg.exec_loop()
