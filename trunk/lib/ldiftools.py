from ldif import LDIFParser
from ldaptools import LDAPUtil
import StringIO

class LDIFImporter(LDIFParser):
	def __init__(self, input):
		LDIFParser.__init__(self, input)
		self.imp_data = []

	def handle(self, dn, entry):
		attributes = [ (k,v) for k,v in entry.items() ]
		self.imp_data += [[dn,attributes]]



if __name__=='__main__':
	ldif_test = open('school.template.ldif')
	buf = ldif_test.read()
	buf = buf.replace('<domain_prefix>','refsvindinge')
	buf = buf.replace('<domain_suffix>','dk')
	f=StringIO.StringIO(buf)
	imp = LDIFImporter(f)
	imp.parse()
	
	l = LDAPUtil('ldapserver')
	l.bind('cn=admin,dc=lin4schools,dc=org','bdnprrfe')
	
	for dn,attribs in imp.imp_data:
		print dn,attribs
		l.l.add_s(dn,attribs)
