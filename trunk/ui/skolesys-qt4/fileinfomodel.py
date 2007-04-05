from PyQt4 import QtCore,QtGui
import pickle,re
import pyqtui4.enhancedstandarditemmodel as esm
import connectionmanager as cm

rx_float = re.compile('(\d+)(,|\.)(\d+)')
QtCore.Qt.ForegroundRole = 9

class FileInfoModel(esm.EnhancedStandardItemModel):
	def __init__(self,parent):
		esm.EnhancedStandardItemModel.__init__(self,parent)
		self.proxy = cm.get_connection().get_proxy_handle()
		self.files = {}
		self.exclude_grouptype_ids=[]
		self.exclude_gid_numbers=[]
		self.displayed_groupnames = {}
		self.proxy = cm.get_connection().get_proxy_handle()
		groups = self.proxy.list_groups()
		for grpname,details in groups.items():
			self.displayed_groupnames[grpname] = details['displayedName']
		self.columninfo = {
			'filename': {'text': self.tr('File name'), 'columnindex': 0},
			'dirname': {'text': self.tr('Directory'), 'columnindex': 1},
			'username': {'text': self.tr('User'), 'columnindex': 2},
			'groupname': {'text': self.tr('Group'), 'columnindex': 3},
			'permissions': {'text': self.tr('Permissions'), 'columnindex': 4},
			'filesize': {'text': self.tr('Size'), 'columnindex': 5}}
		self.initialSetup()

	def makeBytesHumanReadable(self,bytes,decimal_clip=2):
		global rx_float
		if bytes<2**10:
			return self.tr("%1 B ").arg(bytes)
		if bytes<2**20:
			loc = QtCore.QLocale()
			val = str(loc.toString(float(bytes)/2**10,'g',4))
			m = rx_float.match(val)
			if m:
				val = m.groups()[0]+m.groups()[1]+m.groups()[2][:decimal_clip]
			return self.tr("%1 KB").arg(val)
		if bytes<2**30:
			loc = QtCore.QLocale()
			val = str(loc.toString(float(bytes)/2**20,'g',4))
			m = rx_float.match(val)
			if m:
				val = m.groups()[0]+m.groups()[1]+m.groups()[2][:decimal_clip]
			return self.tr("%1 MB").arg(val)
	
	def _addFileInfo(self,filename,dirname,username,groupname,filesize,permissions):
		path = "%s/%s" % (dirname,filename) # the obvious ... full path
		if self.files.has_key(path):
			return
		self.insertRow(self.rowCount())
		idx = self.index(self.rowCount()-1,self.columninfo['filename']['columnindex'])
		#pix = QtGui.QPixmap()
		#pix.load('art/kdmconfig.png')
		#pix = pix.scaled(QtCore.QSize(24,24))
		#self.setData(idx,QtCore.QVariant(pix),QtCore.Qt.DecorationRole)
		self.setData(idx,QtCore.QVariant(QtCore.QString.fromUtf8(filename)))
		
		idx = self.index(self.rowCount()-1,self.columninfo['dirname']['columnindex'])
		self.setData(idx,QtCore.QVariant(QtCore.QString.fromUtf8(dirname)))
		
		idx = self.index(self.rowCount()-1,self.columninfo['username']['columnindex'])
		self.setData(idx,QtCore.QVariant(username))
		
		idx = self.index(self.rowCount()-1,self.columninfo['groupname']['columnindex'])
		if self.displayed_groupnames.has_key(groupname):
			self.setData(idx,QtCore.QVariant(QtCore.QString.fromUtf8(self.displayed_groupnames[groupname])))
		else:
			self.setData(idx,QtCore.QVariant(groupname))
		
		idx = self.index(self.rowCount()-1,self.columninfo['filesize']['columnindex'])
		self.setData(idx,QtCore.QVariant(self.makeBytesHumanReadable(filesize)))
		self.setData(idx,QtCore.QVariant(QtCore.Qt.AlignRight),QtCore.Qt.TextAlignmentRole)
		kb = 2**10
		mb = 2**20
		if filesize>=kb and filesize<mb:
			self.setData(idx,QtCore.QVariant(QtGui.QBrush(QtGui.QColor(90,90,90))),QtCore.Qt.ForegroundRole)
		elif filesize>=mb and filesize<mb*3:
			self.setData(idx,QtCore.QVariant(QtGui.QBrush(QtCore.Qt.darkYellow)),QtCore.Qt.ForegroundRole)
		elif filesize>=mb*3 and filesize<mb*6:
			self.setData(idx,QtCore.QVariant(QtGui.QBrush(QtCore.Qt.magenta)),QtCore.Qt.ForegroundRole)
		elif filesize>=mb*6:
			self.setData(idx,QtCore.QVariant(QtGui.QBrush(QtCore.Qt.red)),QtCore.Qt.ForegroundRole)
		else:
			self.setData(idx,QtCore.QVariant(QtGui.QBrush(QtCore.Qt.gray)),QtCore.Qt.ForegroundRole)
		
		idx = self.index(self.rowCount()-1,self.columninfo['permissions']['columnindex'])
		self.setData(idx,QtCore.QVariant(permissions))
		
		idx = self.index(self.rowCount()-1,0)
		self.setData(idx,QtCore.QVariant(QtCore.QString.fromUtf8(path)),QtCore.Qt.UserRole)
		
		self.files[path] = {
			'filename':filename,
			'dirname':dirname,
			'username':username,
			'groupname':groupname,
			'filesize':filesize,
			'permissions':permissions}

	def _removeFileInfo(self,path):
		for rownum in xrange(self.rowCount()):
			idx = self.index(rownum,0)
			rowpath = idx.data(QtCore.Qt.UserRole).toString().toUtf8()
			if rowpath==path:
				self.removeRow(rownum)
				self.files.pop(path)
				break

	def fileNames(self):
		filenames = []
		for fname in self.files.keys():
			filenames += [fname]
		return filenames
	
	def loadFileInfo(self,username=None,groupname=None,minsize=None,regex=None,order=''):
		self.clear()
		self.initialSetup()
		self.files = {}
		
		files = self.proxy.findfiles(username,groupname,minsize,regex,order)
		for f in files:
			self._addFileInfo(
				f['filename'],f['dirname'],
				f['user'],f['group'],
				f['size'],f['permissions'])
				
	def generateMimeData(self,indexes=None):
		if indexes == None:
			indexes = []
			for rowidx in xrange(self.rowCount()):
				indexes += [self.index(rowidx,0)]
		mimedata = {}
		files = []
		pyobj = []
		row_handled = {}
		for idx in indexes:
			if row_handled.has_key(idx.row()):
				continue
			row_handled[idx.row()] = 1
			idx = self.index(idx.row(),0)
			files += [str(idx.data(QtCore.Qt.UserRole).toString().toUtf8())]
			path = str(idx.data(QtCore.Qt.UserRole).toString().toUtf8())
			if self.files.has_key(path):
				pyobj += [self.files[path]]
					
		mimedata['text/plain'] = ";".join(files)
		mimedata['application/x-skolesysfiles-pyobj'] = pickle.dumps(pyobj)
		return mimedata
	
	def mimeData(self,indexes):
		mimedata = self.generateMimeData(indexes)
		q_mimedata = QtCore.QMimeData()
		q_mimedata.setData("application/x-skolesysfiles-pyobj", mimedata["application/x-skolesysfiles-pyobj"])
		q_mimedata.setData("text/plain", mimedata["text/plain"])
		
		return q_mimedata	

