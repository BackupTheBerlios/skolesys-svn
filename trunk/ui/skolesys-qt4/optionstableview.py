from PyQt4 import QtCore, QtGui
import pyqtui4.pluggablemodelhelper as pmh
import pyqtui4.pluggableitemdelegate as pid
import sys
import connectionmanager as cm

class OptionsTableView(QtGui.QTreeView):
	def __init__(self,parent):
		QtGui.QTreeView.__init__(self,parent)
		model = QtGui.QStandardItemModel()
		#self.verticalHeader().hide()
		self.modelhelper = pmh.PluggableModelHelper(model)
		self.modelhelper.setView(self)
		self.modelhelper.setColumnReadOnly(0)
		
		#self.connect(model,QtCore.SIGNAL("rowsInserted(const QModelIndex&,int,int)"),self.slotRowInserted)
		self.connect(self.itemDelegate(),QtCore.SIGNAL("dataChanged"),self.slotDataChanged)
	
	def setContext(self,servicename,groupname):
		proxy = cm.get_connection().get_proxy_handle()
		options = proxy.list_groupservice_options_available(servicename,groupname)
		self.groupname = groupname
		self.servicename = servicename
		self.setOptions(options)
	
	def setOptions(self,options):
		self.model().clear()
		model = self.model()
		model.insertColumns(0,2)
		row = 0
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
			
	def slotDataChanged(self,idx):
		proxy = cm.get_connection().get_proxy_handle()
		if idx.data(pid.IS_CellId) != QtCore.QVariant.Invalid:
			option_name = str(idx.data(pid.IS_CellId).toString())
			value = idx.data(pid.IS_ShadowValue)
			if value.type() == QtCore.QVariant.Int:
				value,ok = value.toInt()
				proxy.set_groupservice_option_value(self.servicename,self.groupname,option_name,value)
			
			elif value.type() == QtCore.QVariant.String:
				value = str(value.toString().toUtf8()).strip()
				if value == '':
					proxy.unset_groupservice_option(self.servicename,self.groupname,option_name)
				else:
					proxy.set_groupservice_option_value(self.servicename,self.groupname,option_name,value)

			elif value.type() == QtCore.QVariant.Bool:
				value = str(value.toBool())
				proxy.set_groupservice_option_value(self.servicename,self.groupname,option_name,value)


if __name__ == '__main__':

	from skolesys.soap.client import SkoleSYS_Client
	cli = SkoleSYS_Client('https://mainserver.skolesys.local',8443)
	cli.bind('bdnprrfe')	
	options = cli.list_groupservice_options_available('servgrp1','webservice')
	
	
	app = QtGui.QApplication(sys.argv)
	ui = OptionsTableView(None)
	ui.setOptions(options)
	ui.cli = cli
	model = ui.model()

	ui.show()
	sys.exit(app.exec_())
