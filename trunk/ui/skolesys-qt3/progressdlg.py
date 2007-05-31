'''
This file is part of the SkoleSYS libraries
Copyright (C) 2007 Jakob Simon-Gaarde <info at skolesys.dk>

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Library General Public
License version 2 as published by the Free Software Foundation.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Library General Public License for more details.

You should have received a copy of the GNU Library General Public License
along with this library; see the file COPYING.LIB.  If not, write to
the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
Boston, MA 02110-1301, USA.
'''
from qt import *
import sys
from progressdlgbase import ProgressDlgBase

class ProgressDlg(ProgressDlgBase):
	def __init__(self,caption,parent = None,name = None,modal=False):
		ProgressDlgBase.__init__(self,parent,name,modal=modal)
		self.setCaption(caption)
		self.btn_ok.setEnabled(False)
		self.te_details.setShown(False)
		geo = self.geometry()
		geo.setHeight(0)
		geo.setWidth(400)
		self.setTotalSteps(100)
		self.setProgress(100)	
		
	def setTotalSteps(self,steps):
		self.pb_progress_bar.setTotalSteps(steps)
		self.steps=steps
		
	def setProgress(self,prog):
		self.pb_progress_bar.setProgress(prog)
		if prog >= self.steps:
			self.btn_ok.setEnabled(True)
		
	def setLabelText(self,txt):
		self.lb_progress_label.setText(txt)
		
	def addDetails(self,txt):
		self.te_details.append(txt)
		
	def showDetails(self,show):
		if show:
			self.te_details.setShown(True)
			self.btn_details.setState(QButton.On)
		else:
			self.te_details.setShown(False)
			self.btn_details.setState(QButton.Off)
		
		
if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = ProgressDlg()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
