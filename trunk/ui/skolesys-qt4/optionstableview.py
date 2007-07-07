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
import pyqtui4.pluggablemodelhelper as pmh
import pyqtui4.pluggableitemdelegate as pid
import sys
import connectionmanager as cm

class OptionsTableView(QtGui.QTreeView):
	def __init__(self,parent):
		self.change_info = {}
		self.option_info = {}
		QtGui.QTreeView.__init__(self,parent)
		model = QtGui.QStandardItemModel()
		#self.verticalHeader().hide()
		self.modelhelper = pmh.PluggableModelHelper(model)
		self.modelhelper.setView(self)
		self.modelhelper.setColumnReadOnly(0)
		
		#self.connect(model,QtCore.SIGNAL("rowsInserted(const QModelIndex&,int,int)"),self.slotRowInserted)
		self.connect(self.itemDelegate(),QtCore.SIGNAL("dataChanged"),self.slotDataChanged)
	
	def setContext(self,servicename,groupname):
		proxy = cm.get_proxy_handle()
		options = proxy.list_groupservice_options_available(servicename,groupname)
		self.option_info = proxy.get_groupservice_option_values(groupname,servicename)
		self.groupname = groupname
		self.servicename = servicename
		self.setOptions(options)
	
	def setOptions(self,options):
		self.model().clear()
		model = self.model()
		model.insertColumns(0,2)
		row = 0
		self.change_info = {}
		for opt,details in options.items():
			if details['type']==int:
				if details.has_key('enum'):
					self.modelhelper.registerComboBox(opt,details['enum'])
		
				else:
					value,minval,maxval = (None,None,None)
					if details.has_key('range'):
						minval,maxval = details['range']
					
					self.modelhelper.registerSpinBox(opt,minval,maxval)
					
				self.model().insertRow(model.rowCount())
				#self.model().setRowCount(row+1)
				idx = model.index(row,1,QtCore.QModelIndex())
				if details.has_key('value'):
					value = details['value']
				elif details.has_key('default') and type(details['default'])==int:
					value = details['default']
					
				self.modelhelper.setupItem(idx,opt,value,opt)
				idx = model.index(row,0,QtCore.QModelIndex())
				model.setData(idx, QtCore.QVariant(opt), QtCore.Qt.EditRole)
				row += 1
			
			elif details['type']==str:
				if details.has_key('choices'):
					self.modelhelper.registerComboBox(opt,details['choices'])
				else:
					self.modelhelper.registerStandardItem(opt)
		
				value = None
				self.model().insertRow(model.rowCount())
				#self.model().setRowCount(row+1)
				idx = model.index(row,1,QtCore.QModelIndex())
				if details.has_key('value'):
					value = details['value']
				elif details.has_key('default'):
					value = str(details['default'])
					
				self.modelhelper.setupItem(idx,opt,value,opt)
				idx = model.index(row,0,QtCore.QModelIndex())
				model.setData(idx, QtCore.QVariant(opt), QtCore.Qt.EditRole)
				row += 1
		
			elif details['type']==bool:
				self.modelhelper.registerComboBox(opt,{'True':True,'False':False})
				
				value = None
				self.model().insertRow(model.rowCount())
				#self.model().setRowCount(row+1)
				idx = model.index(row,1,QtCore.QModelIndex())
				if details.has_key('value'):
					value = details['value']
				if value==None and details.has_key('default') and type(details['default'])==bool:
					value = details['default']
					
				self.modelhelper.setupItem(idx,opt,value,opt)
				idx = model.index(row,0,QtCore.QModelIndex())
				model.setData(idx, QtCore.QVariant(opt), QtCore.Qt.EditRole)
				row += 1
		for colidx in xrange(model.columnCount()):
			self.resizeColumnToContents(colidx)

		

	def slotRowInserted(self,index,start,end):
		model = self.model()
		for ridx in xrange(model.rowCount()):
			for cidx in xrange(model.columnCount()):
				idx = model.index(ridx,cidx,QtCore.QModelIndex())
				color = QtGui.QColor(240,240,180)
				if ridx % 2:
					color = QtGui.QColor(255,255,255)

				model.setData(idx,QtCore.QVariant(QtGui.QBrush(color)),QtCore.Qt.BackgroundColorRole)
			self.setRowHeight(ridx,20)
			
	def isDirty(self):
		for attr,val in self.change_info.items():
			if self.option_info.has_key(attr) and self.option_info[attr]==val:
				self.change_info.pop(attr)
		if len(self.change_info.keys())==0:
			return False
		return True
	
	def applyChanges(self):
		proxy = cm.get_proxy_handle()
		for option_name,value in self.change_info.items():
			if type(value) == str and value == '':
				proxy.unset_groupservice_option(self.servicename,self.groupname,option_name)
			else:
				proxy.set_groupservice_option_value(self.servicename,self.groupname,option_name,value)
				self.option_info[option_name] = value
		if len(self.change_info.keys()):
			proxy.restart_groupservice(self.groupname,self.servicename)
		self.change_info = {}
	
	def slotDataChanged(self,idx):
		if idx.data(pid.IS_CellId) != QtCore.QVariant.Invalid:
			option_name = str(idx.data(pid.IS_CellId).toString())
			value = idx.data(pid.IS_ShadowValue)
			
			if value.type() == QtCore.QVariant.Int:
				value,ok = value.toInt()
				#proxy.set_groupservice_option_value(self.servicename,self.groupname,option_name,value)
				self.change_info[option_name] = value
			
			elif value.type() == QtCore.QVariant.String:
				value = str(value.toString().toUtf8()).strip()
				if not self.option_info.has_key(option_name) and value == '':
					self.change_info.pop(option_name)
					#proxy.unset_groupservice_option(self.servicename,self.groupname,option_name)
				else:
					#proxy.set_groupservice_option_value(self.servicename,self.groupname,option_name,value)
					self.change_info[option_name] = value

			elif value.type() == QtCore.QVariant.Bool:
				value = str(value.toBool())
				#proxy.set_groupservice_option_value(self.servicename,self.groupname,option_name,value)
				self.change_info[option_name] = value


if __name__ == '__main__':

	from skolesys.soap.client import SkoleSYS_Client
	cli = SkoleSYS_Client('https://127.0.0.1',8443)
	options = cli.list_groupservice_option_available('servgrp1','webservice')
	print options
	
	app = QtGui.QApplication(sys.argv)
	ui = OptionsTableView(None)
	ui.setOptions(options)
	ui.cli = cli
	model = ui.model()

	ui.show()
	sys.exit(app.exec_())
