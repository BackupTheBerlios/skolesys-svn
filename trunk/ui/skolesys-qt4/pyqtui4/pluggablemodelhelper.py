import sys
from PyQt4 import QtCore, QtGui
import itemdelegateplugin as idp
import pluggableitemdelegate as pid

class PluggableModelHelper:
	
	def __init__(self,model):
		self.regmap = {}
		self.itemview = None
		self.model = model
		self.delegate = pid.PluggableItemDelegate(self)
		
	def setView(self,itemview):
		self.itemview = itemview
		itemview.setModel(self.model)
		itemview.setItemDelegate(self.delegate)
	
	def registerSpinBox(self,ctrlid,minimum=False,maximum=False):
		self.regmap[ctrlid] = idp.SpinBoxItemPlugin(minimum,maximum)
		
	def registerComboBox(self,ctrlid,comboitems):
		if type(comboitems) == dict:
			newdict = {}
			for k,v in comboitems.items():
				newdict[QtCore.QString.fromUtf8(k)] = QtCore.QVariant(v)
			self.regmap[ctrlid] = idp.ComboBoxItemPlugin(QtCore.QVariant(newdict))
		elif type(comboitems) == list:
			newlist = []
			for i in comboitems:
				newlist += [QtCore.QString.fromUtf8(i)]
			self.regmap[ctrlid] = idp.ComboBoxItemPlugin(QtCore.QVariant(newlist))
	
	def registerStandardItem(self,ctrlid):
		self.regmap[ctrlid] = None

	def setupItem(self,index,ctrlid,value=None,cellid=None):
		if not self.regmap.has_key(ctrlid):
			return False
		
		self.model.setData(index,QtCore.QVariant(ctrlid),pid.IS_ControlSetup)
		
		if type(value) == str:
			value = QtCore.QString.fromUtf8(value)
		
		ctrl = self.regmap[ctrlid]
		if not value == None:
			if ctrl:
				ctrl.setModelDataFromValue(self.model,index,value)
			else:
				self.model.setData(index,QtCore.QVariant(value),QtCore.Qt.EditRole)
				
		if cellid:
			self.model.setData(index, QtCore.QVariant(cellid), pid.IS_CellId)
				
		return True
		
	def setColumnReadOnly(self,columnindex):
		self.delegate.readonly_columns[columnindex] = 1
	
	def setRowReadOnly(self,rowindex):
		self.delegate.readonly_row[rowindex] = 1
