#!/bin/sh
ss_installer mod_apt_sources cf_ltsp
ss_installer install_packages cf_ltsp
ss_installer copy_files cf_ltsp
ss_installer kick_daemons cf_ltsp
ss_installer mod_fstab cf_ltsp
