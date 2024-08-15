#!/bin/sh
cd ~/
echo "#!/bin/sh
john \$@ > \$LOG_FILE 2>&1
echo \$? > ~/test-exit-status" >  distro-john-the-ripper
chmod +x  distro-john-the-ripper
