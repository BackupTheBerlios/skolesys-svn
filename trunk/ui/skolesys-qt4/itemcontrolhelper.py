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

import sys
from PyQt4 import QtCore, QtGui

IS_ControlSetup = 1000	# String describing the control type: LineEdit, ComboBox, SpinBox ...

IS_ShadowValue = 1001	# Used when the rendered data of a cell is merely a textual 
                   	# representation of the real value
IS_CellId = 1002

class EnhancedItemDelegate(QtGui.QItemDelegate):
	def __init__(self,parent):
		QtGui.QItemDelegate.__init__(self,parent)
		
	def createEditor(self,parent,option,index):
		if index.column()==0:
			return None
		self.custom_editor = False
		self.start_value = index.data(QtCore.Qt.EditRole)
		#data = index.data(QtCore.Qt.EditRole)
		self.ctrl_setup = index.data(IS_ControlSetup)
		
		if self.ctrl_setup.type() == QtCore.QVariant.List and len(self.ctrl_setup.toList())>1:
			# Custom handled item
			self.setup_lst = self.ctrl_setup.toList()
			self.ctrl_type = self.setup_lst[0]
			if self.ctrl_type.toString() == 'ComboBox':
				self.custom_editor = True
				editor = QtGui.QComboBox(parent)
				# Add available items
				items = self.setup_lst[1]
				if items and items.type() == QtCore.QVariant.StringList:
					editor.addItems(items.toStringList())
				elif items and items.type() == QtCore.QVariant.Map:
					itemmap = items.toMap()
					for k in itemmap.keys():
						editor.addItem(k,itemmap[k])
				editor.installEventFilter(self)
				self.start_value = index.data(IS_ShadowValue)
				return editor
			
			elif self.ctrl_type.toString() == 'SpinBox':
				self.custom_editor = True
				editor = QtGui.QSpinBox(parent)
				# Add available items
				minval,maxval = (self.setup_lst[1],self.setup_lst[2])
				if minval.type() == QtCore.QVariant.Int:
					editor.setMinimum(minval.toInt()[0])
				if maxval.type() == QtCore.QVariant.Int:
					editor.setMaximum(maxval.toInt()[0])
				self.start_value = index.data(IS_ShadowValue)
				return editor
				
		return QtGui.QItemDelegate.createEditor(self,parent,option,index)

	def setEditorData(self,editor,index):
		if self.custom_editor == False:
			QtGui.QItemDelegate.setEditorData(self,editor,index)
			return
				
		elif self.ctrl_type.toString() == 'ComboBox':
			comboBox = editor
			items = self.setup_lst[1]
			if items and items.type() == QtCore.QVariant.StringList:
				value = index.data(IS_ShadowValue).toString()
				comboBox.setCurrentIndex(comboBox.findText(value))
			elif items and items.type() == QtCore.QVariant.Map:
				value = index.data(IS_ShadowValue)
				comboBox.setCurrentIndex(comboBox.findData(value))
		
		elif self.ctrl_type.toString() == 'SpinBox':
			spinBox = editor
			value,ok = index.data(IS_ShadowValue).toInt()
			if ok:
				spinBox.setValue(value)
		
	def setModelData(self,editor,model,index):
		end_value = None
		if self.custom_editor == False:
			QtGui.QItemDelegate.setModelData(self,editor,model,index)
			model.setData(index, index.data(QtCore.Qt.EditRole), IS_ShadowValue )
			end_value = index.data(QtCore.Qt.EditRole)
			
		elif self.ctrl_type.toString() == 'ComboBox':
			comboBox = editor
			items = self.setup_lst[1]
			if items and items.type() == QtCore.QVariant.StringList:
				txt = comboBox.currentText()
				model.setItemData(index, {IS_ShadowValue: QtCore.QVariant(txt),QtCore.Qt.EditRole:QtCore.QVariant(txt)})
			elif items and items.type() == QtCore.QVariant.Map:
				idx = comboBox.currentIndex()
				text = comboBox.currentText()
				item_data = {}
				if idx>-1:
					data = comboBox.itemData(idx)
					item_data[IS_ShadowValue] = data

				item_data[QtCore.Qt.EditRole] = QtCore.QVariant(text)
				model.setItemData(index, item_data)
			end_value = index.data(IS_ShadowValue)

		elif self.ctrl_type.toString() == 'SpinBox':
			spinBox = editor
			value = QtCore.QVariant(spinBox.value())
			model.setItemData(index, {IS_ShadowValue: value, QtCore.Qt.EditRole: QtCore.QVariant(value.toString())} )
			end_value = index.data(IS_ShadowValue)
		
		print index.data(IS_ShadowValue).toString().toUtf8(), " (",QtCore.QVariant.typeToName(index.data(IS_ShadowValue).type()),")"
		if self.start_value != end_value:
			self.emit(QtCore.SIGNAL("dataChanged"),index)
			print "Dirty!"
		
	
	def updateEditorGeometry(self,editor,option,index):
		if self.custom_editor == False:
			QtGui.QItemDelegate.updateEditorGeometry(self,editor,option,index)
			return
		
		editor.setGeometry(option.rect)


class ItemControlHelper:
	regmap = {}
	
	def __init__(self,itemview):
		itemview.setItemDelegate(EnhancedItemDelegate(itemview))
		self.itemview = itemview
		
	def registerSpinBox(self,ctrlid,minimum=False,maximum=False):
		self.regmap[ctrlid] = QtCore.QVariant([QtCore.QVariant('SpinBox'),QtCore.QVariant(minimum),QtCore.QVariant(maximum)])
		
	def registerComboBox(self,ctrlid,comboitems):
		if type(comboitems) == dict:
			newdict = {}
			for k,v in comboitems.items():
				newdict[QtCore.QString.fromUtf8(k)] = QtCore.QVariant(v)
			self.regmap[ctrlid] = QtCore.QVariant([QtCore.QVariant('ComboBox'),QtCore.QVariant(newdict)])
		elif type(comboitems) == list:
			newlist = []
			for i in comboitems:
				newlist += [QtCore.QString.fromUtf8(i)]
			self.regmap[ctrlid] = QtCore.QVariant([QtCore.QVariant('ComboBox'),QtCore.QVariant(newlist)])
	
	def registerStandardItem(self,ctrlid):
		self.regmap[ctrlid] = None

	def setupItem(self,index,ctrlid,value=None,cellid=None):
		model = self.itemview.model()
		if not self.regmap.has_key(ctrlid):
			return False
		model.setData(index,self.regmap[ctrlid],IS_ControlSetup)
		
		if type(value) == str:
			value = QtCore.QString.fromUtf8(value)
		
		if not value == None:
			setup_lst = self.regmap[ctrlid].toList()
			ctrltype = setup_lst[0].toString()
			if ctrltype=='ComboBox':
				items = setup_lst[1]
				if items.type() == QtCore.QVariant.StringList:
					model.setData(index, QtCore.QVariant(value), IS_ShadowValue)
					model.setData(index, QtCore.QVariant(value), QtCore.Qt.EditRole)
				if items.type() == QtCore.QVariant.Map:
					for k,v in items.toMap().items():
						if v==QtCore.QVariant(value):
							model.setData(index, v, IS_ShadowValue)
							model.setData(index, QtCore.QVariant(k), QtCore.Qt.EditRole)
			elif ctrltype=='SpinBox':
				minval,maxval = (setup_lst[1],setup_lst[2])
				if minval.type() == QtCore.QVariant.Int:
					if int(value)<minval.toInt()[0]:
						value = minval.toInt()[0]
				if maxval.type() == QtCore.QVariant.Int:
					if int(value)>maxval.toInt()[0]:
						value = maxval.toInt()[0]
				model.setData(index, QtCore.QVariant(value), IS_ShadowValue)
				model.setData(index, QtCore.QVariant(value), QtCore.Qt.EditRole)
				
			elif ctrltype=='StandardItem':
				model.setData(index, QtCore.QVariant(value), IS_ShadowValue)
				model.setData(index, QtCore.QVariant(value), QtCore.Qt.EditRole)
				
		if cellid:
			model.setData(index, QtCore.QVariant(cellid), IS_CellId)
				
		return True
