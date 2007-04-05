from PyQt4 import QtCore,QtGui

class GroupTreeView(QtGui.QTreeView):
	def __init__(self,parent):
		QtGui.QTreeView.__init__(self,parent)
		self.drag_start_pos = None

	def addGroup(self,gid,groupname,displayed_name,grouptype):
		pass

#	def dragEnterEvent(self,dee):
#		QtGui.QTreeView.dragEnterEvent(self,dee)
#		if dir(self).count('hook_dragEnterEvent'):
#			self.hook_dragEnterEvent(self,dee)
#		dee.ignore()

#	def dragLeaveEvent(self,dle):
#		if dir(self).count('hook_dragLeaveEvent'):
#			self.hook_dragEnterEvent(self,dee)


#	def dropEvent(self,de):
#		print de.mimeData().data('text/plain')
#		print "Dropped items"

	def mousePressEvent(self,pe):
		if pe.button() == QtCore.Qt.LeftButton:
			self.drag_start_pos = QtCore.QPoint(pe.pos())
		QtGui.QTreeView.mousePressEvent(self,pe)

	def mouseMoveEvent(self,me):
		if not me.buttons() & QtCore.Qt.LeftButton:
			return
		
		if (me.pos() - self.drag_start_pos).manhattanLength() < QtGui.qApp.startDragDistance():
			return
		
		drag = QtGui.QDrag(self)
		mimeData = QtCore.QMimeData()
		
		mimeData.setData("text/plain", "rwegergerg")
		drag.setMimeData(mimeData)
		print drag.mimeData().hasFormat('text/plain')
		
		drop_action = drag.start(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction)

