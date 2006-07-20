import sys
from qt import *
from lin4schools.soap.client import L4S_Client

class ConnectionManager:
	def __init__(self,host,port):
		self.proxy = L4S_Client(host,port)
		
	def get_proxy_handle(self):
		counter = 0
		while not self.proxy.test_binded() and counter<3:
			passwd = QInputDialog.getText(qApp.translate("General","lin4schools Administration"), qApp.translate("General","Enter administrator password"), QLineEdit.Password)
			if self.proxy.bind(passwd[0].ascii()):
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

