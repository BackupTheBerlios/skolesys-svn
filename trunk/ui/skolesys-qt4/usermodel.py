from PyQt4 import QtCore,QtGui
import skolesys.definitions.userdef as userdef
import pickle,pprint,StringIO,os
import pyqtui4.enhancedstandarditemmodel as esm
import skolesys.definitions.userdef as userdef
import skolesys.tools.schooltime as stime
import pyqtui4.qt4tools as qt4tools

class UserModel(esm.EnhancedStandardItemModel):
	def __init__(self,conn,parent):
		esm.EnhancedStandardItemModel.__init__(self,parent)
		self.proxy = conn.get_proxy_handle()
		self.users = {}
		self.columninfo = {
			'uidnumber': {'text': self.tr('User ID'), 'columnindex': 3},
			'uid': {'text': self.tr('Login'), 'columnindex': 1},
			'cn': {'text': self.tr('User name'), 'columnindex': 0},
			'usertype': {'text': self.tr('User type'), 'columnindex': 2} }
		self.initialSetup()
		self.tr("teacher","singular")
		self.tr("student","singular")
		self.tr("parent","singular")
		self.tr("other","singular")
		default_icon = 'art/student.svg'
		self.icons = {}
		for usertype in userdef.list_usertypes_by_text():
			icon = default_icon
			if os.path.exists('art/%s.svg' % usertype):
				icon = 'art/%s.svg' % usertype
			self.icons[userdef.usertype_as_id(usertype)] = qt4tools.svg2pixmap(icon,24,24)

	def _addUser(self,uidnumber,uid,cn,usertype_id):
		if self.users.has_key(int(uidnumber)):
			return
		self.insertRow(self.rowCount())
		
		idx = self.index(self.rowCount()-1,self.columninfo['cn']['columnindex'])
		
		self.setData(idx,QtCore.QVariant(self.icons[usertype_id]),QtCore.Qt.DecorationRole)
		self.setData(idx,QtCore.QVariant(QtCore.QString.fromUtf8(cn)))
		idx = self.index(self.rowCount()-1,self.columninfo['uid']['columnindex'])
		self.setData(idx,QtCore.QVariant(QtCore.QString.fromUtf8(uid)))
		idx = self.index(self.rowCount()-1,self.columninfo['uidnumber']['columnindex'])
		self.setData(idx,QtCore.QVariant(uidnumber))
		idx = self.index(self.rowCount()-1,self.columninfo['usertype']['columnindex'])
		self.setData(idx,QtCore.QVariant(self.tr(userdef.usertype_as_text(usertype_id),"singular")))
		
		idx = self.index(self.rowCount()-1,0)
		self.setData(idx,QtCore.QVariant(uidnumber),QtCore.Qt.UserRole)
		
		self.users[int(uidnumber)] = {
			'uidnumber':uidnumber,
			'uid':uid,
			'cn':cn,
			'usertype_id':usertype_id}

	def _removeUser(self,uidnumber):
		for rownum in xrange(self.rowCount()):
			idx = self.index(rownum,self.columninfo['cn']['columnindex'])
			rowuidnumber,ok = idx.data(QtCore.Qt.UserRole).toInt()
			if ok and rowuidnumber==int(uidnumber):
				self.removeRow(rownum)
				self.users.pop(int(uidnumber))
				break

	def userNames(self):
		usernames = []
		for k,v in self.users.items():
			usernames += [v['uid']]
		return usernames
	
	def loadUsers(self,usertype_id=None,groupname=None,min_grade=None,max_grade=None):
		self.clear()
		self.initialSetup()
		self.users = {}
		if groupname:
			groupmembers = self.proxy.list_members(groupname)
		users = self.proxy.list_users(usertype_id)
		for u,v in users.items():
			if groupname and type(groupmembers)==list and not groupmembers.count(v['uid']):
				continue

			# Filter by classyear (aargang)
			if min_grade != None and max_grade != None:
				if v.has_key('firstSchoolYear'):
					classyear = stime.firstyear_to_classyear(int(v['firstSchoolYear']))
					if classyear < min_grade or classyear > max_grade:
						continue

			usertype_id = 2
			if v.has_key('usertype_id'):
				usertype_id = v['usertype_id']
			self._addUser(
				v['uidNumber'],v['uid'],
				v['cn'],usertype_id)
				
	def generateMimeData(self,indexes=None):
		if indexes == None:
			indexes = []
			for rowidx in xrange(self.rowCount()):
				indexes += [self.index(rowidx,0)]
		mimedata = {}
		users = []
		pyobj = []
		row_handled = {}
		for idx in indexes:
			if row_handled.has_key(idx.row()):
				continue
			row_handled[idx.row()] = 1
			idx = self.index(idx.row(),0)
			users += [str(idx.data().toString().toUtf8())]
			uidnumber,ok = idx.data(QtCore.Qt.UserRole).toInt()
			if self.users.has_key(uidnumber):
				pyobj += [self.users[uidnumber]]
				
		#iostr = StringIO.StringIO()
		#pprint.pprint(pyobj,iostr)
		#mimedata['text/plain'] = iostr.getvalue()
		#iostr.close()
		mimedata['text/plain'] = "\n".join(users)
		mimedata['application/x-skolesysusers-pyobj'] = pickle.dumps(pyobj)
		return mimedata
	
	def mimeData(self,indexes):
		mimedata = self.generateMimeData(indexes)
		q_mimedata = QtCore.QMimeData()
		q_mimedata.setData("application/x-skolesysusers-pyobj", mimedata["application/x-skolesysusers-pyobj"])
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

