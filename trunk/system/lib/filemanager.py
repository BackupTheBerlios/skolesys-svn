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

from conf import conf
import os,sys,re,time,threading,pwd,grp
import statmon.statmon_sync as statmon_sync
import pysqlite2.dbapi2 as pysqlite

_ONE_DAY_IN_SECONDS = 86400

class FileManager:
	def __init__(self,db_file,paths,fs_encodings,sync_hours=[0,10,12,14,16,18,20,22]):
		"""
		Create a FileManager object. 
		@type	db_file: string
		@param	db_file: Path to the sqlite db where file stat info should be stored
		@type	paths: [string]
		@param	paths: Paths to be monitored through periodical synchronizations
		@type	fs_encodings: [string]
		@param	fs_encodings: The possible charactor encodings used in filenames of the given paths
		@type	sync_hours: [numbers]
		@param	sync_hours: The hours to start the synchronization job (24 hour clock values)
		"""
		self.timer = None
		self.thread_lock = threading.Lock()
		self.db_file = db_file
		self.sync_hours = sync_hours
		self.sync_hours.sort()
		self.paths = paths
		self.fs_encodings = fs_encodings
		self.synchronize()
		self._reset_timer()

	def __del__(self):
		if self.timer:
			self.timer.cancel()

	def _reset_timer(self):
		"""
		Reset the timer for next synchronization.
		"""
		cur_time = time.localtime()
		cur_ctime = time.mktime(cur_time)

		next_sync_hour = None
		add_day = 0
		for i in self.sync_hours:
			if i>cur_time[3] and i<24:
				next_sync_hour = i
				break
		if next_sync_hour==None:
			next_sync_hour = self.sync_hours[0]
			if next_sync_hour>23:
				next_sync_hour = 0
			add_day = 1

		next_sync = cur_time[:3]+(next_sync_hour,0,0)+cur_time[-3:]
		next_ctime = time.mktime(next_sync) + (add_day * _ONE_DAY_IN_SECONDS)
		remaining_seconds = next_ctime - time.mktime(time.localtime())
		self.timer = threading.Timer(remaining_seconds,self._timeout,[])
		self.timer.start()

	def _timeout(self):
		self.synchronize()
		self._reset_timer()
		
	def synchronize(self):
		self.thread_lock.acquire()
		try:
			# We must catch errors in order to release the lock
			statmon_sync.updatedb(self.paths,self.db_file,self.fs_encodings,False)
		except:
			pass
		self.thread_lock.release()

	def find_old(self,user=None,group=None,minsize=None,regex=None,only_files=True,order=''):
		regexopt,useropt,groupopt,typeopt,sizeopt = '','','','',''
		if only_files:
			typeopt = '-type f'
		if group!=None:
			groupopt = '-group "%s"' % group
		if user!=None:
			useropt = '-user "%s"' % user
		if minsize!=None:
			if type(minsize) == int:
				sizeopt = "-size +%dc" % minsize
			else:
				sizeopt = "-size +%s" % minsize
		if regex!=None:
			regexopt = '-regex "%s"' % regex
	
		cmd = "find %s/%s -regextype posix-extended %s %s %s %s %s -printf '%%u\\t%%g\\t%%h\\t%%f\\t%%m\\t%%s\\n'" % \
			(conf.get('DOMAIN','domain_root'),conf.get('DOMAIN','domain_name'),regexopt,useropt,groupopt,typeopt,sizeopt)
		r = os.popen(cmd)
		
		lines = r.readlines()
		
		sort_machine = []
		for l in lines:
			u,g,d,f,p,s = l.strip().split('\t')
			s=int(s)
			info_dict = {'user':u,'group':g,'dirname':d,'filename':f,'permissions':p,'size':s}
			sort_list = []
			for val in order.split(','):
				if info_dict.has_key(val):
					if type(info_dict[val])==str:
						sort_list += [info_dict[val].lower()]
					else:
						sort_list += [info_dict[val]]
			sort_machine += [[sort_list,info_dict]]
		sort_machine.sort()
		
		filelist = []
		for f in sort_machine:
			filelist += [f[1]]
		return filelist


	def make_where_clause(self,user=None,group=None,minsize=None,extensions=None,regex=None,only_files=True,order='')
		regexopt,useropt,groupopt,typeopt,sizeopt = '','','','',''
		#if only_files:
		#	typeopt = '-type f'
		
		stmt = []		
		clause_list = []

		user_dict = {}
		group_dict = {}
		if group!=None:
			try:
				clause_list += [ 'f.gid=%d' % grp.getgrnam(group)[2] ]
				g = grp.getgrnam(group)
				group_dict[g[0]] = g[2]
				group_dict[g[2]] = g[0]
			except:
				clause_list += [ 'f.gid=-1' ]
		else:
			all_groups = grp.getgrall()
			for g in all_groups:
				group_dict[g[0]] = g[2]
				group_dict[g[2]] = g[0]


		if user!=None:
			try:
				clause_list += [ 'f.uid=%d' % pwd.getpwnam(user)[2] ]
				u = pwd.getpwnam(user)
				user_dict[u[0]] = u[2]
				user_dict[u[2]] = u[0]
			except:
				clause_list += [ 'f.uid=-1' ]
		else:
			all_users = pwd.getpwall()
			for u in all_users:
				user_dict[u[0]] = u[2]
				user_dict[u[2]] = u[0]

		if minsize!=None:
			if type(minsize) == int:
				clause_list += ['size>%d'%minsize]
			else:
				clause_list += ['size>%s'%minsize]

		if extensions!=None:
			clause_list += ["(name like '%." + "' or name like '%.".join(extensions) + "')"]
			
		return clause_list


	def count(self,user=None,group=None,minsize=None,extensions=None,regex=None,only_files=True,order=''):
		"""
		Fetch the amount of files matching a certain filter. Result is returned as an int >=0 if 
		the task is successful or -1 if something failed.
		@type	user: string
		@param	user: Only look at files owned by this user
		@type	group: string
		@param	group: Only look at files belonging to this group
		@type	minsize: int
		@param	minsize: Only include files larger than this value in bytes
		@type	extensions: list
		@param	extensions: Include files having one of following extensions
		"""
		clause_list = self.make_where_clause(user,group,minsize,extensions,regex,only_files,order)
		stmt = ["select count(*) from file f, directory d where f.dir_md5sum=d.md5sum"]
		if len(clause_list)>0:
			stmt += [' and '.join(clause_list)]
		
		stmt = ' and '.join(stmt)

		filecount = -1
		self.thread_lock.acquire()
		try:
			# We must catch errors in order to release the lock
			con = pysqlite.connect(self.db_file)
			cur = con.cursor()
			cur.execute(stmt)

			res = cur.fetchone()
			if len(res):
				filecount = res[0]
		except:
			pass

		self.thread_lock.release()		
		return filecount
	

	def find(self,user=None,group=None,minsize=None,extensions=None,regex=None,only_files=True,order=''):
		"""
		Fetch a list of files matching a certain filter with stat info. Result is returned as a
		list of dictionaries.
		@type	user: string
		@param	user: Only look at files owned by this user
		@type	group: string
		@param	group: Only look at files belonging to this group
		@type	minsize: int
		@param	minsize: Only include files larger than this value in bytes
		@type	extensions: list
		@param	extensions: Include files having one of following extensions
		clause_list = self.make_where_clause(user,group,minsize,extensions,regex,only_files,order)
		stmt = ["select f.uid,f.gid,d.path,f.name,'na',f.size from file f, directory d where f.dir_md5sum=d.md5sum"]
		"""
		if len(clause_list)>0:
			stmt += [' and '.join(clause_list)]
		
		stmt = ' and '.join(stmt)

		filelist = []
		self.thread_lock.acquire()
		try:
			# We must catch errors in order to release the lock
			con = pysqlite.connect(self.db_file)
			cur = con.cursor()
			cur.execute(stmt)

			sort_machine = []
			res = cur.fetchmany(1000)
			while res:
				for row in res:
					try:
						uname = user_dict[row[0]]
					except:
						uname = str(row[0])
					try:
						gname = group_dict[row[1]]
					except:
						gname = str(row[1])
					info_dict = {
						'user':uname,
						'group':gname,
						'dirname':row[2],
						'filename':row[3],
						'permissions':row[4],
						'size':row[5]}
					sort_list = []
					for val in order.split(','):
						if info_dict.has_key(val):
							if type(info_dict[val])==str:
								sort_list += [info_dict[val].lower()]
							else:
								sort_list += [info_dict[val]]
					sort_machine += [[sort_list,info_dict]]

				res = cur.fetchmany(1000)
			sort_machine.sort()
			
			filelist = []
			for f in sort_machine:
				filelist += [f[1]]
		except:
			pass

		self.thread_lock.release()		
		return filelist


	def removefiles(self,file_list):
		for f in file_list:
			if os.path.exists(f):
				os.system('rm "%s" -Rf' % f)

	



if __name__=='__main__':
	fm = FileManager()
	for f in fm.find(minsize=80000,order='filename,size'):
		print f['filename'],f['size']

	fm.removefiles(['/home/admin/svn-commit.4.tmp','/home/admin/svn-commit.3.tmp'])

