import os

def get_dist_codename():
	w,r = os.popen2('lsb_release -cs')
	dist_codename = r.readline().strip()
	r.close()
	w.close()
	return dist_codename
