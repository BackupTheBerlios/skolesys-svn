from PyQt4 import QtCore, QtGui
import ui_tooltabwdg as baseui
import pyqtui4.qt4tools as qt4tools
import pyqtui4.actionrequester as ar


class ToolTabWdg(QtGui.QWidget, baseui.Ui_ToolTabWdg,ar.ActionRequester):
	
	def __init__(self,parent):
		QtGui.QWidget.__init__(self,parent)
		ar.ActionRequester.__init__(self)
		self.setupUi(self)
		self.btn_new_user.setIcon(QtGui.QIcon(qt4tools.svg2pixmap('art/new_user.svg',72,72)))
		self.connect(self.btn_new_user,QtCore.SIGNAL("clicked()"),self.execCreateUserWizard)
		self.connect(self.btn_new_group,QtCore.SIGNAL("clicked()"),self.execCreateGroupWizard)
		self.connect(self.btn_open_fileman,QtCore.SIGNAL("clicked()"),self.openFileManager)

		self.btn_new_group.setIcon(QtGui.QIcon(qt4tools.svg2pixmap('art/new_group.svg',72,72)))
		
		
	def execCreateUserWizard(self):
		import ss_mainwindow as mainwin
		mainwin.get_mainwindow().execCreateUserWizard()

	def execCreateGroupWizard(self):
		import ss_mainwindow as mainwin
		mainwin.get_mainwindow().execCreateGroupWizard()
	
	def openFileManager(self):
		import ss_mainwindow as mainwin
		mainwin.get_mainwindow().openFileManager()
	