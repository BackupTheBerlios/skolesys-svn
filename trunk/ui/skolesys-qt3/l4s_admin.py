import sys
from qt import *
from launchdlg import LaunchDlg
from connectionmanager import ConnectionManager
from lin4schools.soap.client import L4S_Client

a = QApplication(sys.argv)
QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
conn = ConnectionManager('https://mainserver',8443)
w = LaunchDlg(conn)
a.setMainWidget(w)
w.show()
a.exec_loop()

