#!/usr/bin/python
import os
files = os.listdir('.')
for f in files:
	fparts = f.split('.')
	if fparts[-1:][0].lower()=='ui':
		os.system('pyuic4 %s > %s.py' % (f,'.'.join(fparts[:-1])))