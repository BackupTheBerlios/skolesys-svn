from qt import *
from widgetdialog import WidgetDialog
from usermanagerwdg import UserManagerWdg
from createuserwdg import CreateUserWdg

def execUserManager(conn):
	dlg = WidgetDialog(buttons=3)
	dlg.btnCustom1.setText(qApp.translate("UserManagerWdg","Create user..."))
	dlg.btnCustom2.setText(qApp.translate("UserManagerWdg","Remove user..."))
	userman = UserManagerWdg(conn,None,"UserManagerWdg")
	dlg.setWidget(userman,True,qApp.translate("UserManagerWdg","Users"))
	QObject.connect(dlg.btnCustom1,SIGNAL("clicked()"),userman.createUser)
	QObject.connect(dlg.btnCustom2,SIGNAL("clicked()"),userman.removeUser)
	dlg.exec_loop()

def execCreateUser(conn):
	dlg = WidgetDialog()
	createuser = CreateUserWdg(conn)
	dlg.setWidget(createuser,True,qApp.translate("CreateUserWdg","User information"))
	dlg.exec_loop()
