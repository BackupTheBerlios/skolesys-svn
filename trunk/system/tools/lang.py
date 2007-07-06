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

import gettext,os

translators = {}

def tr(domain,msg,lang=None):
	"""
	tr is the base translation function that can fetch the translation
	from any domain on any language. It is a simple lazy implementaion
	that stores the translation objects per domain/lang as they are used.
	This makes the tr function ideal in persistent applications, so the
	language files do not need to be parsed again and again.
	"""
	global translators

	if lang==None:
		# If language isn't passed to the function
		lang = 'en' # safe fallback
		if os.getuid()==0:
			# if root then use lang defined in skolesys.conf 
			from skolesys.lib.conf import conf
			lang = conf.get('OPTIONS','default_lang')
		elif os.environ.has_key('LANG'):
			# Else use the environment
			lang = os.environ['LANG']
		print lang
	if not translators.has_key((domain,lang)):
		try:
			translators[(domain,lang)] = gettext.translation(domain, languages=[lang])
		except IOError,e:
			return msg+"*"
	gnu_trans = translators[(domain,lang)]
	
	return gnu_trans.gettext(msg)

