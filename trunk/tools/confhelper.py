from ConfigParser import ConfigParser

def conf2dict(filename,to_lower=True):
	conf_dict = {}
	if os.path.exists(filename):
		conf = ConfigParser()
		f=open(filename)
		conf.readfp()
		f.close()
	sections = conf.sections()
	for sec in sections:
		if to_lower:
			s = sec.lower()
		else
			s = sec
		conf_dict[s] = {}
		for var,val in conf.items(sec):
			if to_lower:
				conf_dict[s][var.lower()] = val
			else:
				conf_dict[s][var] = val
