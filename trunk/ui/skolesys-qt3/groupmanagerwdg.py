import sys
from qt import *
from groupmanagerwdgbase import GroupManagerWdgBase
import skolesys.definitions.userdef as userdef
import launcher

columns = {'groupname':0,'usertype':1}
def col_map_name(col):
	for (k,v) in columns.items():
		if v==col:
			return k
	return None

class GroupListViewItem(QListViewItem):
	def __init__(self,parent,groupname,usertype):
		QListViewItem.__init__(self,parent)
		self.groupname=groupname
		self.usertype=usertype

	def text(self,col):
		colname = col_map_name(col)
		if (colname =='groupname'):
			return self.groupname
		elif (colname =='usertype'):
			return self.usertype
		return ''

class GroupManagerWdg(GroupManagerWdgBase):
	def __init__(self,conn,parent = None,name = None,fl = 0):
		GroupManagerWdgBase.__init__(self,parent,name,fl)
		self.m_lv_grouplist.addColumn(self.tr("Name"))
		self.m_lv_grouplist.addColumn(self.tr("Type"))
		
		self.conn = conn # For passing on to create/remove groups
		self.soapproxy = conn.get_proxy_handle()
		self.grouplist = []
		self.update_list()
		self.contextmenu_enabled = True

		self.typedict={self.tr('All').latin1():None,
			self.tr('Teachers').latin1():userdef.usertype_as_id('teacher'),\
			self.tr('Students').latin1():userdef.usertype_as_id('student'),\
			self.tr('Parents').latin1():userdef.usertype_as_id('parent'),\
			self.tr('Others').latin1():userdef.usertype_as_id('other')}
		
		order = [self.tr('All').latin1(),self.tr('Teachers').latin1(),\
			self.tr('Students').latin1(),self.tr('Parents').latin1(),self.tr('Others').latin1()]
		for usertype in order:
			self.m_cb_usertype_filter.insertItem(usertype)
		
	def slotFilterActivated(self,idx):
		self.update_list(self.typedict[self.m_cb_usertype_filter.currentText().latin1()])
	
	def update_list(self,usertype=None):
		grouplist = self.soapproxy.list_groups(usertype)
		self.m_lv_grouplist.clear()
		self.grouplist = []
		for group in grouplist.keys():
			name = QString.fromUtf8(grouplist[group]['cn'])
			desc = ''
			if grouplist[group].has_key('description'):
				desc = QString.fromUtf8(grouplist[group]['description'])
			self.grouplist+=[GroupListViewItem(self.m_lv_grouplist,name,desc)]
	
	def createGroup(self):
		launcher.execCreateGroup(self.conn)
		self.update_list()

	def selectedGroupnames(self):
		groupnames = []
		item = self.m_lv_grouplist.firstChild()
		while item:
			if item.isSelected():
				groupnames += [str(item.groupname.utf8())]
			item = item.itemBelow()	
		return groupnames
	
	def removeGroup(self):
		groupnames = self.selectedGroupnames()
		launcher.execRemoveGroup(self.conn,groupnames)
		self.update_list()
		return
	
	def slotContextMenuRequested(self):
		groupnames = self.selectedGroupnames()
		if len(groupnames) and self.contextmenu_enabled:
			ctxmenu = QPopupMenu(self,"userManagerContextMenu")
			edit_memberships = ctxmenu.insertItem(self.tr("Edit user memberships..."))
			ctxmenu.insertSeparator()
			remove_groups = ctxmenu.insertItem(self.tr("Remove group(s)..."))
			res = ctxmenu.exec_loop(QCursor.pos())
			if res == edit_memberships:
				launcher.execAddRemoveGroupUsers(self.conn,groupnames)
	
