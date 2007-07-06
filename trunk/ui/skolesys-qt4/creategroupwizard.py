# This file is part of the SkoleSYS libraries
# Copyright (C) 2007 Jakob Simon-Gaarde <info at skolesys.dk>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License version 2 as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public License
# along with this library; see the file COPYING.LIB.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301, USA.

from PyQt4 import QtCore, QtGui
import ui_creategroupwizard as baseui
import groupmodel as gmod
import connectionmanager as cm
import pickle
import skolesys.definitions.groupdef as groupdef
import skolesys.definitions.userdef as userdef
import skolesys.tools.charmapping as charmapping
import pyqtui4.pluggablemodelhelper as pmh
import accesstools
import ss_mainwindow as mainwin

class CreateGroupWizard(QtGui.QDialog, baseui.Ui_CreateGroupWizard):
	
	def __init__(self,parent):
		QtGui.QWidget.__init__(self,parent)

		self.groupview = None
		
		self.name_page_ok = False
		self.group_name_ok = None

		self.setupUi(self)
		self.setupNamePage()
		
		self.connect(self.btn_cancel,QtCore.SIGNAL("clicked()"),self.reject)
		self.connect(self.btn_back,QtCore.SIGNAL("clicked()"),self.back)
		self.connect(self.btn_next,QtCore.SIGNAL("clicked()"),self.next)
		self.connect(self.btn_finish,QtCore.SIGNAL("clicked()"),self.finish)

	def setupNamePage(self):
		self.connect(self.led_groupname,QtCore.SIGNAL("textChanged(const QString&)"),self.checkName)
		self.connect(self.cmb_grouptype,QtCore.SIGNAL("activated(int)"),self.updateNamePage)
		
		self.tr("primary")
		self.tr("system")
		self.tr("service")
		grouptypeids = groupdef.list_grouptypes_by_id()
		#self.cmb_usertype.addItem(self.tr("Select user type..."),QtCore.QVariant(-1))
		
		for i in grouptypeids:
			self.cmb_grouptype.addItem(
				self.tr(groupdef.grouptype_as_text(i)),
				QtCore.QVariant(i))
		self.cmb_grouptype.setCurrentIndex(self.cmb_grouptype.findData(QtCore.QVariant(groupdef.grouptype_as_id('service'))))
		


	def checkName(self):
		displayed_name = str(self.led_groupname.text().toUtf8())
		self.groupname = charmapping.system_nicefy_string(displayed_name)
		self.updateNamePage()

		
	def updateNamePage(self):
		self.setWindowTitle(self.tr("New Group") + " - [ " + self.led_groupname.text() + " ]")
		grouptype_cmb_idx = self.cmb_grouptype.currentIndex()
		# Maybe enable the first school year box
		#grouptype_id,ok = self.cmb_grouptype.itemData(grouptype_cmb_idx).toInt()
		#if grouptype_id == userdef.usertype_as_id('student'):
			#self.sbx_first_school_year.setEnabled(True)
		#else:
			#self.sbx_first_school_year.setEnabled(False)
		if self.groupname!='' and \
			grouptype_cmb_idx!=-1:
			self.name_page_ok = True
		else:
			self.name_page_ok = False
		self.updateWizardButtons()
		
	
	def updateWizardButtons(self):
		
		self.btn_back.setEnabled(True)
		self.btn_next.setEnabled(False)
		self.btn_finish.setEnabled(False)

		if self.name_page_ok:
			self.btn_finish.setEnabled(True)
		else:
			self.btn_finish.setEnabled(False)
		
		if self.swd_userinfo.currentIndex() == 0:
			self.btn_back.setEnabled(False)
			if self.name_page_ok:
				self.btn_next.setEnabled(True)


	def back(self):
		curidx = self.swd_userinfo.currentIndex()
		if curidx-1 < 0:
			return;
		self.swd_userinfo.setCurrentIndex(curidx-1)
		if curidx-1 == 0:
			self.btn_back.setEnabled(False)
		self.updateWizardButtons()

	def next(self):
		curidx = self.swd_userinfo.currentIndex()
		if curidx+1 >= self.swd_userinfo.count():
			return;
		self.swd_userinfo.setCurrentIndex(curidx+1)
		self.btn_back.setEnabled(True)
		self.updateWizardButtons()
	
	def finish(self):
		description = str(self.ted_description.toPlainText().toUtf8())
		proxy = cm.get_proxy_handle()
		displayed_name = str(self.led_groupname.text().toUtf8())
		grouptype_id,ok = self.cmb_grouptype.itemData(self.cmb_grouptype.currentIndex()).toInt()
		org_groupname = self.groupname
		groupname = self.groupname
		num = 1
		while proxy.group_exists(groupname):
			groupname = '%s%d' % (org_groupname,num)
			print groupname
			num += 1
			
		
		res = proxy.creategroup(groupname,displayed_name,grouptype_id,description)
		if res>=0:
			import ss_mainwindow as mainwin
			mainwin.get_mainwindow().emitGroupCreated(groupname)
		
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
		proxy = cm.get_proxy_handle()
		for grp in groups:
			self.groupmodel._removeGroup(grp['gid'])
		
		self.trv_groups.resizeColumnsToContent()		
		# Update the group add selector
		self.updateGroupAddExcludeFilter()

	def hook_dropOnGroupView(self,obj,de):
		dragged_groups = pickle.loads(de.mimeData().data('application/x-skolesysgroups-pyobj'))
		proxy = cm.get_proxy_handle()
		for grp in dragged_groups:
			self.groupmodel._addGroup(grp['gid'],grp['groupname'],grp['displayed_name'],grp['grouptype_id'])
		
		self.trv_groups.resizeColumnsToContent()
		# Update the group add selector
		self.updateGroupAddExcludeFilter()



if __name__ == '__main__':
	import sys
	app = QtGui.QApplication(sys.argv)
	ui = CreateGroupWizard(None)
	
	ui.show()
	sys.exit(app.exec_())
