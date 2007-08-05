#! /usr/bin/python

# Prerequisites
import sys,os
if not os.environ.has_key('DEVNAME'):
	sys.exit(0)
devname = os.environ['DEVNAME']

# Presets
log_enabled = True

action = os.environ['ACTION']

mnt_point = None
import ConfigParser,re,syslog


def log(txt,force=False):
	global log,log_enabled
	if not log_enabled and not force:
		return
	syslog.openlog('skolesys-backup')
	syslog.syslog(txt)
	syslog.closelog()
	
props = {}
def reset_partition_props():
	global props
	props = {'PARTNO' : '1',
		'MNT_POINT' : None,
		'ADD_SCRIPT' : None,
		'ADD_SCRIPT_NOTIFY': None,
		'ADD_SCRIPT_SUBJECT': 'ADD_SCRIPT Notifier',
		'ADD_SCRIPT_BODYFILE': None,
		'ADD_SCRIPT_SENDER': 'anonymous@domain.org',
		'REMOVE_SCRIPT' : None,
		'REMOVE_SCRIPT_NOTIFY': None,
		'REMOVE_SCRIPT_SUBJECT': 'REMOVE_SCRIPT Notifier',
		'REMOVE_SCRIPT_BODYFILE': None,
		'REMOVE_SCRIPT_SENDER': 'anonymous@domain.org' }

conf = ConfigParser.ConfigParser()
conf.read('/home/skolesys/backup.conf')
sections = conf.sections()

rx_partno = re.compile('.*([0-9]+)')

for sec in sections:
	go = True
	reset_partition_props()
	for k,v in conf.items(sec):
		k=k.upper()
		if props.has_key(k):
			props[k] = v
			continue
		log("trying (%s = %s)" % (k,v))
		if not os.environ.has_key(k):
			go = False
			break
		if not os.environ[k] == v:
			go = False
			break
	if not go:
		continue
		
	m = rx_partno.match(devname)
	if not m or not m.groups()[0]==props['PARTNO']:
		log('Right device wrong partition (%s)' % devname)
		go = False

	if go:
		log('%s drive, Action: %s...' % (sec,action),True)
		log('Partition no. = %s (%s)' % (props['PARTNO'],devname))
		if action=='add':
			mnt_point = props['MNT_POINT']
			if props['MNT_POINT']:
				log('Mounting to %s' % mnt_point)
				if not os.path.exists(mnt_point):
					os.makedirs(mnt_point)
				os.system('mount %s %s' % (devname,mnt_point))
			
			if props['ADD_SCRIPT']:
				log('Starting script: %s' % props['ADD_SCRIPT'])
				res = os.system(props['ADD_SCRIPT'])
				log('Script exited with %d' % res)

				if props['ADD_SCRIPT_NOTIFY']:
					log('Notifying: %s' % props['ADD_SCRIPT_NOTIFY'] )
					f = open('/tmp/add_script_notification','w')
					f.write('From: %s\n' % props['ADD_SCRIPT_SENDER'])
					f.write('Subject: %s\n' % props['ADD_SCRIPT_SUBJECT'])
					f.write('To: %s\n\n' % props['ADD_SCRIPT_NOTIFY'])
					if props['ADD_SCRIPT_BODYFILE']:
						bodyfile = props['ADD_SCRIPT_BODYFILE']
						if os.path.exists(bodyfile):
							f2 = open(bodyfile)
							f.writelines(f2.readlines())
							f2.close()
					f.close()
					os.system('sendmail -t < /tmp/add_script_notification')
					os.remove('/tmp/add_script_notification')
					

		if action=='remove':
			if props['MNT_POINT']:
				log('Unmounting %s' % devname)
				os.system('umount %s' % props['MNT_POINT'])

			if props['REMOVE_SCRIPT']:
				log('Starting script %s' % props['REMOVE_SCRIPT'])
				res = os.system(props['REMOVE_SCRIPT'])
				log('Script exited with %d' % res)

				if props['REMOVE_SCRIPT_NOTIFY']:
					f = open('/tmp/remove_script_notification','w')
					f.write('From: %s\n' % props['REMOVE_SCRIPT_SENDER'])
					f.write('Subject: %s\n' % props['REMOVE_SCRIPT_SUBJECT'])
					f.write('To: %s\n\n' % props['REMOVE_SCRIPT_NOTIFY'])
					if props['REMOVE_SCRIPT_BODYFILE']:
						bodyfile = props['REMOVE_SCRIPT_BODYFILE']
						if os.path.exists(bodyfile):
							f2 = open(bodyfile)
							f.writelines(f2.readlines())
							f2.close()
					f.close()
					os.system('sendmail -t < /tmp/remove_script_notification')
					os.remove('/tmp/remove_script_notification')
