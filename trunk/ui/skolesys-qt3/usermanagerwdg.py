import sys
from qt import *
from usermanagerwdgbase import UserManagerWdgBase
from lin4schools.soap.client import L4S_Client
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

	def update_list(self,usertype=None):
		userlist = self.soapproxy.list_users(usertype)
		self.m_lv_userlist.clear()
		self.userlist = []
		for user in userlist.keys():
			name = QString.fromUtf8(userlist[user]['cn'])
			self.userlist+=[UserListViewItem(self.m_lv_userlist,name,'Todo!',user)]
	
	def createUser(self):
		launcher.execCreateUser(self.conn)
		self.update_list()

	def removeUser(self):
		launcher.execRemoveUser(self.conn)

