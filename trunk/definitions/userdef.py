# User types
TEACHER = 1
STUDENT = 2
PARENT = 3
OTHER = 4


def check_usertype_text(usertype_text):
	global TEACHER,STUDENT,PARENT,OTHER
	usertype_text = usertype_text.strip().lower()
	if usertype_text == 'teacher':
		return TEACHER
	if usertype_text == 'student':
		return STUDENT
	if usertype_text == 'parent':
		return PARENT
	if usertype_text == 'other':
		return OTHER
	return None


def translate_usertype_id(usertype_id):
	global TEACHER,STUDENT,PARENT,OTHER
	if usertype_id == TEACHER:
		return 'teacher'
	if usertype_id == STUDENT:
		return 'student'
	if usertype_id == PARENT:
		return 'parent'
	if usertype_id == OTHER:
		return 'other'
	return None
