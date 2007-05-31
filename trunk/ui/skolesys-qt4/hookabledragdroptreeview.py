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

class HookableTreeView(QtGui.QTreeView):
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
	v.hook_dragEnterEvent = hook_drag_enter
	"""
	def __init__(self,parent):
		QtGui.QTreeView.__init__(self,parent)
		self.drag_start_pos = None

	def dragEnterEvent(self,dee):
		if dir(self).count('hook_dragEnterEvent'):
			self.hook_dragEnterEvent(self,dee)

	def dragMoveEvent(self,dme):
		if dir(self).count('hook_dragMoveEvent'):
			self.hook_dragMoveEvent(self,dme)
	
	def dragLeaveEvent(self,dle):
		if dir(self).count('hook_dragLeaveEvent'):
			self.hook_dragLeaveEvent(self,dle)


	def dropEvent(self,de):
		if dir(self).count('hook_dropEvent'):
			self.hook_dropEvent(self,de)

	def mousePressEvent(self,pe):
		if pe.button() == QtCore.Qt.LeftButton:
			self.drag_start_pos = QtCore.QPoint(pe.pos())
		QtGui.QTreeView.mousePressEvent(self,pe)

	def mouseMoveEvent(self,me):
		if not me.buttons() & QtCore.Qt.LeftButton:
			return
		
		if (me.pos() - self.drag_start_pos).manhattanLength() < QtGui.qApp.startDragDistance():
			return
		
		if dir(self).count('hook_startDrag'):
			self.hook_startDrag(self,me)
			
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
	
