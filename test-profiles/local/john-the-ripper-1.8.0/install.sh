#!/bin/sh
DEBIAN_FRONTEND=noninteractive sudo apt-get -y install john

echo $? > ~/install-exit-status
cd ~/
echo "#!/bin/sh
john \$@ > \$LOG_FILE 2>&1
echo \$? > ~/test-exit-status" > john-the-ripper
chmod +x john-the-ripper
