from removegroupwdgbase import RemoveGroupWdgBase
from qt import *

class RemoveGroupWdg(RemoveGroupWdgBase):
	def __init__(self,conn,groupnames,parent = None,name = None,fl = 0):
		RemoveGroupWdgBase.__init__(self,parent,name,fl)
		self.groupnames = groupnames
		for groupname in groupnames:
			self.lb_groupnames.insertItem(QString.fromUtf8(groupname))
		self.proxy = conn.get_proxy_handle()

	def accept(self):
		answer = QMessageBox.question(self,
			self.tr('Remove group(s)'),
			self.tr('Are you sure you want to perform this remove operation?'),
			QMessageBox.Yes,QMessageBox.No)
		if answer==QMessageBox.No:
			return False
		for groupname in self.groupnames:
			self.proxy.removegroup(groupname,self.chb_backup_home.isChecked(),self.chb_remove_home.isChecked())
		return True
