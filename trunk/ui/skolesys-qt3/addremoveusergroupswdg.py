import sys
from qt import *
from addremovewdgbase import AddRemoveWdgBase
from groupmanagerwdg import *
from progressdlg import ProgressDlg
from settings import glob_settings


class AddRemoveUserGroupsWdg(AddRemoveWdgBase):
	"""
	Create and destroy user/group memberships from the user managers
	point of view. Thus a range of users have been selected and now we want
	to add and remove group connections.
	"""
	def __init__(self,conn,uids,parent = None,name = None,fl = 0):
		AddRemoveWdgBase.__init__(self,parent,name,fl)
		self.gm_wdg = GroupManagerWdg(conn,self,"lb_groups")
		self.gm_wdg.contextmenu_enabled = False
		self.mainlayout.addMultiCellWidget(self.gm_wdg,1,8,0,0)
		self.uids = uids
		
		# Populate the subjects listbox
		for uid in uids:
			self.lb_subjects.insertItem(uid)
		
		self.conn = conn # For passing on to create/remove groups
		self.soapproxy = conn.get_proxy_handle()
		self.connect(self.btn_add_add,SIGNAL("clicked()"),self.addToAddClicked)
		self.connect(self.btn_add_remove,SIGNAL("clicked()"),self.addToRemoveClicked)
		
	def languageChange(self):
		self.setCaption(self.tr("Form1"))
		self.remove_label.setText(self.tr("Remove"))
		self.add_label.setText(self.tr("Add"))
	
	def addToListbox(self,lb_addbox,lb_ctrlbox):
		groupnames = self.gm_wdg.selectedGroupnames()
		comparemode = Qt.CaseSensitive | Qt.ExactMatch
		for groupname in groupnames:
			qstr_groupname = QString.fromUtf8(groupname)
			
			# Add the groupname if not present
			item = lb_addbox.findItem(qstr_groupname,comparemode)
			if not item:
				lb_addbox.insertItem(qstr_groupname)
			
			# Remove the groupname from the other box if it is present
			item = lb_ctrlbox.findItem(qstr_groupname,comparemode)
			if item:
				lb_ctrlbox.removeItem(lb_ctrlbox.index(item))
	
	def addToAddClicked(self):
		self.addToListbox(self.lb_add,self.lb_remove)

	def addToRemoveClicked(self):
		self.addToListbox(self.lb_remove,self.lb_add)

	def accept(self):
		answer = QMessageBox.question(self,
			self.tr('Alter group memberships'),
			self.tr('Are you sure you want to perform this operation?'),
			QMessageBox.Yes,QMessageBox.No)
		if answer==QMessageBox.No:
			return False
			
		progdlg = ProgressDlg(self.tr("Altering memberships..."),self,"progress",True)
		progdlg.setTotalSteps(len(self.uids)*(self.lb_add.count()+self.lb_remove.count())-1)
		
		glob_settings.widgetGeometry('skolesys-ui/AddRemoveUserGroups/ProgressDlg',progdlg)
		progdlg.show()
		show_details = glob_settings.intEntry('skolesys-ui/AddRemoveUserGroups/ProgressDlg/show_details',0)[0]
		progdlg.showDetails(show_details)

		progress = 0
		for uid in self.uids:
			# Add groups
			progdlg.setLabelText(self.tr("Altering memberships of %1").arg(uid))
			for idx in xrange(self.lb_add.count()):	
				addgroup = str(self.lb_add.text(idx).utf8())
				details = self.tr('Adding user "%1" to the group "%2" ... ').arg(uid).arg(QString.fromUtf8(addgroup))			
				res = self.soapproxy.groupadd(uid,addgroup)
				if res==1:
					details += self.tr('USER ADDED')
				if res==-3:
					details += self.tr('USER ALREADY MEMBER')
				progdlg.addDetails(details)
				
				progdlg.setProgress(progress)
				progress+=1
				qApp.processEvents()
				
			# Remove groups
			for idx in xrange(self.lb_remove.count()):
				rmgroup = str(self.lb_remove.text(idx).utf8())
				details = self.tr('Removing user "%1" from the group "%2" ... ').arg(uid).arg(QString.fromUtf8(rmgroup))			
				res = self.soapproxy.groupdel(uid,rmgroup)
				if res==1:			
					details += self.tr('USER REMOVED')
				if res==-3:
					details += self.tr('USER NOT MEMBER')	
				progdlg.addDetails(details)			
				progdlg.setProgress(progress)
				progress+=1
				qApp.processEvents()

		progdlg.setLabelText(self.tr("Done."))
		progdlg.setProgress(progdlg.steps)
		progdlg.exec_loop()
		glob_settings.setWidgetGeometry('skolesys-ui/AddRemoveUserGroups/ProgressDlg',progdlg)
		show_details = 0
		if progdlg.btn_details.isOn():
			show_details = 1
		glob_settings.setIntEntry('skolesys-ui/AddRemoveUserGroups/ProgressDlg/show_details',show_details)		
		return True
