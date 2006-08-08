#!/usr/bin/python
import sys
import os.path
from qt import *
from launchdlg import LaunchDlg
from connectionmanager import ConnectionManager
from lin4schools.soap.client import L4S_Client
from settings import glob_settings

a = QApplication(sys.argv)

# Try to load a translation file based on the last parameter
if len(sys.argv)>1:
	trans_ext = sys.argv[-1:][0]
	trans = QTranslator()
	trans.load('l4s_admin_%s.qm' % trans_ext)
	a.installTranslator(trans)
	
QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
conn = ConnectionManager('https://mainserver',8443)
w = LaunchDlg(conn)
pix = QPixmap('app_logo.png')
w.setIcon(pix)
a.setMainWidget(w)
w.show()
glob_settings.widgetGeometry('ssys_admin/MainWindow',w)
a.exec_loop()
glob_settings.setWidgetGeometry('ssys_admin/MainWindow',w)
glob_settings.saveSettings()
