from PyQt4 import QtCore,QtGui
import pyqtui4.typecheck as typecheck


class EnhancedTreeView(QtGui.QTreeWidget):
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
	v = EnhancedTreeView(self)
	
	# decorate with the custom event handler hook_drag_enter()
	v.connectEvent("dragEvent" ,hook_drag_enter)
	"""
	def __init__(self,parent):
		QtGui.QTreeWidget.__init__(self,parent)
		#self.drag_start_pos = None
		self.hooked_functions = {}
		self.header().setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.connect(self.header(),QtCore.SIGNAL("customContextMenuRequested(const QPoint&)"),self.headerContextMenu)
		self.base_cls = QtGui.QTreeWidget
		self.enhanced_model = False
		self.recursionlock = False

		
	def setModel(self,model):
		import pyqtui4.enhancedstandarditemmodel as esm
		self.enhanced_model = False
		if typecheck.check_inheritance(model,[esm.EnhancedStandardItemModel]):
			self.enhanced_model = True
		self.base_cls.setModel(self,model)


	def headerContextMenu(self,pos):
		model = self.model()
		if self.enhanced_model:
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
			if action:
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
		self.base_cls.dragEnterEvent(self,dee)
		self._callback("dragEnterEvent",dee)

	def dragMoveEvent(self,dme):
		self.base_cls.dragMoveEvent(self,dme)
		self._callback("dragMoveEvent",dme)
	
	def dragLeaveEvent(self,dle):
		self.base_cls.dragLeaveEvent(self,dle)
		self._callback("dragLeaveEvent",dle)


	def dropEvent(self,de):
		self._callback("dropEvent",de)

	def mousePressEvent(self,pe):
		#if pe.button() == QtCore.Qt.LeftButton:
			#self.drag_start_pos = QtCore.QPoint(pe.pos())
		self._callback("mousePressEvent",pe)
		self.base_cls.mousePressEvent(self,pe)

	#def mouseMoveEvent(self,me):
		#if not me.buttons() & QtCore.Qt.LeftButton:
			#return
		
		#if (me.pos() - self.drag_start_pos).manhattanLength() < QtGui.qApp.startDragDistance():
			#return
		
		#self._callback("mouseMoveEvent",me)
		#self.base_cls.mouseMoveEvent(self,me)
			
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

