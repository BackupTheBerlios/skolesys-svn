class ActionRequester:
	
	def __init__(self):
		self.connections = {}
		self.toggle_action_connections = {}
		self.disable_list = []

	
	def addConnection(self,action,slot,toggle_action=False, toggle_state=False):
		if not toggle_action:
			self.connections[action] = slot
		else:
			self.toggle_action_connections[action] = [slot,toggle_state]

	def actionConnections(self):
		return self.connections
	
	def toggleActionConnections(self):
		return self.toggle_action_connections
	
	def disableList(self):
		return self.disable_list
	
	def setActionEnabled(self,action,enable=True):
		self.disable_list.remove(action)
		action.setEnabled(enable)
		if not enable:
			self.disable_list += [action]
