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

from PyQt4 import QtCore, QtGui
import connectionmanager as cm
import servermessages as servermsg


def access_denied_dialog(access_ident):
	qmsg = servermsg.get_translator().q_tr('access','%s_infinitive' % access_ident)
	res = QtGui.QMessageBox.information(
		None,QtCore.QCoreApplication.translate("AccessTools","Access denied"),
		QtCore.QCoreApplication.translate("AccessTools","You do not have access to %1.").arg(qmsg.toLower()))

def check_permission(access_ident,show_message=True):
	access = cm.get_proxy_handle().check_my_permission(access_ident)
	if access:
		return True
	else:
		if show_message:
			access_denied_dialog(access_ident)
		return False


def check_permission_multi_or(access_idents,show_message=True):
	if not len(access_idents):
		return True
	proxy = cm.get_proxy_handle()
	my_access = proxy.list_my_permissions()
	sufficient = False
	for acc_ident in access_idents:
		if my_access.count(acc_ident):
			sufficient = True
			break
	if not sufficient:
		if show_message:
			access_denied_dialog(access_idents[0])
	return sufficient

def check_permission_multi_and(access_idents,show_message=True):
	proxy = cm.get_proxy_handle()
	my_access = proxy.list_my_permissions()
	sufficient = True
	for acc_ident in access_idents:
		if not my_access.count(acc_ident):
			sufficient = False
			break
	if not sufficient:
		if show_message:
			access_denied_dialog(acc_ident)
	return sufficient
