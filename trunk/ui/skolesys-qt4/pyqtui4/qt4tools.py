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
from PyQt4 import QtSvg,QtGui,QtCore

def svg2pixmap(svgpath,pix_size_x,pix_size_y,outfile=None,format=None):
	pix=QtGui.QPixmap(pix_size_x,pix_size_y)
	pix.fill(QtCore.Qt.white)
	pix2=QtGui.QPixmap(pix_size_x,pix_size_y)
	pix2.fill(QtCore.Qt.black)
	pix.setAlphaChannel(pix2)
	painter = QtGui.QPainter(pix)
	from PyQt4 import QtSvg
	svg=QtSvg.QSvgRenderer(svgpath)
	svg.render(painter)
	del svg
	if outfile and format:
		pix.save(outfile,format)
	return pix