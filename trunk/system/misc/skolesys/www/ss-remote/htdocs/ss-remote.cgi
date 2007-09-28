#!/usr/bin/python

import os,mimetypes,cgi,gettext
from skolesys.tools.lang import tr
from skolesys.lib.conf import conf
import skolesys.lib.usermanager as userman

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

um=userman.UserManager()
userinfo = um.list_users(usertype=None,uid=username)
if userinfo and userinfo.has_key(username) and userinfo[username].has_key('displayName'):
	print '<h1>Velkommen %s</h1>' % userinfo[username]['displayName']

if error:
	print error

platforms = ['win32']
plat_files = {'win32' : 'ss-remote.exe'}

for platform in list(platforms):
	if not os.path.exists('/skolesys/www/ss-remote/userclients/%s/%s/%s' % (os.environ['REMOTE_USER'],platform,plat_files[platform])):
		platforms.remove(platform)

if len(platforms):
	print "<b>%s</b>" % translate('clients_available')
	print "<br>"
	print "<table>"
	for platform in platforms:
		print '<tr valign="top">'
		print '<td><a href="ss-remote.cgi?action=fetch_%s_client">%s</a></td>' % (platform,plat_files[platform])
		print '<td>%s</td>' % translate('%s_client_desc' % platform)
		print '</tr>'
	print "</table><br>"
else:
	print "<b>%s</b><br>" % translate('no_clients_available')

print translate('download_oneshot_info')
print "<br><br><b>%s:</b>" % translate('important')
print translate('possible_security_breech')
