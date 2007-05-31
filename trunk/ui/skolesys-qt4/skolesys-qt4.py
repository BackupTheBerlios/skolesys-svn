#!/usr/bin/python
import os,sys
from optparse import OptionParser
from PyQt4 import QtGui,QtCore
import ss_mainwindow as ss_mainwin
import connectionmanager as cm
import paths

parser = OptionParser(usage="%s [options]" % sys.argv[0])
parser.add_option("-l", "--lang", dest="lang",default=None,
	help="Start program with danish languagesettings", metavar="LANG")

(options, args) = parser.parse_args()

if not options.lang:
	options.lang = 'en'

app = QtGui.QApplication(sys.argv)

if options.lang:
	trans = QtCore.QTranslator()
	#print __file__
	#appdir = os.path.split(__file__)[0]
	lang_file = paths.path_to('skolesys-qt4_%s.qm') % (options.lang)
	print lang_file
	loadres = trans.load(lang_file)
	if not loadres:
		print "Failed to load language file: %s" % lang_file
	else:
		app.installTranslator(trans)

cm.setup_connection('https://10.1.0.1',8443)

ui = ss_mainwin.get_mainwindow()

if ui:
	ui.setupViews()

ui.show()
sys.exit(app.exec_())

