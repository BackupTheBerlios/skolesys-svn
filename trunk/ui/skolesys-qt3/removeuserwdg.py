from removeuserwdgbase import RemoveUserWdgBase
from qt import *

class RemoveUserWdg(RemoveUserWdgBase):
	def __init__(self,conn,uids,parent = None,name = None,fl = 0):
		RemoveUserWdgBase.__init__(self,parent,name,fl)
		self.uids = uids
		for uid in uids:
			self.lb_users.insertItem(uid)
		self.proxy = conn.get_proxy_handle()

	def accept(self):
		answer = QMessageBox.question(self,
			self.tr('Remove user(s)'),
			self.tr('Are you sure you want to perform this remove operation?'),
			QMessageBox.Yes,QMessageBox.No)
		if answer==QMessageBox.No:
			return False
		for uid in self.uids:
			self.proxy.removeuser(uid,self.chb_backup_home.isChecked(),self.chb_remove_home.isChecked())
		return True
