import skolesys,inspect,os
import groupserviceinterface as gsi
import userserviceinterface as usi

location = "%s/services" % os.path.split(inspect.getsourcefile(skolesys))[0]
files = os.listdir(location)
exports = []
services = None
for f in files:
	if os.path.isdir("%s/%s" % (location,f)) and f!='.svn':
		exports += [f]

del files
del f

__all__ = [exports]

def _get_exports_list(module):
    try:
        return list(module.__all__)
    except AttributeError:
        return [n for n in dir(module) if n[0] != '_']

# inspect the available services 
def _inspect_services():
	global services
	if services==None:
		services = {'groupservices':[],'userservices':[]}
		for i in exports:
			service_mod = 'skolesys.services.%s.interface' % i
			__import__(service_mod, globals(),locals(),['ServiceInterface'])
			try:
				mod = __import__(service_mod, globals(),locals(),['ServiceInterface'])
			except Exception, e:
				print e,
				print '- %s could not be loaded' % service_mod
				continue
		
			if not dir(mod).count('ServiceInterface'):
				print '%s lacks the ServiceInterface class' % service_mod
		
			classes = inspect.getmro(mod.ServiceInterface)
			for cls in classes:
				if cls==gsi.GroupServiceInterface:
					services['groupservices'] += [i]
				elif cls==usi.UserServiceInterface:
					services['userservices'] += [i]
	return services
	

def create_groupserviceinterface(servicename,groupname):
	if not groupservices().count(servicename):
		print 'The group service "%s" does not exist.' % servicename
		return None
	try:
		service_mod = 'skolesys.services.%s.interface' % servicename
		mod = __import__(service_mod, globals(),locals(),['ServiceInterface'])
		return mod.ServiceInterface(groupname)
	except Exception, e:
		print e,
		print '- Group service interface for "%s" could not be instantiated' % servicename
		return None
	
def create_userserviceinterface(servicename,username,groupname=None):
	if not userservices().count(servicename):
		print 'The user service "%s" does not exist.' % servicename
		return None
	try:
		service_mod = 'skolesys.services.%s.interface' % servicename
		mod = __import__(service_mod, globals(),locals(),['ServiceInterface'])
		return mod.ServiceInterface(username,groupname)
	except Exception, e:
		print e,
		print '- User service interface for "%s" could not be instantiated' % servicename
		return None


def groupservices():
	return _inspect_services()['groupservices']
		

def userservices():
	return _inspect_services()['userservices']
