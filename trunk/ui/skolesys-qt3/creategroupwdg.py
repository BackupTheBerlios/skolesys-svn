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
from creategroupwdgbase import CreateGroupWdgBase
import skolesys.definitions.groupdef as groupdef

class CreateGroupWdg(CreateGroupWdgBase):
	def __init__(self,conn,parent = None,name = None,fl = 0):
		CreateGroupWdgBase.__init__(self,parent,name,fl)
		self.proxy = conn.get_proxy_handle()
		self.setup()
		
	def setup(self):
		# login restriction
		rx = QRegExp('\\w+')
		rx_validator = QRegExpValidator(rx,self)
		self.ed_groupname.setValidator(rx_validator)
		self.connect(self.ed_groupname,SIGNAL("textChanged(const QString&)"),self.check_group)
		
		self.typedict={self.tr('Primary').latin1():groupdef.grouptype_as_id('primary'),\
			self.tr('System').latin1():groupdef.grouptype_as_id('system'),\
			self.tr('Service').latin1():groupdef.grouptype_as_id('service')}
		
		order = [self.tr('Service').latin1(),\
			self.tr('Primary').latin1(),self.tr('System').latin1()]
		for grouptype in order:
			self.cmb_grouptype.insertItem(grouptype)

	def check_group(self):
		groupname=str(self.ed_groupname.text().utf8())
		if self.proxy.group_exists(groupname):
			self.ed_groupname.setPaletteForegroundColor(Qt.red)
		else:
			self.ed_groupname.setPaletteForegroundColor(Qt.black)

	def accept(self):
		groupname=str(self.ed_groupname.text().utf8())
		if self.proxy.group_exists(groupname):
			QMessageBox.information(self,
				self.tr('Create group'),
				self.tr('The group "%1" already exists on the system - choose another.').arg(groupname))
			self.ed_groupname.setFocus()
			self.ed_groupname.selectAll()
			return False
		# user type
		grouptype = self.typedict[self.cmb_grouptype.currentText().latin1()]
		desc = str(self.te_description.text().utf8())[:1020]
		print self.proxy.creategroup(groupname,grouptype,desc)
		return True
