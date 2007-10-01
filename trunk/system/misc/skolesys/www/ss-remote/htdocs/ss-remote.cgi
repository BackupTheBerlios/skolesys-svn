#!/usr/bin/python

import os,mimetypes,cgi,gettext,sys
from skolesys.tools.lang import tr
from skolesys.lib.conf import conf
import skolesys.cfmachine.infocollection as ic
import skolesys.lib.usermanager as userman
from Cheetah.Template import Template

lang = 'en'
if conf.has_option('OPTIONS','default_lang'):
	lang = conf.get('OPTIONS','default_lang')

if os.environ.has_key('HTTP_ACCEPT_LANGUAGE'):
	lang = os.environ['HTTP_ACCEPT_LANGUAGE'].split(',')[0].split(';')[0].split('-')[0]

def translate(msg,as_html=True):
	global lang
	return tr('ss-remote',msg,lang).replace('\n','<br>')

def send_file(path):

	dirname,basename = os.path.split(path)

	print "Content-type: %s" % mimetypes.guess_type(path)[0]
	print 'Content-Disposition: attachment; filename="%s"' % basename
	print 'Content-Length: %d' % os.stat(path)[6]
	
	print
	f = open(path)
	data = f.read()
	f.close()
	os.remove(path)
	print data


username = os.environ['REMOTE_USER']

def send_ss_remote_win32():
	if not os.path.exists('/skolesys/www/ss-remote/userclients/%s/win32/ss-remote.exe' % username):
		return False
	send_file('/skolesys/www/ss-remote/userclients/%s/win32/ss-remote.exe' % username)
	return True

fields = cgi.FieldStorage()
	
error = None

if fields.has_key('action'):
	action = fields['action'].value.lower()
	if fields['action'].value.lower() == 'fetch_win32_client':
		if not send_ss_remote_win32():
			error = translate('win32_na')

print "Content-Type: text/html; charset=UTF-8"
print "\n"

import skolesys.cfmachine.infocollection as ic
ic_inst = ic.InfoCollection()
conf_dict = ic_inst.get_collection()

tmp_platforms = [{'platform': 'win32'}]
platforms = []
plat_files = {'win32' : 'ss-remote.exe'}
plat_icons = {'win32' : 'images/ss-remote-win32.png'}

for platform in list(tmp_platforms):
	if os.path.exists('/skolesys/www/ss-remote/userclients/%s/%s/%s' % (os.environ['REMOTE_USER'],platform['platform'],plat_files[platform['platform']])):
		platforms += [platform]

data = {}
data['conf'] = conf_dict['conf']
data['plat_files'] = plat_files
data['plat_icons'] = plat_icons
data['platforms'] = platforms
data['translate'] = translate

um=userman.UserManager()
userinfo = um.list_users(usertype=None,uid=username)
if userinfo and userinfo.has_key(username) and userinfo[username].has_key('displayName'):
	data['ldap'] = userinfo[username]

if error:
	print error

t = Template(file="templates/index.tmpl",searchList=[data])
print t

