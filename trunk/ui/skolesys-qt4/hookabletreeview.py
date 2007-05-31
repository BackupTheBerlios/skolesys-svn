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

from PyQt4 import QtCore,QtGui
import pyqtui4.typecheck as typecheck

class EnhancedTreeView(QtGui.QTreeView):
	"""
	By promote views to this class you can decorate your tree view with
	ad-hoc functions rather than creating a new subclass each time you need 
	custom behaviour in a tree view.
	Example:
	
	def hook_drag_enter(obj,dee):
		if dee.mimeType().hasFormat('text/xml'):
			dee.accept()
			return
		dee.ignore()
	
	# Create a tree view
	v = HookableDragDropTreeView(self)
	
	# decorate with the custom event handler hook_drag_enter()
	v.connectEvent("dragEvent" ,hook_drag_enter)
	"""
	def __init__(self,parent):
		QtGui.QTreeView.__init__(self,parent)
		self.drag_start_pos = None
		self.hooked_functions = {}
		self.header().setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.connect(self.header(),QtCore.SIGNAL("customContextMenuRequested(const QPoint&)"),self.headerContextMenu)

	def headerContextMenu(self,pos):
		model = self.model()
		import pyqtui4.enhancedstandarditemmodel as esm
		if typecheck.check_inheritance(model,[esm.EnhancedStandardItemModel]):
			context = QtGui.QMenu(self)
			actionmap = {}
			for colkey,colinfo in model.columninfo.items():
				action = context.addAction(colinfo['text'])
				actionmap[action] = colkey
				action.setCheckable(True)
				if not self.isColumnHidden(colinfo['columnindex']):
					action.setChecked(True)
				action.column_key = colkey
					
			action = context.exec_(QtGui.QCursor.pos())
			self.toggleHiddenColumn(model.columnIndexByKey(actionmap[action]))

	def toggleHiddenColumn(self,columnindex):
		if self.isColumnHidden(columnindex):
			self.setColumnHidden(columnindex,False)
		else:
			self.setColumnHidden(columnindex,True)
		self.resizeColumnsToContent()

	def resizeColumnsToContent(self):
		for colidx in xrange(self.model().columnCount()):
			self.resizeColumnToContents(colidx)

	def connectEvent(self,eventname,func):
		if not self.hooked_functions.has_key(eventname):
			self.hooked_functions[eventname] = []
		self.hooked_functions[eventname] += [func]
			
	def _callback(self,eventname,eventobj):
		if self.hooked_functions.has_key(eventname):
			for func in self.hooked_functions[eventname]:
				func(self,eventobj)

	def dragEnterEvent(self,dee):
		QtGui.QTreeView.dragEnterEvent(self,dee)
		self._callback("dragEnterEvent",dee)

	def dragMoveEvent(self,dme):
		QtGui.QTreeView.dragMoveEvent(self,dme)
		self._callback("dragMoveEvent",dme)
	
	def dragLeaveEvent(self,dle):
		QtGui.QTreeView.dragLeaveEvent(self,dle)
		self._callback("dragLeaveEvent",dle)


	def dropEvent(self,de):
		self._callback("dropEvent",de)

	def mousePressEvent(self,pe):
		if pe.button() == QtCore.Qt.LeftButton:
			self.drag_start_pos = QtCore.QPoint(pe.pos())
		self._callback("mousePressEvent",pe)
		QtGui.QTreeView.mousePressEvent(self,pe)

	def mouseMoveEvent(self,me):
		if not me.buttons() & QtCore.Qt.LeftButton:
			return
		
		if (me.pos() - self.drag_start_pos).manhattanLength() < QtGui.qApp.startDragDistance():
			return
		
		self._callback("mouseMoveEvent",me)
			
		# hook_startDrag - Example
		#-------------------------
		
		#	def hook_start_drag(obj,me):
		#		drag = QtGui.QDrag(obj)
		#		mimeData = QtCore.QMimeData()
		#
		#		mimeData.setData("text/plain", "rwegergerg")
		#		drag.setMimeData(mimeData)
		#		print drag.mimeData().hasFormat('text/plain')
		#	
		#		drop_action = drag.start(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction)
	
