from PyQt4 import QtCore, QtGui
import typecheck as tc

class ActionHandler:

	def __init__(self):
		self.actions = {}
		self.action_groups = {}
		self.default_action_group = ""

	def setDefaultActionGroup(self,action_group):
		self.default_action_group = action_group

	def addAction(self,action_key,action_text,pixmap=None,reciever_slot=None,action_group=None,accel=None,checkable=None):
		new_action = QtGui.QAction( action_key,self )
		new_action.setText(action_text)
		
		if pixmap:
			new_action.setIcon(QtGui.QIcon(pixmap))
		
		if accel:
			new_action.setShortcut(accel)
			
		if not checkable == None:
			new_action.setCheckable(checkable)
			
		if reciever_slot:
			if checkable:
				QtCore.QObject.connect(new_action,QtCore.SIGNAL( "toggled(bool)" ),reciever_slot)
			else:
				QtCore.QObject.connect(new_action,QtCore.SIGNAL( "triggered()" ),reciever_slot)
			
		self.actions[action_key] = new_action
		
		if not action_group:
			action_group = self.default_action_group
		if not self.action_groups.has_key(action_group):
			self.action_groups[action_group] = []
		self.action_groups[action_group] += [action_key]
		return new_action

	def action(self,action_key):
		if self.actions.has_key(action_key):
			return self.actions[action_key]
		return None
	
	def actionKeys(self,action_group=None):
		if action_group == None:
			return self.actions.keys()
		else:
			if self.action_groups.has_key(action_group):
				return self.action_groups[action_group]
	
	def actionGroups(self):
		return self.action_groups.keys()
	
	def installConnectionMap(self,action_requester):
		# Check param type must inherit ActionRequester and QObject
		import actionrequester as ar
		
		if not tc.check_inheritance(action_requester,(QtCore.QObject,ar.ActionRequester)):
			print "Wrong type sent to ActionHandler.installConnectionMap"
			return False
		
		con_map = action_requester.actionConnections()
		for action,slot in con_map.items():
			action.setEnabled(True)
			action.setCheckable(False)
			QtCore.QObject.connect(action,QtCore.SIGNAL("triggered()"),slot)

		toggle_con_map = action_requester.toggleActionConnections()
		for action,slot_and_state in toggle_con_map.items():
			action.setEnabled(True)
			action.setCheckable(True)
			action.setChecked(slot_and_state[1])
			QtCore.QObject.connect(action,QtCore.SIGNAL("toggled(bool)"),slot_and_state[0])
			
		for pre_disable in action_requester.disableList():
			pre_disable.setEnabled(False)
		return True

  	def uninstallConnectionMap(self,action_requester):
		# Check param type must inherit ActionRequester and QObject
		import actionrequester as ar
		if not tc.check_inheritance(action_requester,(QtCore.QObject,ar.ActionRequester)):
			print "Wrong type sent to ActionHandler.installConnectionMap"
			return False
		
		con_map = action_requester.actionConnections()
		for action,slot in con_map.items():
			action.setEnabled(False)
			action.setCheckable(False)
			QtCore.QObject.disconnect(action,QtCore.SIGNAL("triggered()"),slot)
			
		toggle_con_map = action_requester.toggleActionConnections()
		for action,slot_and_state in toggle_con_map.items():
			slot_and_state[1] = action.isChecked()
			action.setEnabled(False)
			action.setCheckable(False)
			QtCore.QObject.disconnect(action,QtCore.SIGNAL("toggled(bool)"),slot_and_state[0])
