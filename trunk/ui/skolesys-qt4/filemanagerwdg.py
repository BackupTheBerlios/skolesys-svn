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

from PyQt4 import QtCore, QtGui
import ui_filemanagerwdg as baseui
import fileinfomodel as fimod
import pyqtui4.pluggablemodelhelper as pmh
import connectionmanager as cm
import pickle,re

rx_float = re.compile('(\d+)(,|\.)(\d+)')

class FileManagerWdg(QtGui.QWidget, baseui.Ui_FileManagerWdg):
	
	def __init__(self,parent):
		QtGui.QWidget.__init__(self,parent)
		# Get connection handle
		self.proxy = cm.get_proxy_handle()
		
		# Setup GUI
		self.setupUi(self)
		self.setupModel()
		self.setupUserFilterCombo()
		self.setupGroupFilterCombo()
		self.setupContentTypeFilterCombo()
		
		# Update file view
		# Jakob: disabled preloading of file info sice it takes too long with no filters setup
		#self.updateFileView()
		
		# Connect threshold sliders
		#self.connect(self.sld_kb_minsize,QtCore.SIGNAL('valueChanged(int)'),self.updateFileView)
		#self.connect(self.sld_kb_minsize,QtCore.SIGNAL('sliderReleased()'),self.updateFileView)
		#self.connect(self.sld_mb_minsize,QtCore.SIGNAL('valueChanged(int)'),self.updateFileView)
		#self.connect(self.sld_mb_minsize,QtCore.SIGNAL('sliderReleased()'),self.updateFileView)
		
		self.minSizeChangeTimer = QtCore.QTimer(self)
		self.minSizeChangeTimer.setSingleShot(True)
		self.connect(self.sbx_kb_minsize,QtCore.SIGNAL('valueChanged(int)'),self.minSizeChanged)
		self.connect(self.sbx_mb_minsize,QtCore.SIGNAL('valueChanged(int)'),self.minSizeChanged)
		self.connect(self.minSizeChangeTimer, QtCore.SIGNAL('timeout()'), self.updateFileView);
		
		# Connect buttons
		self.connect(self.btn_delete,QtCore.SIGNAL('clicked()'),self.removeFiles)

	def setupModel(self):
		self.fileinfomodel = fimod.FileInfoModel(self.trv_files)
		self.modelhelper = pmh.PluggableModelHelper(self.fileinfomodel)
		self.modelhelper.setView(self.trv_files)
		for colidx in xrange(self.fileinfomodel.columnCount()):
			self.modelhelper.setColumnReadOnly(colidx)

	def setupUserFilterCombo(self):
		all_users = self.proxy.list_users(None)
		self.cmb_userfilter.clear()
		self.cmb_userfilter.addItem(self.tr('All',"plural users"),QtCore.QVariant(''))
		usernames = all_users.keys()
		usernames.sort()
		for user in usernames:
			self.cmb_userfilter.addItem(QtCore.QString.fromUtf8(user),QtCore.QVariant(QtCore.QString.fromUtf8(user)))
		self.connect(self.cmb_userfilter,QtCore.SIGNAL('activated(int)'),self.updateFileView)
	
	def setupGroupFilterCombo(self):
		all_groups = self.proxy.list_groups(None)
		self.cmb_groupfilter.clear()
		self.cmb_groupfilter.addItem(self.tr('All',"plural groups"),QtCore.QVariant(''))
		groupnames = all_groups.keys()
		groupnames.sort()
		for group in groupnames:
			self.cmb_groupfilter.addItem(QtCore.QString.fromUtf8(all_groups[group]['displayedName']),QtCore.QVariant(QtCore.QString.fromUtf8(group)))
		self.connect(self.cmb_groupfilter,QtCore.SIGNAL('activated(int)'),self.updateFileView)
	
	def setupContentTypeFilterCombo(self):
		self.cmb_contenttypefilter.clear()
		#self.cmb_contenttypefilter.addItem(self.tr('All content types',"plural content types"),QtCore.QVariant(''))
		#self.cmb_contenttypefilter.addItem(self.tr('Movies (mpg,avi,wmv,...)',"Content types"),QtCore.QVariant(".*\.(avi|mpg|mpeg|wmv)$"))
		#self.cmb_contenttypefilter.addItem(self.tr('Sound (mp3,wav,ogg,...)',"Content types"),QtCore.QVariant(".*\.(wav|mp2|mpeg3|mp3|wma)$"))
		#self.cmb_contenttypefilter.addItem(self.tr('Windows executables (exe,dll,bat,...)',"Content types"),QtCore.QVariant(".*\.(exe|ocx|dll|com|bat)$"))
		#self.cmb_contenttypefilter.addItem(self.tr('OpenOffice docs (odt,ods,odb,...)',"Content types"),QtCore.QVariant(".*\.(odt|ods|odp|odg|odm|odb|odt)$"))
		#self.cmb_contenttypefilter.addItem(self.tr('MS Office docs (doc,xls,mdb,...)',"Content types"),QtCore.QVariant(".*\.(doc|xls|ppt|mdb)$"))
		#self.cmb_contenttypefilter.addItem(self.tr('Archives (zip,rar,cab,...)',"Content types"),QtCore.QVariant(".*\.(zip|arc|arj|lz|rar|tar|tgz|gz|bz2|gzip|cpio|cab|lzh|lha)$"))
		
		self.cmb_contenttypefilter.addItem(self.tr('All content types',"plural content types"),QtCore.QVariant(''))
		self.cmb_contenttypefilter.addItem(self.tr('Movies (mpg,avi,wmv,...)',"Content types"),QtCore.QVariant("avi|mpg|mpeg|wmv"))
		self.cmb_contenttypefilter.addItem(self.tr('Sound (mp3,wav,ogg,...)',"Content types"),QtCore.QVariant("wav|mp2|mpeg3|mp3|wma"))
		self.cmb_contenttypefilter.addItem(self.tr('Windows executables (exe,dll,bat,...)',"Content types"),QtCore.QVariant("exe|ocx|dll|com|bat"))
		self.cmb_contenttypefilter.addItem(self.tr('OpenOffice docs (odt,ods,odb,...)',"Content types"),QtCore.QVariant("odt|ods|odp|odg|odm|odb|odt"))
		self.cmb_contenttypefilter.addItem(self.tr('MS Office docs (doc,xls,mdb,...)',"Content types"),QtCore.QVariant("doc|xls|ppt|mdb"))
		self.cmb_contenttypefilter.addItem(self.tr('Archives (zip,rar,cab,...)',"Content types"),QtCore.QVariant("zip|arc|arj|lz|rar|tar|tgz|gz|bz2|gzip|cpio|cab|lzh|lha"))

		self.connect(self.cmb_contenttypefilter,QtCore.SIGNAL('activated(int)'),self.updateFileView)

	def makeBytesHumanReadable(self,bytes,decimal_clip=2):
		global rx_float
		if bytes<2**10:
			return self.tr("%1  B").arg(bytes)
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
	
	def minSizeChanged(self):
		kb = 2**10
		mb = 2**20
		minsize = kb*self.sbx_kb_minsize.value()
		minsize += mb*self.sbx_mb_minsize.value()
		self.lbl_minsize_threshold.setText(self.makeBytesHumanReadable(minsize))
		self.minSizeChangeTimer.start(1000)
		

	
	def updateFileView(self):
		# Calculate minimum size threshold
		QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
		kb = 2**10
		mb = 2**20
		minsize = kb*self.sbx_kb_minsize.value()
		minsize += mb*self.sbx_mb_minsize.value()
		if minsize==0:
			minsize = None
		
		# Get group filter
		idx = self.cmb_groupfilter.currentIndex()
		if idx > -1:
			groupfilter = str(self.cmb_groupfilter.itemData(idx).toString().toUtf8())
			if groupfilter=='':
				# Group filter set to "All"
				groupfilter = None
		
		# Get user filter
		idx = self.cmb_userfilter.currentIndex()
		if idx > -1:
			userfilter = str(self.cmb_userfilter.itemData(idx).toString().toUtf8())
			if userfilter=='':
				# user filter set to "All"
				userfilter = None
		
		# Get content type filter
		idx = self.cmb_contenttypefilter.currentIndex()
		if idx > -1:
			contenttypefilter = str(self.cmb_contenttypefilter.itemData(idx).toString().toUtf8()).split('|')
			if contenttypefilter==['']:
				# contenttype filter set to "All"
				contenttypefilter = None
			print contenttypefilter
		cnt = self.proxy.countfiles(userfilter,groupfilter,minsize,contenttypefilter,regex=None,order='')
		go_ahead = True
		QtGui.QApplication.restoreOverrideCursor()
		if cnt>1000:
			answer = QtGui.QMessageBox.question(self,
				self.tr('Load File info...'),
				self.tr('The current filter will fetch info for %1 files, this operation may take minutes. '+
					'Do you want to continue?').arg(cnt),
				QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
			if answer==QtGui.QMessageBox.No:
				go_ahead = False
		QtGui.QApplication.processEvents()
		if go_ahead:
			QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
			self.fileinfomodel.loadFileInfo(username=userfilter,groupname=groupfilter,extensions=contenttypefilter,minsize=minsize)
			QtGui.QApplication.restoreOverrideCursor()
		#for colidx in xrange(self.fileinfomodel.columnCount()):
			#self.trv_files.resizeColumnToContents(colidx)
	
	# Actions on files
	def removeFiles(self):
		mimedata = self.fileinfomodel.generateMimeData(self.trv_files.selectedIndexes())
		rmlist = []
		for f in pickle.loads(mimedata['application/x-skolesysfiles-pyobj']):
			path = "%s/%s" % (f['dirname'],f['filename'])
			rmlist += ["%s/%s" % (f['dirname'],f['filename'])]
			self.fileinfomodel._removeFileInfo(path)
			
		self.proxy.removefiles(rmlist)


if __name__ == '__main__':
	import sys
	app = QtGui.QApplication(sys.argv)
	ui = FileManagerWdg(None)
	
	ui.show()
	sys.exit(app.exec_())
