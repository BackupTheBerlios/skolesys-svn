from launchdlgbase import LaunchDlgBase
from launcher import *
import os.path

class LaunchDlg(LaunchDlgBase):
	def __init__(self,conn,parent=None,name=None,modal=1,fl=0):
		LaunchDlgBase.__init__(self,parent,name,modal,fl)
		basepath = os.path.split(__file__)[0]
		logo = QPixmap('%s/logo_small.png' % basepath)
		self.lbl_logo.setPixmap(logo)
		self.conn = conn
		
	def userManager(self):
		execUserManager(self.conn)

	def groupManager(self):
		execGroupManager(self.conn)
