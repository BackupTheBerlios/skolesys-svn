iso_base = "kubuntu-6.06.1-desktop-i386.iso"

inst_manifest_excludes = \
"""^ubiquity
^.*lang.*-zh
^.*lang.*-nl
^.*lang.*-de
^.*lang.*-fr
^grub
^qtparted
^libdebian-installer
^libdebconfclient
^kubuntu-live
^user-setup"""

version = '0.7'
volume_id = 'SkoleSYS_<ver>.9'

diskname = 'SkoleSYS <ver>.9 LTSP "Pilot" - Release i386'

iso_product = 'skolesys-<ver>.9-ltsp-i386.iso'


post_extract_script = """
rm livecd/programs -R -f
rm livecd/start.*
rm livecd/autorun.inf
"""

chroot_script = """
export SKOLESYS_REP=http://skolesys.dk/testing
export HOME=/tmp
export LANG=C

wget $SKOLESYS_REP/skolesys.gpg.asc
gpg --import skolesys.gpg.asc
gpg --armor --export EEF2B7FA | apt-key add -
echo "deb $SKOLESYS_REP pilot main" >> /etc/apt/sources.list
echo "deb $SKOLESYS_REP pilot nonfree" >> /etc/apt/sources.list
echo "deb http://dk.archive.ubuntu.com/ubuntu/ dapper universe" >> /etc/apt/sources.list
apt-get update
apt-get install python2.4-skolesys-seeder
"""
