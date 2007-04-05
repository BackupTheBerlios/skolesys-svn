from PyQt4 import QtCore,QtGui
import skolesys.definitions.groupdef as groupdef
import pickle
import pyqtui4.enhancedstandarditemmodel as esm
import skolesys.definitions.groupdef as groupdef
import pyqtui4.qt4tools as qt4tools

class GroupModel(esm.EnhancedStandardItemModel):
	def __init__(self,conn,parent):
		esm.EnhancedStandardItemModel.__init__(self,parent)
		self.proxy = conn.get_proxy_handle()
		self.groups = {}
		self.exclude_grouptype_ids=[]
		self.exclude_gid_numbers=[]
		self.columninfo = {
			'gid': {'text': self.tr('Group ID'), 'columnindex': 3},
			'groupname': {'text': self.tr('Group name'), 'columnindex': 1},
			'displayed_name': {'text': self.tr('Displayed name'), 'columnindex': 0},
			'grouptype': {'text': self.tr('Group type'), 'columnindex': 2} }
		self.initialSetup()
		self.tr("primary","singular")
		self.tr("system","singular")
		self.tr("service","singular")

	def _addGroup(self,gid,groupname,displayed_name,grouptype_id):
		if self.groups.has_key(int(gid)):
			return
		self.insertRow(self.rowCount())
		idx = self.index(self.rowCount()-1,self.columninfo['displayed_name']['columnindex'])
		self.setData(idx,QtCore.QVariant(qt4tools.svg2pixmap('art/group.svg',24,24)),QtCore.Qt.DecorationRole)
		self.setData(idx,QtCore.QVariant(QtCore.QString.fromUtf8(displayed_name)))
		self.setData(idx,QtCore.QVariant(gid),QtCore.Qt.UserRole)
		idx = self.index(self.rowCount()-1,self.columninfo['groupname']['columnindex'])
		self.setData(idx,QtCore.QVariant(QtCore.QString.fromUtf8(groupname)))
		idx = self.index(self.rowCount()-1,self.columninfo['gid']['columnindex'])
		self.setData(idx,QtCore.QVariant(gid))
		idx = self.index(self.rowCount()-1,self.columninfo['grouptype']['columnindex'])
		self.setData(idx,QtCore.QVariant(self.tr(groupdef.grouptype_as_text(grouptype_id),"singular")))
		
		idx = self.index(self.rowCount()-1,0)
		self.setData(idx,QtCore.QVariant(gid),QtCore.Qt.UserRole)
		
		self.groups[int(gid)] = {
			'gid':gid,
			'groupname':groupname,
			'displayed_name':displayed_name,
			'grouptype_id':grouptype_id}

	def _removeGroup(self,gid):
		for rownum in xrange(self.rowCount()):
			idx = self.index(rownum,self.columninfo['displayed_name']['columnindex'])
			rowgid,ok = idx.data(QtCore.Qt.UserRole).toInt()
			if ok and rowgid==int(gid):
				self.removeRow(rownum)
				self.groups.pop(int(gid))
				break

	def groupNames(self):
		groupnames = []
		for k,v in self.groups.items():
			groupnames += [v['groupname']]
		return groupnames
	
	def loadGroups(self,grouptype_id=None,username=None):
		self.clear()
		self.initialSetup()
		self.groups = {}
		if username:
			usergroups = self.proxy.list_usergroups(username)
		groups = self.proxy.list_groups(grouptype_id)
		for g,v in groups.items():
			if username and type(usergroups)==list and not usergroups.count(v['cn']):
				continue

			if list(self.exclude_gid_numbers).count(int(v['gidNumber'])):
				continue
			if list(self.exclude_grouptype_ids).count(int(v['grouptype_id'])):
				continue
			self._addGroup(
				v['gidNumber'],v['cn'],
				v['displayedName'],v['grouptype_id'])
				
	def generateMimeData(self,indexes=None):
		if indexes == None:
			indexes = []
			for rowidx in xrange(self.rowCount()):
				indexes += [self.index(rowidx,0)]
		mimedata = {}
		groups = []
		pyobj = []
		row_handled = {}
		for idx in indexes:
			if row_handled.has_key(idx.row()):
				continue
			row_handled[idx.row()] = 1
			idx = self.index(idx.row(),0)
			groups += [str(idx.data().toString().toUtf8())]
			gid,ok = idx.data(QtCore.Qt.UserRole).toInt()
			if self.groups.has_key(gid):
				pyobj += [self.groups[gid]]
					
		mimedata['text/plain'] = "\n".join(groups)
		mimedata['application/x-skolesysgroups-pyobj'] = pickle.dumps(pyobj)
		return mimedata
	
	def mimeData(self,indexes):
		mimedata = self.generateMimeData(indexes)
		q_mimedata = QtCore.QMimeData()
		q_mimedata.setData("application/x-skolesysgroups-pyobj", mimedata["application/x-skolesysgroups-pyobj"])
		q_mimedata.setData("text/plain", mimedata["text/plain"])
		
		return q_mimedata	

	#def dragEnterEvent(self,dee):
		#QtGui.QTreeView.dragEnterEvent(self,dee)
		#if dir(self).count('hook_dragEnterEvent'):
			#self.hook_dragEnterEvent(self,dee)
		#dee.ignore()

	#def dragLeaveEvent(self,dle):
		#if dir(self).count('hook_dragLeaveEvent'):
			#self.hook_dragEnterEvent(self,dee)


	#def dropEvent(self,de):
		#print de.mimeData().data('text/plain')
		#print "Dropped items"

	#def mousePressEvent(self,pe):
		#if pe.button() == QtCore.Qt.LeftButton:
			#self.drag_start_pos = QtCore.QPoint(pe.pos())
		#QtGui.QTreeView.mousePressEvent(self,pe)

	#def mouseMoveEvent(self,me):
		#if not me.buttons() & QtCore.Qt.LeftButton:
			#return
		
		#if (me.pos() - self.drag_start_pos).manhattanLength() < QtGui.qApp.startDragDistance():
			#return
		
		#drag = QtGui.QDrag(self)
		#mimeData = QtCore.QMimeData()
		
		#mimeData.setData("text/plain", "rwegergerg")
		#drag.setMimeData(mimeData)
		#print drag.mimeData().hasFormat('text/plain')
		
		#drop_action = drag.start(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction)

