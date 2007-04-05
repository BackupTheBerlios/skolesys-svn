from PyQt4 import QtCore,QtGui
import pluggableitemdelegate as pid

class ItemDelegatePlugin:
	def createEditor(self,parent,option,index):
		pass
	def setEditorData(self,editor,index):
		pass
	def setModelData(self,editor,model,index):
		pass
	def updateEditorGeometry(self,editor,option,index):
		pass
	def setModelDataFromValue(self,model,index,value):
		pass
	
class ComboBoxItemPlugin(ItemDelegatePlugin):
	
	def __init__(self,items):
		self.items = items
	
	def createEditor(self,parent,option,index):
		editor = QtGui.QComboBox(parent)
		# Add available items
		items = self.items
		if items and items.type() == QtCore.QVariant.StringList:
			editor.addItems(items.toStringList())
		elif items and items.type() == QtCore.QVariant.Map:
			itemmap = items.toMap()
			for k in itemmap.keys():
				editor.addItem(k,itemmap[k])
		return editor

	def setEditorData(self,editor,index):
		comboBox = editor
		items = self.items
		if items and items.type() == QtCore.QVariant.StringList:
			value = index.data(pid.IS_ShadowValue).toString()
			comboBox.setCurrentIndex(comboBox.findText(value))
		elif items and items.type() == QtCore.QVariant.Map:
			value = index.data(pid.IS_ShadowValue)
			comboBox.setCurrentIndex(comboBox.findData(value))
		comboBox.showPopup()

	def setModelData(self,editor,model,index):
		comboBox = editor
		items = self.items
		if items and items.type() == QtCore.QVariant.StringList:
			txt = comboBox.currentText()
			model.setItemData(index, {pid.IS_ShadowValue: QtCore.QVariant(txt),QtCore.Qt.EditRole:QtCore.QVariant(txt)})
		elif items and items.type() == QtCore.QVariant.Map:
			idx = comboBox.currentIndex()
			text = comboBox.currentText()
			item_data = {}
			if idx>-1:
				data = comboBox.itemData(idx)
				item_data[pid.IS_ShadowValue] = data

			item_data[QtCore.Qt.EditRole] = QtCore.QVariant(text)
			model.setItemData(index, item_data)
			
	def setModelDataFromValue(self,model,index,value):
		items = self.items
		if items.type() == QtCore.QVariant.StringList:
			model.setData(index, QtCore.QVariant(value), pid.IS_ShadowValue)
			model.setData(index, QtCore.QVariant(value), QtCore.Qt.EditRole)
		if items.type() == QtCore.QVariant.Map:
			for k,v in items.toMap().items():
				if v==QtCore.QVariant(value):
					model.setData(index, v, pid.IS_ShadowValue)
					model.setData(index, QtCore.QVariant(k), QtCore.Qt.EditRole)


class SpinBoxItemPlugin(ItemDelegatePlugin):
	
	def __init__(self,minval=None,maxval=None):
		self.minimum,self.maximum = minval,maxval
	
	def createEditor(self,parent,option,index):
		editor = QtGui.QSpinBox(parent)
		# Add available items
		minval,maxval = self.minimum,self.maximum
		if not minval == None:
			editor.setMinimum(minval)
		if not maxval == None:
			editor.setMaximum(maxval)
		return editor

	def setEditorData(self,editor,index):
		spinBox = editor
		value,ok = index.data(pid.IS_ShadowValue).toInt()
		if ok:
			spinBox.setValue(value)

	def setModelData(self,editor,model,index):
		spinBox = editor
		value = QtCore.QVariant(spinBox.value())
		model.setItemData(index, {pid.IS_ShadowValue: value, QtCore.Qt.EditRole: QtCore.QVariant(value.toString())} )
		end_value = index.data(pid.IS_ShadowValue)
			
	def setModelDataFromValue(self,model,index,value):
		minval,maxval = self.minimum,self.maximum
		if not minval == None:
			if int(value)<minval:
				value = minval
		if not maxval == None:
			if int(value)>maxval:
				value = maxval
		model.setData(index, QtCore.QVariant(value), pid.IS_ShadowValue)
		model.setData(index, QtCore.QVariant(value), pid.QtCore.Qt.EditRole)
