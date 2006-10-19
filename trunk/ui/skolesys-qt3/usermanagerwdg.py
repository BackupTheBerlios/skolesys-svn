import sys
from qt import *
from usermanagerwdgbase import UserManagerWdgBase
import skolesys.definitions.userdef as userdef
import skolesys.tools.schooltime as stime
import launcher,config

columns = {'username':0,'usertype':1,'login':2}
def col_map_name(col):
	for (k,v) in columns.items():
		if v==col:
			return k
	return None

class UserListViewItem(QListViewItem):
	def __init__(self,parent,username,usertype,login):
		QListViewItem.__init__(self,parent)
		self.username=username
		self.usertype=usertype
		self.login=login

	def text(self,col):
		colname = col_map_name(col)
		if (colname =='username'):
			return self.username
		elif (colname =='usertype'):
			return self.usertype
		elif (colname =='login'):
			return self.login
		return ''

class UserManagerWdg(UserManagerWdgBase):
	def __init__(self,conn,parent = None,name = None,fl = 0):
		self.classyear_filter_enabled = False
		self.group_filter_enabled = False
		self.group_members = []
		UserManagerWdgBase.__init__(self,parent,name,fl)
		self.m_lv_userlist.addColumn(self.tr("Name"))
		self.m_lv_userlist.addColumn(self.tr("Type"))
		self.m_lv_userlist.addColumn(self.tr("Login"))
		
		self.conn = conn # For passing on to create/remove users
		self.soapproxy = conn.get_proxy_handle()
		self.userlist = []
		self.update_list()
		self.contextmenu_enabled = True

		# setup usertype combo
		setupdict = {}
		self.typedict = {}
		for type_text in userdef.list_types_by_text():
			self.typedict[self.tr(type_text).latin1()] = userdef.usertype_as_id(type_text)
			setupdict[type_text] = self.tr(type_text).latin1()

		self.typedict[self.tr('all').latin1()] = None
		setupdict['all'] = self.tr('all').latin1()
		self.connect(self.m_cb_usertype_filter,SIGNAL("activated(int)"),self.slot_usertype_changed)
		self.connect(self.cmb_groupfilter,SIGNAL("activated(int)"),self.slot_groupfilter_changed)
		self.connect(self.sbx_firstschoolyear_min,SIGNAL("valueChanged(int)"),self.slot_classyear_span_changed)
		self.connect(self.sbx_firstschoolyear_max,SIGNAL("valueChanged(int)"),self.slot_classyear_span_changed)
		
		typeorder = ['all'] + config.usertype_order
		for usertype_text in typeorder:
			if setupdict.has_key(usertype_text):
				self.m_cb_usertype_filter.insertItem(setupdict[usertype_text])
		
		# Setup group combo
		self.groups_to_combo()
	
	def groups_to_combo(self):
		# Setup group combo
		self.all_groups = self.soapproxy.list_groups(None)
		self.cmb_groupfilter.clear()
		self.cmb_groupfilter.insertItem(self.tr('All'))
		groupnames = self.all_groups.keys()
		groupnames.sort()
		for group in groupnames:
			self.cmb_groupfilter.insertItem(QString.fromUtf8(group))

	def slot_groupfilter_changed(self):
		groupname = str(self.cmb_groupfilter.currentText().utf8())
		self.group_filter_enabled = False
		if not self.all_groups.has_key(groupname) or self.cmb_groupfilter.currentItem()==0:
			self.group_filter_enabled = False
			usertype_id = self.typedict[self.m_cb_usertype_filter.currentText().latin1()]
			self.update_list(usertype_id)
			return
		self.group_filter_enabled = True
		self.group_members = self.soapproxy.list_members(groupname)
		usertype_id = self.typedict[self.m_cb_usertype_filter.currentText().latin1()]
		self.update_list(usertype_id)
		

	def slot_classyear_span_changed(self,idx):
		usertype_id = self.typedict[self.m_cb_usertype_filter.currentText().latin1()]
		self.update_list(usertype_id)

	def slot_usertype_changed(self,idx):
		self.classyear_filter_enabled = False
		usertype_id = self.typedict[self.m_cb_usertype_filter.currentText().latin1()]
		if usertype_id==userdef.usertype_as_id('student'):
			self.classyear_filter_enabled = True
			self.lbl_firstschoolyear_to.setEnabled(True)
			self.sbx_firstschoolyear_min.setEnabled(True)
			self.sbx_firstschoolyear_max.setEnabled(True)
		else:
			self.lbl_firstschoolyear_to.setEnabled(False)
			self.sbx_firstschoolyear_min.setEnabled(False)
			self.sbx_firstschoolyear_max.setEnabled(False)
		
		self.update_list(usertype_id)
	
	def update_list(self,usertype=None):
		userlist = self.soapproxy.list_users(usertype)
		self.m_lv_userlist.clear()
		self.userlist = []
		
		for user in userlist.keys():
			name = QString.fromUtf8(userlist[user]['cn'])
			usertype = qApp.translate("UserTypes",userlist[user]['title'])

			# Filter by classyear (aargang)
			min_classyear = self.sbx_firstschoolyear_min.value()
			max_classyear = self.sbx_firstschoolyear_max.value()
			if self.classyear_filter_enabled and userlist[user].has_key('firstSchoolYear'):
				classyear = stime.firstyear_to_classyear(int(userlist[user]['firstSchoolYear']))
				if classyear < min_classyear or classyear > max_classyear:
					continue
					
			# filter by group
			if self.group_filter_enabled and not self.group_members.count(user):
				continue
			
			self.userlist+=[UserListViewItem(self.m_lv_userlist,name,usertype,user)]
	
	def createUser(self):
		launcher.execCreateUser(self.conn)
		self.update_list()

	def selectedUids(self):
		uids = []
		item = self.m_lv_userlist.firstChild()
		while item:
			if item.isSelected():
				uids += [item.login]
			item = item.itemBelow()
		return uids
	
	def removeUser(self):
		uids = self.selectedUids()
		launcher.execRemoveUser(self.conn,uids)
		self.update_list()
		return

	def slotContextMenuRequested(self):
			uids = self.selectedUids()
			item = self.m_lv_userlist.currentItem()
			if len(uids) and self.contextmenu_enabled:
					ctxmenu = QPopupMenu(self,"userManagerContextMenu")
					edit_memberships = ctxmenu.insertItem(self.tr("Edit group memberships..."))
					if item:
							edit_current = ctxmenu.insertItem(self.tr("Edit %1...").arg(item.username))
					ctxmenu.insertSeparator()
					remove_users = ctxmenu.insertItem(self.tr("Remove user(s)..."))
					res = ctxmenu.exec_loop(QCursor.pos())
					if res == edit_memberships:
							launcher.execAddRemoveUserGroups(self.conn,uids)

