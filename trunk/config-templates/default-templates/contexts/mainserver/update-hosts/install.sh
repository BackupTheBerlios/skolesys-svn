#!/bin/sh

if ! ss_installer copy_files cf_install
then
	echo "ss_installer failed to copy configuration files"
	exit 1
fi

if ! ss_installer kick_daemons cf_install
then
	echo "ss_installer failed kick daemons"
	exit 1
fi

exit 0
