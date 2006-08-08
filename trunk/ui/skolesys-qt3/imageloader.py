from qt import *
import os.path

def load_pixmap(filename):
	basepath = os.path.split(__file__)[0]
	if os.path.exists('%s/art/%s' % (basepath,filename)):
		return QPixmap('%s/art/%s' % (basepath,filename))
	else:
		return None
