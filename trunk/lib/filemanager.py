from conf import conf
import os,sys,re

class FileManager:
	def find(self,user=None,group=None,minsize=None,regex=None,only_files=True,order=''):
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


	def removefiles(self,file_list):
		for f in file_list:
			if os.path.exists(f):
				os.system('rm "%s" -Rf' % f)

	



if __name__=='__main__':
	fm = FileManager()
	for f in fm.find(minsize=80000,order='filename,size'):
		print f['filename'],f['size']

	fm.removefiles(['/home/admin/svn-commit.4.tmp','/home/admin/svn-commit.3.tmp'])

