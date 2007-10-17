#! /usr/bin/python

# This file is part of the SkoleSYS libraries
# Copyright (C) 2007 Jakob Simon-Gaarde <info at skolesys.dk>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License version 2 as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public License
# along with this library; see the file COPYING.LIB.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301, USA.

__author__ = "Jakob Simon-Gaarde <jakob@skolesys.dk>"

import os,re
from conf import conf
import skolesys.tools.log as log

#-------------------------------------
#--------------- Hooks ---------------

class Hooks:
	"""
	SkoleSYS Developer:
	------------------
	The Hooks class is a simple yet effective way for adding an end-user (administrator) interface
	to SkoleSYS core events. So if a SkoleSYS developer wants to add the possibilty to hook into
	some event he/she will use the Hooks.fetch_hooks() method to retrieve whatever hooks are added
	for the given event and the call them one by one.
	The mechanism is file based and uses the api_method argument to resolve a list of folders to
	search through for files:
	1. Calculate a list of hook base-dirs (default: /etc/skolesys/hooks) but more base-paths can
	   be added in skolesys.conf (section "DOMAIN" variable "hooks_path")
	2. calculate the hook sub-dirs using the api_method argument. This will normally correspond
	   to the given core event. ie. api_method="lib.usermanager.changeuser", this argument will
	   resolv to the subdir: lib/usermanager/changeuser
	3. run through the files in the base-dirs/subdir parsing them for the function "hook".
	
	example:
		if for a certain installation there is the configuration
		hook_path=/etc/skolesys/hooks:/skolesys/freeschool.dk/hooks
		and Hooks.fetch_hooks('lib.groupmanager.creategroup') is called, then the
		searchdirs will be as follows:
			
			/etc/skolesys/hooks/lib/groupmanager/greategroup
			/skolesys/freeschool.dk/hooks/lib/groupmanager/greategroup
			
		the method will return a list of functions if any were found by the name "hook" in
		the files contained in the searchdirs.
	
	SkoleSYS school administrator:
	-----------------------------
	To add a hook to the core-event lib.usermanager.createuser, place a python script in 
	/etc/skolesys/hooks/lib/usermanager/createuser and implement the function "hook" that takes
	keyword arguments.
	
	example:
		The hook that adds all new users to a SQL database could look something like this:
		
		file: /etc/skolesys/hooks/lib/usermanager/createuser/db_add
		
		import pysqlite2.dbapi2 as pysqlite
		def hook(**args):
			con = pysqlite.connect("db_file"
			cur = con.cursor())
			cursor.execute('insert into user values (:uid,:uidNumber, ... )',args)
			...
	"""	
	
	def __init__(self):
		"""
		Initialize Hooks finding all valid hook base-dirs.
		"""
		path_list = []
		if conf.has_option('DOMAIN','hooks_path'):
			path_list = conf.get('DOMAIN','hooks_path').split(':')
		path_list += ['/etc/skolesys/hooks']
		path_distinct = {}
		for path in path_list:
			if os.path.exists(path):
				path_distinct[path] = 1
		self.path = path_distinct.keys()


	def fetch_hooks(self,api_method):
		"""
		Fetch a list of hook functions for a certain api method.
		"""
		rx_sep=re.compile('[\./]')
		parts = rx_sep.split(api_method)
		hooks = {}
		# loop hook paths
		for p in self.path:
			hook_path = os.path.join(p,os.path.join(*parts))
			if os.path.exists(hook_path):
				# the api_path has a corresponding hook dir run through the files
				for f in os.listdir(hook_path):
					# parse the hook file
					hookfile = os.path.join(hook_path,f)
					try:
						hookfile = os.path.join(hook_path,f)
						exec(open(os.path.join(hook_path,f)).read())
					except Exception, e:
						log.write('Failed to parse "%s": %s' % (f,e),context="skolesys-hooks")
						continue
					
					# Check for required hook function
					if locals().has_key('hook'):
						# add the hook to the list of hooks
						hooks[hookfile] = hook
						# remove the hook func from locals
						locals().pop('hook')
		return hooks
	
	
	def call_hooks(self,api_method,**args):
		hooks = self.fetch_hooks(api_method)
		for f,h in hooks.items():
			try:
				h(**args)
			except Exception, e:
				log.write('Failed while executing "%s": %s' % (f,e),context="skolesys-hooks")
				continue
