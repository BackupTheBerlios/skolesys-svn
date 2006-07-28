import sys
from qt import *
import inspect

CustomButton1 = 1
CustomButton2 = 2

class WidgetDialog(QDialog):
	def __init__(self,parent=None,name=None,buttons=0,custombuttons_left=1,cancel_btn=True,modal=0,fl=0):
		QDialog.__init__(self,parent,name,modal,fl)
		self.widget = None
		if not name:
			self.setName( "TRDialog" )
		self.dlg_layout = QVBoxLayout( self, 11, 6, "TRDialogLayout")
		self.layout1 = QHBoxLayout( None, 0, 6, "layout1")

		spacer1 = QSpacerItem( 181, 20, QSizePolicy.Expanding, QSizePolicy.Minimum )
		if not custombuttons_left:
			self.layout1.addItem( spacer1 )

		if buttons & CustomButton1:
			self.btnCustom1 = QPushButton( self, "m_btnCustom1" )
			self.layout1.addWidget( self.btnCustom1 )
		
		if buttons & CustomButton2:
			self.btnCustom2 = QPushButton( self, "m_btnCustom2" )
			self.layout1.addWidget( self.btnCustom2 )
		
		if custombuttons_left:
			self.layout1.addItem( spacer1 )

		self.spacer1 = QSpacerItem( 181, 20, QSizePolicy.Expanding, QSizePolicy.Minimum )
		self.btnOK = QPushButton( self, "m_btnOK" )
		self.layout1.addWidget( self.btnOK )
		self.connect( self.btnOK, SIGNAL( "clicked()" ), self, SLOT( "accept()" ) )

		self.cancel_btn = cancel_btn
		if cancel_btn:
			self.btnCancel = QPushButton( self, "m_btnCancel" )
			self.layout1.addWidget( self.btnCancel )
			self.connect(self.btnCancel, SIGNAL( "clicked()" ), self, SLOT( "reject()" ) )

		self.languageChange()
	
		r = self.layout1.geometry()
		r.moveBy(-100,-100)
		self.layout1.setGeometry(r)
		self.resize( QSize(385, 419).expandedTo(self.minimumSizeHint()) )
		self.clearWState( Qt.WState_Polished )

	def languageChange(self):
		self.setCaption( self.tr( "TRDialog" ) )
		if self.cancel_btn:
			self.btnCancel.setText( self.tr( "&Cancel" ) )
			self.btnCancel.setAccel( QKeySequence( self.tr( "Alt+C" ) ) )
		self.btnOK.setText( self.tr( "&OK" ) )
		self.btnOK.setAccel( QKeySequence( self.tr( "Alt+O" ) ) )

	def setWidget(self,widget,embedInGroupbox=False,groupBoxTitle="",margin=6,buttonsEnabled=True):
		meta_parent = self
		meta_layout = self.dlg_layout
		self.dlg_layout.setMargin(margin)

		if widget and embedInGroupbox:
			self.groupBox = QGroupBox( self, "groupBox" )
			self.groupBox.setGeometry( QRect( 20, 20, 190, 143 ) )
			self.groupBox.setColumnLayout(0, Qt.Vertical )
			self.groupBox.layout().setSpacing( 6 )
			self.groupBox.layout().setMargin( 6 )
			self.groupBoxLayout = QVBoxLayout( self.groupBox.layout() )
			self.groupBoxLayout.setAlignment( Qt.AlignTop )
			self.groupBox.setTitle(groupBoxTitle)
			self.dlg_layout.addWidget(self.groupBox)
			
			meta_parent = self.groupBox
			meta_layout = self.groupBoxLayout
			widget.setFocus()
		
		if widget:
			widget.reparent(meta_parent,QPoint(0,0))
			widget.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.MinimumExpanding)
			#TRDialogLayout->insertWidget(0,widget,1,Qt::AlignTop);
			widgetLay = widget.layout();
			if widgetLay:
				widgetLay.setResizeMode(QLayout.Minimum);
			
			self.widget = widget
			meta_layout.addWidget( widget )
			
			#self.dlg_layout.addLayout(m_foldedExtensionLayout);
			
			if buttonsEnabled:
				self.dlg_layout.addLayout( self.layout1 )
			widget.setFocus()
	
	def accept(self):
		if self.widget:
			try:
				inspect.ismethod(self.widget.accept)
				if self.widget.accept():
					QDialog.accept(self)
				else:
					return
			except Exception, e:
				print e
				pass
		QDialog.accept(self)

	def reject(self):
		if self.widget:
			try:
				inspect.ismethod(self.widget.reject)
				if self.widget.reject():
					QDialog.reject(self)
				else:
					return
			except:
					pass
		QDialog.reject(self)
	
if __name__=="__main__":
	# Test
	a = QApplication(sys.argv)
	QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
	w = WidgetDialog()
	w.setWidget(QFileDialog())
	a.setMainWidget(w)
	w.show()
	a.exec_loop()	
	a=WidgetDialog()
