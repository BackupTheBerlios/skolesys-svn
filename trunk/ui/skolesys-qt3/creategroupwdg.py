from qt import *
from creategroupwdgbase import CreateGroupWdgBase
import skolesys.definitions.userdef as userdef

class CreateGroupWdg(CreateGroupWdgBase):
	def __init__(self,conn,parent = None,name = None,fl = 0):
		CreateGroupWdgBase.__init__(self,parent,name,fl)
		self.proxy = conn.get_proxy_handle()
		self.setup()
		
	def setup(self):
		# login restriction
		rx = QRegExp('\\w+')
		rx_validator = QRegExpValidator(rx,self)
		self.ed_groupname.setValidator(rx_validator)
		self.connect(self.ed_groupname,SIGNAL("textChanged(const QString&)"),self.check_group)
		
		self.typedict={self.tr('Teacher').latin1():userdef.check_usertype_text('teacher'),\
			self.tr('Student').latin1():userdef.check_usertype_text('student'),\
			self.tr('Parent').latin1():userdef.check_usertype_text('parent'),\
			self.tr('Other').latin1():userdef.check_usertype_text('other')}
		
		for usertype in self.typedict.keys():
			self.cmb_usertype.insertItem(usertype)

	def check_group(self):
		groupname=str(self.ed_groupname.text().utf8())
		if self.proxy.group_exists(groupname):
			self.ed_groupname.setPaletteForegroundColor(Qt.red)
		else:
			self.ed_groupname.setPaletteForegroundColor(Qt.black)

	def accept(self):
		groupname=str(self.ed_groupname.text().utf8())
		if self.proxy.group_exists(groupname):
			QMessageBox.information(self,
				self.tr('Create group'),
				self.tr('The group "%1" already exists on the system - choose another.').arg(groupname))
			self.ed_groupname.setFocus()
			self.ed_groupname.selectAll()
			return False
		# user type
		usertype = self.typedict[self.cmb_usertype.currentText().latin1()]
		desc = str(self.te_description.text().utf8())[:1020]
		print self.proxy.creategroup(groupname,usertype,desc)
		return True
