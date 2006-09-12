#!/usr/bin/python
import sys
import os.path
from qt import *
from launchdlg import LaunchDlg
from connectionmanager import ConnectionManager
from skolesys.soap.client import SkoleSYS_Client
from settings import glob_settings
from imageloader import load_pixmap

a = QApplication(sys.argv)

# Try to load a translation file based on the last parameter
if len(sys.argv)>1:
	trans_ext = sys.argv[-1:][0]
	trans = QTranslator()
	trans.load('skolesys_ui_%s.qm' % trans_ext)
	a.installTranslator(trans)
	
QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
conn = ConnectionManager('https://mainserver.skolesys.local',8443)
w = LaunchDlg(conn)
w.setIcon(load_pixmap('app_logo.png'))
a.setMainWidget(w)
w.show()
glob_settings.widgetGeometry('ssys_admin/MainWindow',w)
a.exec_loop()
glob_settings.setWidgetGeometry('ssys_admin/MainWindow',w)
glob_settings.saveSettings()
