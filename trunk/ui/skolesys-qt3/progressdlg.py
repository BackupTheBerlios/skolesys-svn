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
