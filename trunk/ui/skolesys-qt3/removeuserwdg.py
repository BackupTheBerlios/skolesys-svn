from removeuserwdgbase import RemoveUserWdgBase
from qt import *

class RemoveUserWdg(RemoveUserWdgBase):
	def __init__(self,conn,uid,parent = None,name = None,fl = 0):
		RemoveUserWdgBase.__init__(self,parent,name,fl)
		self.uid = uid
		self.proxy = conn.get_proxy_handle()

	def accept(self):
		answer = QMessageBox.question(self,
			self.tr('Remove user'),
			self.tr('Are you sure you want to remove "%1"?').arg(self.uid),
			QMessageBox.Yes,QMessageBox.No)
		if answer==QMessageBox.No:
			return False
		self.proxy.removeuser(self.uid,self.chb_backup_home.isChecked(),self.chb_remove_home.isChecked())
		return True
