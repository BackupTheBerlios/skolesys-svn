from launchdlgbase import LaunchDlgBase
from launcher import *
from imageloader import load_pixmap
class LaunchDlg(LaunchDlgBase):
	def __init__(self,conn,parent=None,name=None,modal=1,fl=0):
		LaunchDlgBase.__init__(self,parent,name,modal,fl)
		self.lbl_logo.setPixmap(load_pixmap('logo_small.png'))
		self.conn = conn
		
	def userManager(self):
		execUserManager(self.conn)

	def groupManager(self):
		execGroupManager(self.conn)
