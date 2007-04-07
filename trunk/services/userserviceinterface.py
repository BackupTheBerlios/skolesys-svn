import optionmanager as om

class UserServiceInterface(om.OptionManager):

	def __init__(self,servicename,username,groupname):
		om.OptionManager.__init__(self,servicename,username,groupname)

	def hook_attachservice(self):
		pass

	def hook_detachservice(self):
		pass

	def invalidate(self):
		pass

	def restart(self):
		pass
