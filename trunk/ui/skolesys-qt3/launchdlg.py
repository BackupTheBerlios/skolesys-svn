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
from launchdlgbase import LaunchDlgBase
from launcher import *
from imageloader import load_pixmap
class LaunchDlg(LaunchDlgBase):
	def __init__(self,conn,parent=None,name=None,modal=1,fl=0):
		LaunchDlgBase.__init__(self,parent,name,modal,fl)
		self.lbl_logo.setPixmap(load_pixmap('logo_small.png'))
		self.conn = conn
		
	def userManager(self):
		execUserManager(self.conn)

	def groupManager(self):
		execGroupManager(self.conn)
