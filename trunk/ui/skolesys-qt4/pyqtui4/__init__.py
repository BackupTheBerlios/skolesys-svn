import os,inspect

location = os.path.split(__file__)[0]
files = os.listdir(location)
exports = []

for f in files:
	if os.path.isfile("%s/%s" % (location,f)):
		if f.split('.')[-1:][0].lower()=='py' and not f == '__init__.py':
			exports += [f]

del files
del f

__all__ = [exports]

def _get_exports_list(module):
    try:
        return list(module.__all__)
    except AttributeError:
        return [n for n in dir(module) if n[0] != '_']