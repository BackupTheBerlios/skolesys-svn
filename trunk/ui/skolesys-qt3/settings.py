from qt import *
import sys

class Settings:
	
	def __init__(self,saveOnExit=True):
		self.cache = {}
		self.settings = QSettings()
		self.dirtymap = {}
		self.oldSize = {}
		self.oldPosition = {}
	
	def setPath(self,domain,product,scope=QSettings.User):
		self.settings.setPath(domain,product,scope)
	
	def setIntEntry(self,subnode,val):
		"""
		Creates a settings variable in the memorystorage and makes it dirty writing in
		the appropriate OS-platform settings system.
		"""
		self.dirtymap[subnode] = 1
		self.cache[subnode] = QVariant(val)
	
	def intEntry(self,subnode,defval=0,forceReadReg=False):
		"""
		Get an int from the settings memory storage or reads it from OS-platform settings system if nessecary.
		If the variable is not stored in one of those the defaultvalue will be written to the memorystorage and
		made dirty for writing to the OS-platform settings system
		"""
		if not forceReadReg and \
			self.cache.has_key(subnode) and \
			self.cache[subnode].canCast(QVariant.Int):
				return self.cache[subnode].toInt(),True
		
		itmp,ok = self.settings.readNumEntry(subnode,defval)
		if not ok:
			self.setIntEntry(subnode,defval)
			return self.cache[subnode].toInt(),False
		
		self.cache[subnode] = QVariant(itmp)
		return self.cache[subnode].toInt(),True
	
	def setRectEntry(self,subnode,rect):
		"""
		Creates a settings variable in the memorystorage and makes it dirty writing in
		the appropriate OS-platform settings system.
		"""
		self.dirtymap[subnode] = 1
		self.cache[subnode] = QVariant(rect)
	
	
	def rectEntry(self,subnode,defval=QRect(50,50,400,300),forceReadReg=False):
		"""
		Get a color from the settings memory storage or reads it from OS-platform settings system if nessecary.
		If the variable is not stored in one of those the defaultvalue will be written to the memorystorage and
		made dirty for writing to the OS-platform settings system
		"""
	
		if not forceReadReg and \
			self.cache.has_key(subnode) and \
			self.cache[subnode].type() == QVariant.Rect:
				return self.cache[subnode].asRect(),True
		
		stmp,ok = self.settings.readEntry(subnode,QString.null)
		if not ok:
			self.setRectEntry(subnode,defval)
			return self.cache[subnode].asRect(),False
		
		rectstrlist = QStringList.split(",",stmp)
		if rectstrlist.count()<4:
			self.setRectEntry(subnode,defval)
			return self.cache[subnode].asRect(),False
		
		l,okl = rectstrlist[0].toInt()
		t,okt = rectstrlist[1].toInt()
		w,okw = rectstrlist[2].toInt()
		h,okh = rectstrlist[3].toInt()
		
		if not okl or not okt or not okw or not okh:
			self.setRectEntry(subnode,defval)
			return self.cache[subnode].asRect(),False
		
		rtmp = QRect(l,t,w,h)
		vtmp = QVariant(rtmp)
		self.cache[subnode] = vtmp
		return self.cache[subnode].asRect(),True
	
	
	def setWidgetGeometry(self,subnode,widget):
		"""
		Save the geometry and window state of a <i>widget</i>.
		If a widget is in maximized,minimized or fullscreen state the normal state geometry 
		should be saved aswell.
		"""
		
		# Check if widget is docked
		clientgeometry = subnode+"/geometry"
		clientwindowState = subnode+"/windowState"
		r = QRect(widget.geometry())
		if widget.windowState() & Qt.WindowMinimized or \
			widget.windowState() & Qt.WindowMaximized or \
			widget.windowState() & Qt.WindowFullScreen:
			if not self.oldSize.contains(widget):
				return
			s = self.oldSize[widget]
			if self.oldPosition.contains(widget):
				p = self.oldPosition[widget]
			else:
				p = QPoint(0,0)
			r = QRect(p,s)
		self.setRectEntry(clientgeometry,r)
		self.setIntEntry(clientwindowState,widget.windowState())
	
	
	def widgetGeometry(self,subnode,widget):
		"""
		Restore the geometry and window state of a workspace client (MDI client)
		"""
		clientgeometry = subnode+"/geometry"
		clientwindowState = subnode+"/windowState"
		widget.setGeometry(self.rectEntry(clientgeometry)[0])
		widget.setWindowState(self.intEntry(clientwindowState)[0])
		return True
	
	def saveSettings(self):
		"""
		Do the actual writing to registry (win32) or files (unix/mac)
		"""
		dirtyVariables = self.dirtymap.keys()
		for slit in dirtyVariables:
			v = self.cache[slit]
			vtyp = v.type()
			if vtyp == QVariant.Font:
				self.writeFont(slit)
			elif vtyp == QVariant.Color:
				self.writeColor(slit)
			elif vtyp == QVariant.StringList:
				self.writeStringList(slit)
			elif vtyp == QVariant.Rect:
				self.writeRect(slit)
			elif vtyp == QVariant.Int:
				self.writeInt(slit)
			elif vtyp == QVariant.Brush:
				self.writeBrush(slit)
			elif vtyp == QVariant.Pen:
				self.writePen(slit)
			else:
				self.writeString(slit)
		return True
	
	
	def writeColor(self,subnode):
		"""
		Used by saveSettings()
		"""
		self.settings.writeEntry(subnode,self.cache[subnode].toString())
		self.dirtymap.pop(subnode)
	
	def writeStringList(self,subnode):
		"""
		Used by saveSettings()
		"""
		sl = QStringList(self.cache[subnode].asStringList())
		self.settings.writeEntry(subnode,sl)
		self.dirtymap.pop(subnode)
	
	def writeString(self,subnode):
		"""
		Used by saveSettings()
		"""
		if self.cache[subnode].canCast(QVariant.String):
			self.settings.writeEntry(subnode,self.cache[subnode].toString())
			self.dirtymap.pop(subnode)
	
	
	def writeFont(self,subnode):
		"""
		Used by saveSettings()
		"""
		font = QFont(self.cache[subnode].asFont())
		fontstrlist = QStringList()
		fontstrlist.append(font.family())
		fontstrlist.append(QString.number(font.pointSize()))
		fontstrlist.append(QString.number(font.bold()))
		fontstrlist.append(QString.number(font.strikeOut()))
		fontstrlist.append(QString.number(font.italic()))
		fontstrlist.append(QString.number(font.underline()))
		self.settings.writeEntry(subnode,fontstrlist.join(","))
		self.dirtymap.pop(subnode)
	
	def writeRect(self,subnode):
		"""
		Used by saveSettings()
		"""
		rect = QRect(self.cache[subnode].asRect())
		rectstrlist = QStringList()
		rectstrlist.append(QString.number(rect.left()))
		rectstrlist.append(QString.number(rect.top()))
		rectstrlist.append(QString.number(rect.width()))
		rectstrlist.append(QString.number(rect.height()))
		self.settings.writeEntry(subnode,rectstrlist.join(","))
		self.dirtymap.pop(subnode)
	
	def writeInt(self,subnode):
		"""
		Used by saveSettings()
		"""
		self.settings.writeEntry(subnode,self.cache[subnode].toInt())
		self.dirtymap.pop(subnode)
	
	def saveWidgetOldSize(self,w,oldsize):
		self.oldSize[w] = oldsize
	
	def saveWidgetOldPosition(self,w,oldpos):
		self.oldPosition[w] = oldpos
	
	
	def writeBrush(self,subnode):
		"""
		Write a QBrush's settings
		"""
		sltmp = QStringList()
		brush = QBrush(self.cache[subnode].asBrush())
		sltmp.append(QVariant(brush.color()).toString())
		sltmp.append(QString.number(int(brush.style())))
		self.settings.writeEntry(subnode,sltmp)
		self.dirtymap.pop(subnode)
	
	def writePen(self,subnode):
		"""
		Write a QPen's settings
		"""
		sltmp = QStringList()
		pen = QPen(self.cache[subnode].asPen())
		sltmp.append(QVariant(pen.color()).toString())
		sltmp.append(QString.number(int(pen.style())))
		sltmp.append(QString.number(int(pen.width())))
		sltmp.append(QString.number(int(pen.capStyle())))
		sltmp.append(QString.number(int(pen.joinStyle())))
		self.settings.writeEntry(subnode,sltmp)
		self.dirtymap.pop(subnode)
	
	
	def subkeyList(self,key):
		"""
		Fetch a list of subkeys for a certain key <i>key</i> 
		"""
		return QStringList(self.settings.subkeyList(key))
	
	def entryList(self,key):
		"""
		Fetch a list of entries for a certain key <i>key</i> 
		"""
		return QStringList(self.settings.entryList(key))
	
	def removeEntry(self,key):
		"""
		Remove a full key from the application settings with all 
		underlying subkeys and entries.
		"""	
		subkeys = subkeyList(key)
		for subkey in subkeys:
			removeEntry(key+"/"+str(subkey))
		
		entries = entryList(key)
		for entry in entries:
			self.settings.removeEntry(key+"/"+str(entry))
		
		return self.settings.removeEntry(key)

glob_settings = Settings()
