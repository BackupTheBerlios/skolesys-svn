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
import ui_createuserwizard as baseui
import groupmodel as gmod
import connectionmanager as cm
import pickle
import skolesys.definitions.groupdef as groupdef
import skolesys.definitions.userdef as userdef
import pyqtui4.pluggablemodelhelper as pmh


class CreateUserWizard(QtGui.QDialog, baseui.Ui_CreateUserWizard):
	
	def __init__(self,parent):
		QtGui.QWidget.__init__(self,parent)
		self.groupview = None
		
		self.name_page_ok = False
		self.group_page_ok = False
		self.login_page_ok = False
		self.login_valid = False

		self.setupUi(self)
		self.setupNamePage()
		self.setupGroupPage()
		self.setupLoginPage()
		
		self.connect(self.btn_cancel,QtCore.SIGNAL("clicked()"),self.reject)
		self.connect(self.btn_back,QtCore.SIGNAL("clicked()"),self.back)
		self.connect(self.btn_next,QtCore.SIGNAL("clicked()"),self.next)
		self.connect(self.btn_finish,QtCore.SIGNAL("clicked()"),self.finish)
		

	def setupNamePage(self):
		self.connect(self.led_given_name,QtCore.SIGNAL("textChanged(const QString&)"),self.updateNamePage)
		self.connect(self.led_family_name,QtCore.SIGNAL("textChanged(const QString&)"),self.updateNamePage)
		self.connect(self.cmb_usertype,QtCore.SIGNAL("activated(int)"),self.updateNamePage)
		
		self.tr("teacher")
		self.tr("student")
		self.tr("parent")
		self.tr("other")
		usertypeids = userdef.list_usertypes_by_id()
		#self.cmb_usertype.addItem(self.tr("Select user type..."),QtCore.QVariant(-1))
		
		for i in usertypeids:
			self.cmb_usertype.addItem(
				self.tr(userdef.usertype_as_text(i)),
				QtCore.QVariant(i))
		self.cmb_usertype.setCurrentIndex(-1)
		
		self.sbx_first_school_year.setValue(QtCore.QDate.currentDate().year())

		
	def updateNamePage(self):
		self.setWindowTitle(self.tr("New User") + " - [ " + self.led_given_name.text() + " " + self.led_family_name.text() + " ]")
		usertype_cmb_idx = self.cmb_usertype.currentIndex()
		# Maybe enable the first school year box
		usertype_id,ok = self.cmb_usertype.itemData(usertype_cmb_idx).toInt()
		if usertype_id == userdef.usertype_as_id('student'):
			self.sbx_first_school_year.setEnabled(True)
		else:
			self.sbx_first_school_year.setEnabled(False)
		if not self.led_given_name.text().isEmpty() and \
			not self.led_family_name.text().isEmpty() and \
			usertype_cmb_idx!=-1:
			self.name_page_ok = True
		else:
			self.name_page_ok = False
		self.updateWizardButtons()
		

	def setupGroupPage(self):
		proxy = cm.get_connection().get_proxy_handle()
		# Primary group combo
		
		self.cmb_primary_group.clear()
		for groupname,details in proxy.list_groups(groupdef.grouptype_as_id('primary')).items():
			self.cmb_primary_group.addItem(
				QtCore.QString().fromUtf8(details['displayedName']),
				QtCore.QVariant(details['gidNumber']))
		self.cmb_primary_group.setCurrentIndex(-1)
		self.connect(self.cmb_primary_group,QtCore.SIGNAL("activated(int)"),self.updateGroupPage)

		# Secondary groups
		self.groupmodel = gmod.GroupModel(cm.get_connection(),self.trv_groups)
		self.modelhelper = pmh.PluggableModelHelper(self.groupmodel)
		self.modelhelper.setView(self.trv_groups)
		for colidx in xrange(self.groupmodel.columnCount()):
			self.modelhelper.setColumnReadOnly(colidx)
		
		self.trv_groups.setColumnHidden(self.groupmodel.columninfo['gid']['columnindex'],True)
		self.trv_groups.setColumnHidden(self.groupmodel.columninfo['groupname']['columnindex'],True)

		# group list connections
		self.trv_groups.connectEvent("dropEvent",self.hook_dropOnGroupView)
		self.trv_groups.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.connect(self.trv_groups,QtCore.SIGNAL("customContextMenuRequested(const QPoint&)"),self.groupsContextMenu)
		self.connect(self.btn_add_groups,QtCore.SIGNAL("clicked()"),self.viewGroupsAvailable)
		
		self.groupmodel.setAcceptedMimeTypes(['application/x-skolesysgroups-pyobj'])

	def updateGroupPage(self):
		if self.cmb_usertype.currentIndex()!=-1:
			self.group_page_ok = True
		else:
			self.group_page_ok = False
		self.updateWizardButtons()
		

	def setupLoginPage(self):
		self.connect(self.led_login,QtCore.SIGNAL("textChanged(const QString&)"),self.checkLogin)
		self.connect(self.led_passwd,QtCore.SIGNAL("textChanged(const QString&)"),self.updateLoginPage)
		self.connect(self.led_passwd_confirm,QtCore.SIGNAL("textChanged(const QString&)"),self.updateLoginPage)
		self.led_login.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[-\._A-Za-z0-9]+$"),self.led_login))
		self.pal_org = QtGui.QPalette(self.led_login.palette())
	
	def checkLogin(self):
		proxy = cm.get_connection().get_proxy_handle()
		login=str(self.led_login.text().toUtf8())
		self.led_login.setText(login.lower())
		pal = QtGui.QPalette(self.pal_org)
		if proxy.user_exists(login):
			pal.setColor(QtGui.QPalette.Text,QtCore.Qt.red)
			self.login_valid = False
		elif len(login)>=2:
			self.login_valid = True

		self.led_login.setPalette(pal)
		self.updateLoginPage()
	
	def updateLoginPage(self):
		self.login_page_ok = True
		if not self.login_valid:
			self.login_page_ok = False
		
		elif len(str(self.led_passwd.text().toUtf8()))<3 or \
			str(self.led_passwd.text().toUtf8())!=str(self.led_passwd_confirm.text().toUtf8()):
			self.login_page_ok = False
			
		self.updateWizardButtons()
		
	
	def updateWizardButtons(self):
		
		self.btn_back.setEnabled(True)
		self.btn_next.setEnabled(False)
		self.btn_finish.setEnabled(False)

		if self.name_page_ok and self.group_page_ok and self.login_page_ok:
			self.btn_finish.setEnabled(True)
		else:
			self.btn_finish.setEnabled(False)
		
		if self.swd_userinfo.currentIndex() == 0:
			self.btn_back.setEnabled(False)
			if self.name_page_ok:
				self.btn_next.setEnabled(True)
			
		if self.swd_userinfo.currentIndex() == 1:
			if self.group_page_ok:
				self.btn_next.setEnabled(True)

		if self.swd_userinfo.currentIndex() == 2:
			self.btn_next.setEnabled(False)

	def back(self):
		curidx = self.swd_userinfo.currentIndex()
		if curidx-1 < 0:
			return;
		self.swd_userinfo.setCurrentIndex(curidx-1)
		if curidx-1 == 0:
			self.btn_back.setEnabled(False)
		if self.groupview:
			self.groupview.hide()
		self.updateWizardButtons()

	def next(self):
		curidx = self.swd_userinfo.currentIndex()
		if curidx+1 >= self.swd_userinfo.count():
			return;
		self.swd_userinfo.setCurrentIndex(curidx+1)
		self.btn_back.setEnabled(True)
		if self.groupview:
			self.groupview.hide()
		self.updateWizardButtons()
	
	def finish(self):
		uid = str(self.led_login.text().toUtf8())
		givenname = str(self.led_given_name.text().toUtf8())
		familyname = str(self.led_family_name.text().toUtf8())
		usertype_id,ok = self.cmb_usertype.itemData(self.cmb_usertype.currentIndex()).toInt()
		firstyear = None
		if usertype_id == userdef.usertype_as_id('student'):
			firstyear = self.sbx_first_school_year.value()
		primarygroup,ok = self.cmb_primary_group.itemData(self.cmb_primary_group.currentIndex()).toInt()
		passwd = str(self.led_passwd.text().toUtf8())
		proxy = cm.get_connection().get_proxy_handle()
		res = proxy.createuser(uid,givenname,familyname,passwd,usertype_id,primarygroup,firstyear)
		if res>=0:
			import ss_mainwindow as mainwin
			mainwin.get_mainwindow().emitUserCreated(uid)
			
		for groupname in self.groupmodel.groupNames():
			proxy.groupadd(uid,groupname)
		
		self.accept()

	def updateGroupAddExcludeFilter(self):
		# Setup excludefilter
		self.add_group_wdg.groupmodel.exclude_gid_numbers = []
		for gid_number in self.groupmodel.groups.keys():
			self.add_group_wdg.groupmodel.exclude_gid_numbers += [gid_number]
			
		self.add_group_wdg.groupmodel.exclude_grouptype_ids=[groupdef.grouptype_as_id('primary')]
		self.add_group_wdg.updateGroupView()
	
	def viewGroupsAvailable(self):
		import groupviewwdg as gvw
		if not self.groupview:
			self.groupview = QtGui.QDialog(self)
			self.groupview.setWindowTitle(self.tr("Available groups"))
			
			self.vboxlayout = QtGui.QVBoxLayout(self.groupview)
			self.vboxlayout.setMargin(0)
			self.vboxlayout.setSpacing(6)
			self.vboxlayout.setObjectName("vboxlayout")
			
			self.add_group_wdg = gvw.GroupViewWdg(self.groupview)
			self.vboxlayout.addWidget(self.add_group_wdg)
			
			# Remove Primary groups from the group filter
			idx = self.add_group_wdg.cmb_grouptype_filter.findData(QtCore.QVariant(groupdef.grouptype_as_id('primary')))
			self.add_group_wdg.cmb_grouptype_filter.removeItem(idx)
			
		self.updateGroupAddExcludeFilter()
		self.groupview.show()
		wizard_rect = self.frameGeometry()
		wizard_rect2 = self.geometry()
		a=QtCore.QRect(wizard_rect.x()+wizard_rect.width(),wizard_rect.y(),300,wizard_rect2.height())
		self.groupview.setGeometry(a)


	def groupsContextMenu(self,pos):
		menu = QtGui.QMenu(self)
		dropaction = menu.addAction(self.tr('Remove groups'))
		self.connect(dropaction,QtCore.SIGNAL('triggered()'),self.removeGroups)
		menu.exec_(QtGui.QCursor.pos())


	def removeGroups(self):
		mimedata = self.groupmodel.generateMimeData(self.trv_groups.selectedIndexes())
		groups = pickle.loads(mimedata['application/x-skolesysgroups-pyobj'])
		proxy = cm.get_connection().get_proxy_handle()
		for grp in groups:
			self.groupmodel._removeGroup(grp['gid'])
		
		self.trv_groups.resizeColumnsToContent()		
		# Update the group add selector
		self.updateGroupAddExcludeFilter()

	def hook_dropOnGroupView(self,obj,de):
		dragged_groups = pickle.loads(de.mimeData().data('application/x-skolesysgroups-pyobj'))
		proxy = cm.get_connection().get_proxy_handle()
		for grp in dragged_groups:
			self.groupmodel._addGroup(grp['gid'],grp['groupname'],grp['displayed_name'],grp['grouptype_id'])
		
		self.trv_groups.resizeColumnsToContent()
		# Update the group add selector
		self.updateGroupAddExcludeFilter()



if __name__ == '__main__':
	import sys
	app = QtGui.QApplication(sys.argv)
	ui = CreateUserWizard(None)
	
	ui.show()
	sys.exit(app.exec_())
