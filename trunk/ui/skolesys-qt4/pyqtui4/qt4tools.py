from PyQt4 import QtSvg,QtGui,QtCore

def svg2pixmap(svgpath,pix_size_x,pix_size_y,outfile=None,format=None):
	pix=QtGui.QPixmap(pix_size_x,pix_size_y)
	pix.fill(QtCore.Qt.white)
	pix2=QtGui.QPixmap(pix_size_x,pix_size_y)
	pix2.fill(QtCore.Qt.black)
	pix.setAlphaChannel(pix2)
	painter = QtGui.QPainter(pix)
	from PyQt4 import QtSvg
	svg=QtSvg.QSvgRenderer(svgpath)
	svg.render(painter)
	del svg
	if outfile and format:
		pix.save(outfile,format)
	return pix