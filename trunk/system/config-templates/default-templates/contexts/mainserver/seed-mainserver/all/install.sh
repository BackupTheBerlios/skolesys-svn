#!/bin/sh
if ! ss_installer mod_apt_sources cf_install
then
	echo "ss_installer failed to update source.list"
	exit 1
fi

if ! ss_installer install_packages cf_install
then
	echo "ss_installer failed to install packages"
	exit 1
fi

if ! ss_installer copy_files cf_install
then
	echo "ss_installer failed to copy configuration files"
	exit 1
fi

if ! ss_installer set_hostname cf_install
then
	echo "ss_installer failed to set the hostname"
	exit 1
fi

if ! ss_installer run_script -i /bin/sh init_firestarter
then
	echo "ss_installer failed initialize the firewall"
	exit 1
fi

if ! ss_installer kick_daemons cf_install
then
	echo "ss_installer failed kick daemons"
	exit 1
fi

if ! ss_installer mod_fstab cf_install
then
	echo "ss_installer failed update fstab"
	exit 1
fi

if ! ss_installer run_script -i /bin/sh enable_mod_auth_pam 
then
	echo "ss_installer failed to enable apache mod_auth_pam"
	exit 1
fi

exit 0
