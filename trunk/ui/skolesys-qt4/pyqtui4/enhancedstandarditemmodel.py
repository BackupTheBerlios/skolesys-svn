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

class EnhancedStandardItemModel(QtGui.QStandardItemModel):

	def __init__(self,parent,columninfo={}):
		QtGui.QStandardItemModel.__init__(self,parent)
		self.accepted_mime_types = QtGui.QStandardItemModel.mimeTypes(self)
		self.columninfo = columninfo

	def addColumn(self,column_key,column_text,columnidx):
		self.columninfo[column_key] = {'text': column_text,'columnindex': columnidx}

	def columnIndexByKey(self,column_key):
		if self.columninfo.has_key(column_key):
			return self.columninfo[column_key]['columnindex']
		return None

	def initialSetup(self):
		columns = {}
		maxidx = 0
		for k,v in self.columninfo.items():
			columns[v['columnindex']] = v['text']
			maxidx = max(maxidx,v['columnindex'])
		self.insertColumns(0,maxidx+1)

		for k,v in columns.items():
			self.setHeaderData(k,QtCore.Qt.Horizontal,QtCore.QVariant(v))
	
	def mimeTypes(self):
		return self.accepted_mime_types

	def setAcceptedMimeTypes(self,list_of_mimetypes):
		self.accepted_mime_types = list_of_mimetypes
		

