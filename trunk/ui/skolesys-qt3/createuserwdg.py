from qt import *
from createuserwdgbase import CreateUserWdgBase

class CreateUserWdg(CreateUserWdgBase):
	def __init__(self,conn,parent = None,name = None,fl = 0):
		CreateUserWdgBase.__init__(self,parent,name,fl)
		self.proxy = conn.get_proxy_handle()
		self.setup()
		
	def setup(self):
		# login restriction
		rx = QRegExp('^[a-z][._0-9a-z]*')
		rx_validator = QRegExpValidator(rx,self)
		self.ed_login.setValidator(rx_validator)
		# present the domain name
		self.lbl_domain_name.setText('@%s' % self.proxy.domain_name())
		self.connect(self.ed_login,SIGNAL("textChanged(const QString&)"),self.check_login)
		
		self.typedict={self.tr('Teacher').latin1():1,\
			self.tr('Student').latin1():2,\
			self.tr('Parent').latin1():3,\
			self.tr('Other').latin1():4}
		
		for usertype in self.typedict.keys():
			self.cmb_usertype.insertItem(usertype)

	def check_login(self):
		login=self.ed_login.text().latin1()+self.lbl_domain_name.text().latin1()
		if self.proxy.user_exists(login):
			self.ed_login.setPaletteForegroundColor(Qt.red)
		else:
			self.ed_login.setPaletteForegroundColor(Qt.black)

	def accept(self):
		login=self.ed_login.text().latin1()+self.lbl_domain_name.text().latin1()
		if self.proxy.user_exists(login):
			QMessageBox.information(self,
				self.tr('Create user'),
				self.tr('The user login "%1" already exists on the system - choose another.').arg(login))
			self.ed_login.setFocus()
			self.ed_login.selectAll()
			return False
		firstname=str(self.ed_firstname.text().utf8())
		lastname=str(self.ed_lastname.text().utf8())
		if not len(firstname) or not len(lastname):
			QMessageBox.information(self,
				self.tr('Create user'),
				self.tr('Users must have a full name registered.'))
			if not len(firstname):
				self.ed_firstname.setFocus()
				return False
			if not len(lastname):
				self.ed_lastname.setFocus()
				return False
		# user type
		usertype = self.typedict[self.cmb_usertype.currentText().latin1()]
		# password
		passwd = QInputDialog.getText(self.tr("Password"),self.tr("Confirm the user's password"), QLineEdit.Password)
		if passwd[1]==False or passwd[0].latin1()!=self.ed_passwd.text().latin1():
			self.ed_passwd.setFocus()
			self.ed_passwd.selectAll()
			return False
		print "wiejfwef"
		print self.proxy.createuser(login,firstname,lastname,self.ed_passwd.text().latin1(),usertype)
		return True
