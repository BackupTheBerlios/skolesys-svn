import sys
from qt import *
from addremovewdgbase import AddRemoveWdgBase
from usermanagerwdg import *
from progressdlg import ProgressDlg
from settings import glob_settings

class AddRemoveGroupUsersWdg(AddRemoveWdgBase):
	"""
	Create and destroy user/group memberships from the group managers
	point of view. Thus a range of groups have been selected and now we want
	to add and remove user connections.
	"""
	def __init__(self,conn,groupnames,parent = None,name = None,fl = 0):
		AddRemoveWdgBase.__init__(self,parent,name,fl)
		self.um_wdg = UserManagerWdg(conn,self,"lb_users")
		self.um_wdg.contextmenu_enabled = False
		self.mainlayout.addMultiCellWidget(self.um_wdg,1,8,0,0)
		self.groupnames = groupnames
		
		# Populate the subjects listbox
		for groupname in groupnames:
			self.lb_subjects.insertItem(QString.fromUtf8(groupname))
		
		self.conn = conn # For passing on to create/remove groups
		self.soapproxy = conn.get_proxy_handle()
		self.connect(self.btn_add_add,SIGNAL("clicked()"),self.addToAddClicked)
		self.connect(self.btn_add_remove,SIGNAL("clicked()"),self.addToRemoveClicked)
		
	def languageChange(self):
		self.setCaption(self.tr("Form1"))
		self.remove_label.setText(self.tr("Remove"))
		self.add_label.setText(self.tr("Add"))
	
	def addToListbox(self,lb_addbox,lb_ctrlbox):
		uids = self.um_wdg.selectedUids()
		comparemode = Qt.CaseSensitive | Qt.ExactMatch
		for uid in uids:
			
			# Add the groupname if not present
			item = lb_addbox.findItem(uid,comparemode)
			if not item:
				lb_addbox.insertItem(uid)
			
			# Remove the groupname from the other box if it is present
			item = lb_ctrlbox.findItem(uid,comparemode)
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
		progdlg.setTotalSteps(len(self.groupnames)*(self.lb_add.count()+self.lb_remove.count())-1)

		glob_settings.widgetGeometry('skolesys-ui/AddRemoveGroupUsers/ProgressDlg',progdlg)
		progdlg.show()
		show_details = glob_settings.intEntry('skolesys-ui/AddRemoveGroupUsers/ProgressDlg/show_details',0)[0]
		progdlg.showDetails(show_details)
		progress = 0
		for groupname in self.groupnames:
			# Add groups
			progdlg.setLabelText(self.tr("Altering memberships of %1").arg(QString.fromUtf8(groupname)))
			for idx in xrange(self.lb_add.count()):
				adduid = str(self.lb_add.text(idx))
				details = self.tr('Adding user "%1" to the group "%2" ... ').arg(adduid).arg(QString.fromUtf8(groupname))
				res = self.soapproxy.groupadd(adduid,groupname)
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
				rmuid = str(self.lb_remove.text(idx))
				details = self.tr('Removing user "%1" from the group "%2" ... ').arg(rmuid).arg(QString.fromUtf8(groupname))
				res = self.soapproxy.groupdel(rmuid,groupname)
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
		glob_settings.setWidgetGeometry('skolesys-ui/AddRemoveGroupUsers/ProgressDlg',progdlg)
		show_details = 0
		if progdlg.btn_details.isOn():
			show_details = 1
		glob_settings.setIntEntry('skolesys-ui/AddRemoveGroupUsers/ProgressDlg/show_details',show_details)
		return True
