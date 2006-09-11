import sys
from qt import *
from skolesys.soap.client import SkoleSYS_Client
import pickle

class ConnectionManager:
	def __init__(self,host,port):
		self.proxy = SkoleSYS_Client(host,port)
		
	def get_proxy_handle(self):
		counter = 0
		while not self.proxy.test_binded() and counter<3:
			passwd = QInputDialog.getText(qApp.translate("General","SkoleSYS Administration"), qApp.translate("General","Enter administrator password"), QLineEdit.Password)
			if passwd[1]==False:
				sys.exit(0)
			if self.proxy.bind(str(passwd[0].utf8())):
				break
			counter+=1
		if counter>=3:
			print "The connection manager has cut this session from further use"
			sys.exit(0)
		return self.proxy

if __name__=='__main__':
	a = QApplication(sys.argv)
	cm = ConnectionManager('https://mainserver',8443)
	if cm.get_proxy_handle():
		print "OK"

