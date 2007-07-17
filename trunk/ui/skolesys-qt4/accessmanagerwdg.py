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
import ui_accessmanagerwdg as ui_amwdg
import usermodel as umod
import skolesys.definitions.userdef as userdef
import connectionmanager as cm
import pickle
import pyqtui4.pluggablemodelhelper as pmh
import ss_mainwindow as mainwin
import servermessages as srvmsg

class AccessManagerWdg(QtGui.QDialog, ui_amwdg.Ui_AccessManagerWdg):
	
	def __init__(self,parent):
		QtGui.QWidget.__init__(self,parent)
		self.current_uid = None
		self.proxy = cm.get_proxy_handle()
		self.setupUi(self)
		self.setupModel()
		self.setupUserView()
		self.setupAccessView()
		self.updateUserView()
		
		self.trv_userlist.connectEvent('currentChanged',self.userChanged)
		self.connect(self.trw_access_idents,QtCore.SIGNAL('itemChanged ( QTreeWidgetItem * , int )'),self.accessChanged)
		self.connect(self.btn_close,QtCore.SIGNAL('clicked()'),self.accept)

	def setupModel(self):
		self.usermodel = umod.UserModel(self.trv_userlist)
		self.umodhelper = pmh.PluggableModelHelper(self.usermodel)
		self.umodhelper.setView(self.trv_userlist)
		for colidx in xrange(self.usermodel.columnCount()):
			self.umodhelper.setColumnReadOnly(colidx)

	def setupUserView(self):
		self.trv_userlist.setColumnHidden(self.usermodel.columninfo['uidnumber']['columnindex'],True)
		self.trv_userlist.setColumnHidden(self.usermodel.columninfo['uid']['columnindex'],True)
		self.trv_userlist.setColumnHidden(self.usermodel.columninfo['usertype']['columnindex'],True)


	def setupAccessView(self):
		self.trw_access_idents.setColumnCount(1)
		self.trw_access_idents.setHeaderLabels([self.tr('Access')])
		proxy = cm.get_proxy_handle()
		access_idents = proxy.list_access_identifiers()
		access_groups = {}
		translator = srvmsg.get_translator()
		for ai in access_idents:
			ai_parts = ai.split('.')
			if not access_groups.has_key(ai_parts[0]):
				access_groups[ai_parts[0]] = {
					'access_idents':[],
					'text': translator.q_tr('access','%s_description' % ai_parts[0])}
			access_groups[ai_parts[0]]['access_idents'] += [{
				'access_ident': ai,
				'text':translator.q_tr('access','%s_infinitive' % ai) }]
		
		for grp,ai_list in access_groups.items():
			grp_item = QtGui.QTreeWidgetItem(self.trw_access_idents,[ai_list['text']])
			grp_item.setData(0,32,QtCore.QVariant(grp))
			self.trw_access_idents.addTopLevelItem(grp_item)
			for access_ident in ai_list['access_idents']:
				ai_item = QtGui.QTreeWidgetItem(grp_item,[access_ident['text']])
				ai_item.setCheckState(0,QtCore.Qt.Unchecked)
				ai_item.setData(0,32,QtCore.QVariant(access_ident['access_ident']))
				grp_item.addChild(ai_item)
			self.trw_access_idents.expandItem(grp_item)
		
		self.trw_access_idents.setEnabled(False)
			
		
	def updateUserView(self):
		self.usermodel.loadUsers()
			
		for colidx in xrange(self.usermodel.columnCount()):
			self.trv_userlist.resizeColumnToContents(colidx)
			
	def userChanged(self,sender,idx):
		self.disconnect(self.trw_access_idents,QtCore.SIGNAL('itemChanged ( QTreeWidgetItem * , int )'),self.accessChanged)
		uidnumber = idx.data(QtCore.Qt.UserRole).toInt()[0]
		uid = self.usermodel.users[uidnumber]['uid']
		self.current_uid = uid
		binded_uid = cm.get_binded_user()
		
		permlist = cm.get_proxy_handle().list_permissions(uid)
		for idx in xrange(self.trw_access_idents.topLevelItemCount()):
			topitem = self.trw_access_idents.topLevelItem(idx)
			access_group = str(topitem.data(0,32).toString())
			for cidx in xrange(topitem.childCount()):
				childitem = topitem.child(cidx)
				if permlist.count(str(childitem.data(0,32).toString())):
					childitem.setCheckState(0,QtCore.Qt.Checked)
				else:
					childitem.setCheckState(0,QtCore.Qt.Unchecked)
				if access_group=='access' and self.current_uid==binded_uid:
					# Prevent user from revoking access.granter and access.soap.bind
					childitem.setFlags(QtCore.Qt.ItemIsUserCheckable)
				else:
					childitem.setFlags(QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsSelectable)
		self.trw_access_idents.setEnabled(True)
		self.connect(self.trw_access_idents,QtCore.SIGNAL('itemChanged ( QTreeWidgetItem * , int )'),self.accessChanged)
	
	def accessChanged(self,item):
		proxy = cm.get_proxy_handle()
		access_ident = str(item.data(0,32).toString())
		if item.checkState(0)==QtCore.Qt.Checked:
			proxy.grant_access(self.current_uid,access_ident)
		else:
			proxy.revoke_access(self.current_uid,access_ident)
		