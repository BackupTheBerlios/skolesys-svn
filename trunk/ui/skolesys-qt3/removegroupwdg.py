from removegroupwdgbase import RemoveGroupWdgBase
from qt import *

class RemoveGroupWdg(RemoveGroupWdgBase):
	def __init__(self,conn,groupname,parent = None,name = None,fl = 0):
		RemoveGroupWdgBase.__init__(self,parent,name,fl)
		self.groupname = groupname
		self.proxy = conn.get_proxy_handle()

	def accept(self):
		answer = QMessageBox.question(self,
			self.tr('Remove group'),
			self.tr('Are you sure you want to remove "%1"?').arg(QString.fromUtf8(self.groupname)),
			QMessageBox.Yes,QMessageBox.No)
		if answer==QMessageBox.No:
			return False
		self.proxy.removegroup(self.groupname,self.chb_backup_home.isChecked(),self.chb_remove_home.isChecked())
		return True
