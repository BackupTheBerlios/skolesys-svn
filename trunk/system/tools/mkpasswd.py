'''
 This module depends on python >= 2.3

 Module written by Bjorn Ove Grotan <bgrotan@grotan.com>

  mkpasswd is free software; you can redistribute it and/or modify it
  under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.
 
  mkpasswd is distributed in the hope that it will be useful, but
  WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
  General Public License for more details.
 
  You should have received a copy of the GNU General Public License
  along with mkpasswd; if not, write to the Free Software Foundation,
  Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

 For extra strength passwords, we wanted SSHA in our LDAP-environment
 as the standard python-module 'sha' does not support ssha, but this can 
 easily be implemented with a few extra functions. 

 SSHA can be described as:
     the SHA1-digest of a password with a sequence of "salt" bytes, where
     the bytes are randomly chosen - followed by the same salt bytes
 For LDAP-use, the SHA1 and SSHA-digest has to be base64-encoded. 

 Example-LDIF:
     {SSHA}oaEG3PJ10sHxGcSxsDRRooTifL55/2NOdN3nU1VEV+NFzc9Q
 
 This package should now support passwords compatible with [1] Samba using the [2]
 smbpasswd module for [3] Python. The samba compability is added for use with Samba 
 as PDC with storing user and host-information in LDAP.

 [1] http://www.samba.org
 [2] http://barryp.org/software/py-smbpasswd/
 [3] http://www.python.org
'''
import string,base64
import random,sys
import exceptions
import md5,sha,crypt
import re,binascii
smb = 0 # Where 1 is true, and 0 is false
debug = False

try:
	import smbpasswd
	smb = 1 
except:
	smb = 0
	if debug:
		print '''
		module <smbpasswd> not found or not installed. Windows-passwords are therefor
		not supported!
		'''

def getsalt(chars = string.letters + string.digits,length=16):
	''' Generate a random salt. Default length is 16 '''
	salt = ''
	for i in range(int(length)):
		salt += random.choice(chars)
	return salt

def randpasswd(chars = string.digits + string.ascii_letters,length=8):
	''' Returns a random password at a given length based on a character-set.'''
	result = ''
	for i in range(length):
		result = result + getsalt(chars,1)
	return result

def check_password(s):
	''' Returns true or false if the argument is concidered a strong password.
		The password must meat certain rules.. like:
		both small and CAPITALIZED characters, numbers and special characters 
		such as .,/!"# etc
	'''
	return True

def validate_passwd(hash,passwd):
	''' Return True or False on wether passwd validates correctly to the
		hash given.'''
	rx_typematch = re.compile("^\{(\S+)\}(.+)$")
	m = rx_typematch.match(hash)
	if not m:
		sys.stderr.write('The recieved hash "%s" is invalid - should have format "{TYPE}hashdata"\n' % hash)
		return False

	if not m.groups()[0].upper() == 'SSHA':
		sys.stderr.write('Only SSHA hashes are accepted - The recieved one is "%s"\n' % m.groups()[0].upper())
		return False

	ohash = m.groups()[1]
	ohash = ohash.decode('base64')

	osalt = ohash[20:]
	ohash = ohash[:20]

	odigest = sha.new(passwd+osalt).hexdigest()

	nhash = binascii.unhexlify(odigest)

	if ohash == nhash:
		return True

	return False


def mkpasswd(pwd,sambaver=3,default='ssha'):
	''' Make a given password cryptated, possibly with different 
		crypt-algorihtms. This module was written for use with 
		LDAP - so default is seeded sha
	'''
	alg = {
		'ssha':'Seeded SHA',
		'sha':'Secure Hash Algorithm',
		'md5':'MD5',
		'smd5':'Seeded MD5',
		'crypt':'standard unix crypt'
	}
	if smb:
		alg['lmhash'] = 'lan man hash'
		alg['nthash'] = 'nt hash'
	if default not in alg.keys():
		return 'algorithm <%s> not supported in this version.' % default
	else:
		salt = getsalt()
		if default == 'ssha':
			return "{SSHA}" + base64.encodestring(sha.new(str(pwd) + salt).digest() + salt)
		elif default =='sha':
			return "{SHA}" + base64.encodestring(sha.new(str(pwd)).digest())
		elif default =='md5':
			return "{MD5}" + base64.encodestring(md5.new(str(pwd)).digest())
		elif default == 'smd5':
			return "{SMD5}" + base64.encodestring(md5.new(str(pwd) + salt).digest() + salt)
		elif default =='crypt':
			return "{CRYPT}" + crypt.crypt(str(pwd),getsalt(length=2)) # crypt only uses a salt of length 2
		elif default == 'lmhash':
			if sambaver==3:
				return "{sambaLMPassword}" + smbpasswd.lmhash(pwd)
			elif sambaver==2:
				return "{lmPassword}" + smbpasswd.lmhash(pwd)
		elif default == 'nthash':
			if sambaver==3:
				return "{sambaNTPassword}" + smbpasswd.lmhash(pwd)
			elif sambaver==2:
				return "{NTPassword}" + smbpasswd.lmhash(pwd)

def check_strength(passwordString=""):
	
	def check_length():
		return 13 * pLength
		
	def check_chars():
		upperBool = False
		lowerBool = False
		specialBool = False
		numberBool = False
		combination = 0
		
		valueDict = {0:50, 1:50, 2:20, 3:0, 4:0}
		
		for x in passwordString:
			if (not lowerBool) and (x in string.ascii_lowercase):
				lowerBool = True
				combination += 1
			if (not upperBool) and (x in string.ascii_uppercase):
				upperBool = True
				combination += 1
			if (not numberBool) and (x in string.digits):
				numberBool = True
				combination += 1
			if (not specialBool) and ((x in string.punctuation) \
					and (not(x in string.ascii_uppercase)) \
					and (not(x in string.ascii_lowercase)) \
					and (not(x in string.digits))):
				specialBool = True
				combination += 1
			if upperBool and lowerBool and specialBool and numberBool:
				break
		
		#print passwordString, combination, upperBool, lowerBool, numberBool, specialBool
		return valueDict[combination]
		
		
	def check_distribution():
		tmpDict = {}
		for x in passwordString:
			tmpDict[x] = None
		
		ratio = pLength / len(tmpDict.keys())
		#if 1 == ratio:
		#    return 0
		return 13 * (ratio-1)
		
	def check_special_characters():
		tmpVal = 0
		return tmpVal
	
	pLength = len(passwordString)
	
	value = check_length()
	#print "Length: ", value
	value -= check_distribution()
	#print "Distribution: ", value
	value -= check_chars()
	#print "Chars: ", value
	
	if value < 0:
		value = 0
	
	if value > 100:
		value = 100
		
	return value


def check_strength_function():

	pwList = ["a", "aA", "aaaaaaaaaaa", "abcdefgh", "aBcDeFgH", "abc123ef",
		"aBc123Ef", "      ", "abC12 \ *+"]
		
	for x in pwList:
		print x, check_strength(x)
		
	
