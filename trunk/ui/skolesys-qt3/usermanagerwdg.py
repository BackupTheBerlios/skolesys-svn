import sys
from qt import *
from usermanagerwdgbase import UserManagerWdgBase
from skolesys.soap.client import SkoleSYS_Client
import launcher

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
		UserManagerWdgBase.__init__(self,parent,name,fl)
		self.m_lv_userlist.addColumn(self.tr("Name"))
		self.m_lv_userlist.addColumn(self.tr("Type"))
		self.m_lv_userlist.addColumn(self.tr("Login"))
		
		self.conn = conn # For passing on to create/remove users
		self.soapproxy = conn.get_proxy_handle()
		self.userlist = []
		self.update_list()
		self.contextmenu_enabled = True

		self.typedict={self.tr('All').latin1():None,
			self.tr('Teachers').latin1():1,\
			self.tr('Students').latin1():2,\
			self.tr('Parents').latin1():3,\
			self.tr('Others').latin1():4}
		
		order = [self.tr('All').latin1(),self.tr('Teachers').latin1(),\
			self.tr('Students').latin1(),self.tr('Parents').latin1(),self.tr('Others').latin1()]
		for usertype in order:
			self.m_cb_usertype_filter.insertItem(usertype)
		
	def slotFilterActivated(self,idx):
		self.update_list(self.typedict[self.m_cb_usertype_filter.currentText().latin1()])
	
	def update_list(self,usertype=None):
		userlist = self.soapproxy.list_users(usertype)
		self.m_lv_userlist.clear()
		self.userlist = []
		for user in userlist.keys():
			name = QString.fromUtf8(userlist[user]['cn'])
			usertype = qApp.translate("UserTypes",userlist[user]['title'])
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
		if len(uids) and self.contextmenu_enabled:
			ctxmenu = QPopupMenu(self,"userManagerContextMenu")
			edit_memberships = ctxmenu.insertItem(self.tr("Edit group memberships..."))
			ctxmenu.insertSeparator()
			remove_users = ctxmenu.insertItem(self.tr("Remove user(s)..."))
			res = ctxmenu.exec_loop(QCursor.pos())
			if res == edit_memberships:
				launcher.execAddRemoveUserGroups(self.conn,uids)
			
