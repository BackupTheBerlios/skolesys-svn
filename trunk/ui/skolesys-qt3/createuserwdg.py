from qt import *
from createuserwdgbase import CreateUserWdgBase
import config
import skolesys.definitions.userdef as userdef

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
		# present the domain name (This has been removed for the sake of smaller pupils)
		# self.lbl_domain_name.setText('@%s' % self.proxy.domain_name())
		self.connect(self.ed_login,SIGNAL("textChanged(const QString&)"),self.check_login)
		self.connect(self.cmb_usertype,SIGNAL("activated(int)"),self.usertype_changed)
		self.connect(self.cb_allgroups,SIGNAL("toggled(bool)"),self.allgroups_toggled)
		
		thisyear = QDateTime.currentDateTime().date().year()
		self.sbx_firstschoolyear.setValue(thisyear)
		self.sbx_firstschoolyear.setMinValue(thisyear-15)
		self.sbx_firstschoolyear.setMaxValue(thisyear+3)

		setupdict = {}
		self.typedict = {}
		for type_text in userdef.list_usertypes_by_text():
			self.typedict[self.tr(type_text).latin1()] = userdef.usertype_as_id(type_text)
			setupdict[type_text] = { 
				'id': userdef.usertype_as_id(type_text),
				'display': self.tr(type_text).latin1() }
		
		for usertype_text in config.usertype_order:
			if setupdict.has_key(usertype_text):
				self.cmb_usertype.insertItem(setupdict[usertype_text]['display'])
		
		self.usertype_changed()
	
	def groups_to_combo(self,usertype):
		self.cur_groups = self.proxy.list_groups(usertype)
		self.cmb_primarygroup.clear()
		for group in self.cur_groups:
			self.cmb_primarygroup.insertItem(QString.fromUtf8(group))
			
	def update_groupcombo(self):
		if self.cb_allgroups.isChecked():
			return
		usertype_id = self.typedict[self.cmb_usertype.currentText().latin1()]
		self.groups_to_combo(usertype_id)

	def usertype_changed(self):
		self.update_groupcombo()
		usertype_id = self.typedict[self.cmb_usertype.currentText().latin1()]
		if usertype_id==userdef.usertype_as_id('student'):
			self.lbl_firstschoolyear.setEnabled(True)
			self.sbx_firstschoolyear.setEnabled(True)
		else:
			self.lbl_firstschoolyear.setEnabled(False)
			self.sbx_firstschoolyear.setEnabled(False)
	
	def allgroups_toggled(self,toggled):
		if toggled:
			self.groups_to_combo(None)
		else:
			self.update_groupcombo()

	
	def check_login(self):
		login=self.ed_login.text().latin1()#+self.lbl_domain_name.text().latin1()
		if self.proxy.user_exists(login):
			self.ed_login.setPaletteForegroundColor(Qt.red)
		else:
			self.ed_login.setPaletteForegroundColor(Qt.black)

	def accept(self):
		login=self.ed_login.text().latin1()#+self.lbl_domain_name.text().latin1()
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
		# first school year
		firstschoolyear = str(self.sbx_firstschoolyear.value())
		# Primary group
		groupname = str(self.cmb_primarygroup.currentText().utf8())
		if self.cur_groups.has_key(groupname):
			primary_gid = self.cur_groups[groupname]['gidNumber']
		else:
			primary_gid=None
			return True
		# password
		passwd = QInputDialog.getText(self.tr("Password"),self.tr("Confirm the user's password"), QLineEdit.Password)
		if passwd[1]==False or passwd[0].latin1()!=self.ed_passwd.text().latin1():
			self.ed_passwd.setFocus()
			self.ed_passwd.selectAll()
			return False
		res = self.proxy.createuser(login,firstname,lastname,self.ed_passwd.text().latin1(),usertype,primary_gid,firstschoolyear)
		# XXX Handle errors
		if res==1:
			print 'User "%s" created successfully' % login
		return True
