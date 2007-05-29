import os.path

def path_to(project_path):
	basepath = os.path.split(__file__)[0]
	return '%s/%s' % (basepath,project_path)
