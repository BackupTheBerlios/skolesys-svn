import os


for f in os.listdir('.'):
	parts = f.split('.')
	if parts[-1:][0]=='ui':
		print parts[0],parts[1]
		os.system('pyuic -o %s.py %s' % (parts[0],f))
