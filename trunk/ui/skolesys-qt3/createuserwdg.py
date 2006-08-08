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
		self.connect(self.cmb_usertype,SIGNAL("activated(int)"),self.update_groupcombo)
		self.connect(self.cb_allgroups,SIGNAL("toggled(bool)"),self.allgroups_toggled)
		
		self.typedict={self.tr('Teacher').latin1():1,\
			self.tr('Student').latin1():2,\
			self.tr('Parent').latin1():3,\
			self.tr('Other').latin1():4}
		
		for usertype in self.typedict.keys():
			self.cmb_usertype.insertItem(usertype)
		
		self.update_groupcombo()
	
	def groups_to_combo(self,usertype):
		self.cur_groups = self.proxy.list_groups(usertype)
		self.cmb_primarygroup.clear()
		for group in self.cur_groups:
			self.cmb_primarygroup.insertItem(QString.fromUtf8(group))
			
	def update_groupcombo(self):
		if self.cb_allgroups.isChecked():
			return
		usertype = self.typedict[self.cmb_usertype.currentText().latin1()]
		self.groups_to_combo(usertype)

	def allgroups_toggled(self,toggled):
		if toggled:
			self.groups_to_combo(None)
		else:
			self.update_groupcombo()

	
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
		# Primary group
		groupname = str(self.cmb_primarygroup.currentText().utf8())
		if self.cur_groups.has_key(groupname):
			primary_gid = self.cur_groups[groupname]['gidNumber']
		else:
			primary_gid=None
			return True
		print primary_gid
		# password
		passwd = QInputDialog.getText(self.tr("Password"),self.tr("Confirm the user's password"), QLineEdit.Password)
		if passwd[1]==False or passwd[0].latin1()!=self.ed_passwd.text().latin1():
			self.ed_passwd.setFocus()
			self.ed_passwd.selectAll()
			return False
		print self.proxy.createuser(login,firstname,lastname,self.ed_passwd.text().latin1(),usertype,primary_gid)
		return True
