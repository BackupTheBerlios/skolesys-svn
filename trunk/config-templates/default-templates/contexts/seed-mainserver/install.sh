#!/bin/sh
ss_installer mod_apt_sources cf_install
ss_installer install_packages cf_install
ss_installer copy_files cf_install
ss_installer set_hostname cf_install
ss_installer run_script -i /bin/sh init_firestarter
ss_installer kick_daemons cf_install
ss_installer mod_fstab cf_install
