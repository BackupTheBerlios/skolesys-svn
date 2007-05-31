'''
This file is part of the SkoleSYS libraries
Copyright (C) 2007 Jakob Simon-Gaarde <info at skolesys.dk>

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Library General Public
License version 2 as published by the Free Software Foundation.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Library General Public License for more details.

You should have received a copy of the GNU Library General Public License
along with this library; see the file COPYING.LIB.  If not, write to
the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
Boston, MA 02110-1301, USA.
'''

'''
This file is part of the SkoleSYS libraries
Copyright (C) 2007 Jakob Simon-Gaarde <info at skolesys.dk>

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Library General Public
License version 2 as published by the Free Software Foundation.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Library General Public License for more details.

You should have received a copy of the GNU Library General Public License
along with this library; see the file COPYING.LIB.  If not, write to
the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
Boston, MA 02110-1301, USA.
'''
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
