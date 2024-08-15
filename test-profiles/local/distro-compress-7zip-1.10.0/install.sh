#!/bin/sh
cd ~
echo "#!/bin/sh
7zz b > \$LOG_FILE 2>&1
echo \$? > ~/test-exit-status" >  distro-compress-7zip
chmod +x  distro-compress-7zip
