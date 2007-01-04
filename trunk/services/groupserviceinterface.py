import optionmanager as om

class GroupServiceInterface(om.OptionManager):

	def __init__(self,servicename,groupname):
		om.OptionManager.__init__(self,servicename,None,groupname)

	def hook_attachservice(self,uidnumbers):
		pass

	def hook_detachservice(self,uidnumbers):
		pass

	def hook_groupadd(self,uidnumber):
		pass

	def hook_groupdel(self,uidnumber):
		pass

