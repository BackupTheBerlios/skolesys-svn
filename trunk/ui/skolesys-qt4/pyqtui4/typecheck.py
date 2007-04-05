import inspect

def check_inheritance(obj,class_list):
	if not type(class_list)==list and \
		not type(class_list)==tuple:
		print "check_inheritance: The class_list type is invalid"
		return False
	
	cls_list = list(class_list)
	classes = list(inspect.getmro(type(obj)))
	for cls in cls_list:
		if not classes.count(cls):
			print "check_inheritance: The type %s is not in the class hierarchi of %s" % (cls,obj)
			return False
	return True