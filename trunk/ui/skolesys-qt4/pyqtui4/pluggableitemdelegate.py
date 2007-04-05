from PyQt4 import QtCore, QtGui

IS_ControlSetup = 1000	# String describing the control type: LineEdit, ComboBox, SpinBox ...

IS_ShadowValue = 1001	# Used when the rendered data of a cell is merely a textual 
                   	# representation of the real value
IS_CellId = 1002

class PluggableItemDelegate(QtGui.QItemDelegate):
	def __init__(self,wm_mapper):
		QtGui.QItemDelegate.__init__(self,wm_mapper.model)
		self.wm_mapper = wm_mapper
		self.readonly_columns = {}
		self.readonly_rows = {}
	
	def createEditor(self,parent,option,index):
		# Reset all state variables
		if self.readonly_rows.has_key(index.row()):
			return None
		if self.readonly_columns.has_key(index.column()):
			return None
		
		ctrl,self.ctrl,self.start_value,self.end_value = None,None,None,None
		
		# Inticipate using the standard QItemDelegate
		self.start_value = index.data(QtCore.Qt.EditRole)
		
		# See if the model-index is stamped with a registered editor
		print str(index.data(IS_ControlSetup).toString())
		if self.wm_mapper.regmap.has_key(str(index.data(IS_ControlSetup).toString())):
			ctrl = self.wm_mapper.regmap[str(index.data(IS_ControlSetup).toString())]
		
		if ctrl:
			# Using a reg
			editor = ctrl.createEditor(parent,option,index)
			if editor:
				self.ctrl = ctrl
				self.start_value = index.data(IS_ShadowValue)
				editor.installEventFilter(self)
				return editor
				
		return QtGui.QItemDelegate.createEditor(self,parent,option,index)

	def setEditorData(self,editor,index):
		if self.ctrl == None:
			QtGui.QItemDelegate.setEditorData(self,editor,index)
			return
				
		else:
			self.ctrl.setEditorData(editor,index)
			
	def setModelData(self,editor,model,index):
		end_value = None
		if self.ctrl == None:
			QtGui.QItemDelegate.setModelData(self,editor,model,index)
			model.setData(index, index.data(QtCore.Qt.EditRole), IS_ShadowValue )
			end_value = index.data(QtCore.Qt.EditRole)
			
		else:
			self.ctrl.setModelData(editor,model,index)
			end_value = index.data(IS_ShadowValue)
		
		print index.data(IS_ShadowValue).toString().toUtf8(), " (",QtCore.QVariant.typeToName(index.data(IS_ShadowValue).type()),")"
		if self.start_value != end_value:
			self.emit(QtCore.SIGNAL("dataChanged"),index)
			print "Dirty!"
		
	
	def updateEditorGeometry(self,editor,option,index):
		if self.ctrl == False:
			QtGui.QItemDelegate.updateEditorGeometry(self,editor,option,index)
			return
		
		editor.setGeometry(option.rect)
