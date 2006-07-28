from launchdlgbase import LaunchDlgBase
from launcher import *

class LaunchDlg(LaunchDlgBase):
	def __init__(self,conn,parent=None,name=None,modal=1,fl=0):
		LaunchDlgBase.__init__(self,parent,name,modal,fl)
		self.conn = conn
		
	def userManager(self):
		execUserManager(self.conn)

	def groupManager(self):
		execGroupManager(self.conn)
