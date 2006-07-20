from qt import *
from createuserwdgbase import CreateUserWdgBase

class CreateUserWdg(CreateUserWdgBase):
	def __init__(self,conn,parent = None,name = None,fl = 0):
		CreateUserWdgBase.__init__(self,parent,name,fl)
		self.proxy = conn.get_proxy_handle()
		
	def accept(self):
		login=self.ed_login.text().latin1()
		firstname=self.ed_firstname.text().latin1()
		lastname=self.ed_lastname.text().latin1()
		self.proxy.createuser(login,firstname,lastname,'123456',1)
		return True
