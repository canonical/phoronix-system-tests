#!/bin/sh

DEBIAN_FRONTEND=noninteractive sudo apt-get -y install povray

echo $? > ~/install-exit-status

cd ~
echo "#!/bin/sh
echo 1 | /usr/bin/povray -benchmark > \$LOG_FILE 2>&1
echo \$? > ~/test-exit-status" > povray
chmod +x povray
