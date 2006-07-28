from qt import *
from widgetdialog import WidgetDialog

# User manager
from usermanagerwdg import UserManagerWdg
from createuserwdg import CreateUserWdg
from removeuserwdg import RemoveUserWdg

# Group manager
from groupmanagerwdg import GroupManagerWdg
from creategroupwdg import CreateGroupWdg
from removegroupwdg import RemoveGroupWdg

def execUserManager(conn):
	dlg = WidgetDialog(buttons=3)
	dlg.setCaption(qApp.translate("UserManagerWdg","User Manager"))
	dlg.btnCustom1.setText(qApp.translate("UserManagerWdg","Create user..."))
	dlg.btnCustom2.setText(qApp.translate("UserManagerWdg","Remove user..."))
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

def execRemoveUser(conn,uid):
	dlg = WidgetDialog()
	dlg.setCaption(qApp.translate("RemoveUserWdg","Remove User [%1]").arg(uid))
	removeuser = RemoveUserWdg(conn,uid)
	dlg.setWidget(removeuser,True,qApp.translate("CreateUserWdg","User information"))
	dlg.exec_loop()

def execGroupManager(conn):
	dlg = WidgetDialog(buttons=3)
	dlg.setCaption(qApp.translate("GroupManagerWdg","Group Manager"))
	dlg.btnCustom1.setText(qApp.translate("GroupManagerWdg","Create group..."))
	dlg.btnCustom2.setText(qApp.translate("GroupManagerWdg","Remove group..."))
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

def execRemoveGroup(conn,groupname):
	dlg = WidgetDialog()
	dlg.setCaption(qApp.translate("RemoveGroupWdg","Remove Group [%1]").arg(groupname))
	removegroup = RemoveGroupWdg(conn,groupname)
	dlg.setWidget(removegroup,True,qApp.translate("CreateGroupWdg","Group information"))
	dlg.exec_loop()
