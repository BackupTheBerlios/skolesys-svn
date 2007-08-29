#!/usr/bin/python

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

import os,sys
from optparse import OptionParser

def execute(cmd):
	os.system(cmd)
	#print cmd

def make_root_block(dir):
	if not os.path.isdir(dir):
		return
	if not os.path.exists("%s/.root_block" % dir):
		execute('mkdir %s/.root_block' % dir)
		execute('touch %s/.root_block/.block' % dir)
	execute('chown root.root %s/.root_block -R' % dir)
	execute('chmod u-x,u+Xrw,g-rwx,o-rwx %s/.root_block -R' % dir)

def fix_user_permissions():
	um = userman.UserManager()
	userinfo = um.list_users(None)
	homes_root = "%s/%s/users" % (conf.get('DOMAIN','domain_root'),conf.get('DOMAIN','domain_name'))
	for uid,info in userinfo.items():
		print 'Fixing user permissions for "%s"...' % uid
		gid = int(info['gidNumber'])
		home = "%s/%s" % (homes_root,uid)

		if not os.path.exists(home):
			execute('mkdir %s' % home)
			execute('chown %s.%d %s' % (uid,gid,home))

		documents = "%s/documents" % home
		if not os.path.exists(documents):
			execute('mkdir %s' % documents)
			execute('chown %s.%d %s' % (uid,gid,documents))

		cmd_fix_owner = 'chown %s.%s %s/* -RP' % (uid,gid,documents)
		cmd_fix_perm = 'chmod u-x,u+Xrw,g-rwx,o-rwx %s/* -R' % documents
		execute(cmd_fix_owner)
		execute(cmd_fix_perm)
		make_root_block(documents)
		

def fix_group_permissions():
	gm = groupman.GroupManager()
	groupinfo = gm.list_groups('service')
	groups_root = "%s/%s/groups" % (conf.get('DOMAIN','domain_root'),conf.get('DOMAIN','domain_name'))
	for gid,info in groupinfo.items():
		print 'Fixing group permissions for "%s"...' % gid
		home = "%s/%s" % (groups_root,gid)
		
		if not os.path.exists(home):
			execute('mkdir %s' % home)
			execute('chgrp %s %s -R -f' % (gid,home))
			execute('chmod g+wrs,o-rwx %s -R -f' % home)

		execute('chgrp %s %s -R -f' % (gid,home))
		execute('chmod o-rwx,g-x,g+X,u-x,u+X %s -R -f' % home)


if __name__=='__main__':

	shell_cmd_name = os.path.split(sys.argv[0])[-1:][0]

	# Check root privilegdes
	if not os.getuid()==0:
		print "This command requires root priviledges"
		sys.exit(0)

	from skolesys.lib.conf import conf
	import skolesys.lib.usermanager as userman
	import skolesys.lib.groupmanager as groupman

	parser = OptionParser(usage="usage: %s options" % shell_cmd_name)

	parser.add_option("-g", "--groups",
		action="store_true", dest="groups", default=False,
		help="Update group permissions")

	parser.add_option("-u", "--users",
		action="store_true", dest="users", default=False,
		help="Update user permissions and ownerships")

	parser.add_option("-a", "--all",
		action="store_true", dest="all", default=False,
		help="Update all permissions and ownerships")

	(options, args) = parser.parse_args()

	something_done = False

	if options.groups==True or options.all==True:
		fix_group_permissions()
		something_done = True

	if options.users==True or options.all==True:
		fix_user_permissions()
		something_done = True

	if not something_done:
		#print "No options were given\nUsage: %s" % parser.usage
		parser.print_help()
