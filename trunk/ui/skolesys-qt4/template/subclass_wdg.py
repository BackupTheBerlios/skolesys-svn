from PyQt4 import QtCore, QtGui
import ui_<wdg_small_name>wdg as baseui


class <wdg_name>Wdg(QtGui.QWidget, baseui.Ui_<wdg_name>Wdg):
	
	def __init__(self,parent):
		QtGui.QWidget.__init__(self,parent)
		self.setupUi(self)

if __name__ == '__main__':
	import sys
	app = QtGui.QApplication(sys.argv)
	ui = <wdg_name>Wdg(conn,None)
	
	ui.show()
	sys.exit(app.exec_())
