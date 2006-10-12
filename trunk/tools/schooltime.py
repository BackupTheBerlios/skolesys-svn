import time

def firstyear_to_classyear(year):
	now = time.localtime()
	if now[7]>=195:
		return now[0]-year
	else:
		return now[0]-year-1
