#!/usr/bin/python
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
import sys
import os.path
from qt import *
from launchdlg import LaunchDlg
from connectionmanager import ConnectionManager
from settings import glob_settings
from imageloader import load_pixmap

a = QApplication(sys.argv)

# Try to load a translation file based on the last parameter
if len(sys.argv)>1:
	trans_ext = sys.argv[-1:][0]
	trans = QTranslator()
	trans.load('skolesys-ui_%s.qm' % trans_ext)
	a.installTranslator(trans)
	
QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
conn = ConnectionManager('https://mainserver.localnet',10033)
w = LaunchDlg(conn)
w.setIcon(load_pixmap('app_logo.png'))
a.setMainWidget(w)
w.show()
glob_settings.widgetGeometry('skolesys-ui/MainWindow',w)
a.exec_loop()
glob_settings.setWidgetGeometry('skolesys-ui/MainWindow',w)
glob_settings.saveSettings()
