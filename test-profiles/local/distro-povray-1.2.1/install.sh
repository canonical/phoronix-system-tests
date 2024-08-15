#!/bin/sh

cd ~
echo "#!/bin/sh
echo 1 | /usr/bin/povray -benchmark > \$LOG_FILE 2>&1
echo \$? > ~/test-exit-status" >  distro-povray
chmod +x  distro-povray
