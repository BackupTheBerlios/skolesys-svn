# User types
_user_struct = {}

# NOTE: types are canse in-sensetive!
_user_struct['type_id'] = {
	1 : 'teacher',
	2 : 'student',
	3 : 'parent',
	4 : 'other'}
	
_user_struct['type_text'] = {}
for k,v in _user_struct['type_id'].items():
	exec('%s=%d' % (v.upper(),k))
	_user_struct['type_text'][v.lower()] = k


def usertype_as_id(usertype):
	"""
	Convert a user type id (sanity check) or user type text to it's user type id.
	If an int is passed it is regarded as a user type id itself and therefore normally
	just returned as is, but if the value is not valid None is returned.
	"""
	if type(usertype)==str:
		if _user_struct['type_text'].has_key(usertype.strip().lower()):
			return _user_struct['type_text'][usertype.strip().lower()]
	elif type(usertype) == int:
		if _user_struct['type_id'].has_key(usertype):
			return usertype
	else:
		return None

def usertype_as_text(usertype):
	"""
	Convert a user type id or user type text (sanity check) to it's user type text.
	If a str is passed it is regarded as a user type text itself and therefore normally
	just returned as is, but if the value is not valid None is returned.
	"""
	if type(usertype)==str:
		if _user_struct['type_text'].has_key(usertype.strip().lower()):
			return usertype.strip().lower()
	elif type(usertype) == int:
		if _user_struct['type_id'].has_key(usertype):
			return _user_struct['type_id'][usertype]
	else:
		return None

def list_types_by_id():
	return _user_struct['type_id'].keys()

def list_types_by_text():
	return _user_struct['type_text'].keys()


