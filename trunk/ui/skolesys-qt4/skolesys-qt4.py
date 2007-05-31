#!/usr/bin/python
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

