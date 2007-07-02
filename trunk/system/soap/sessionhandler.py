import threading

class SessionHandler:
	
	def __init__(self,def_timeout=0):
		self.sessions = {}
		self.def_timeout = def_timeout
		
		
	def remove_session(self,session_id):
		if self.sessions.has_key(session_id):
			if self.sessions[session_id].has_key('timer'):
				self.sessions[session_id]['timer'].cancel()
				del self.sessions[session_id]['timer']
			del self.sessions[session_id]
			print 'Session "%s" killed' % str(session_id)
		
		
	def create_session(self, session_id, timeout=None):
		
		# check if the session_id already exists
		if self.session_exists(session_id):
			return False
		
		self.sessions[session_id] = {'session_id': session_id}
		return self.set_session_timeout(session_id,timeout)
	
	
	def set_session_timeout(self,session_id,timeout):
		
		if not self.sessions.has_key(session_id):
			return False
		
		if self.sessions[session_id].has_key('timer'):
			self.sessions[session_id]['timer'].cancel()
			del self.sessions[session_id]['timer']
			
		# Resolve the session timeout value
		if timeout == None:
			timeout = self.def_timeout
			
		# create the session dictionary
		self.sessions[session_id]['timeout'] = timeout

		if timeout != 0 and timeout != None:
			timer = threading.Timer(timeout,self.remove_session,[session_id])
			self.sessions[session_id]['timer'] = timer
			timer.start()
		
		return True

	
	def session_exists(self,session_id):
		
		try:
			if not self.sessions.has_key(session_id):
				return False
			
			timeout = self.sessions[session_id]['timeout']
			self.set_session_timeout(session_id,timeout)
			return True
		except:
			return False


	def has_session_variable(self,session_id,variable):
		if not self.session_exists(session_id):
			return False
		
		# Set the session variable
		if self.sessions[session_id].has_key(variable):
			return True


	def set_session_variable(self,session_id,variable,value):
		if not self.session_exists(session_id):
			return False

		# Set the session variable
		self.sessions[session_id][variable] = value
		
		return True


	def get_session_variable(self,session_id,variable):
		if not self.session_exists(session_id):
			return False, None
		
		# Set the session variable
		if self.sessions[session_id].has_key(variable):
			return True, self.sessions[session_id][variable]
		
		return False, None

	
	def unset_session_variable(self,session_id,variable):
		if not self.session_exists(session_id):
			return False
		
		# Set the session variable
		if self.sessions[session_id].has_key(variable):
			del self.sessions[session_id][variable]
			return True

