#!/bin/sh
cd ~
echo "#!/bin/sh
7zz b > \$LOG_FILE 2>&1
echo \$? > ~/test-exit-status" > compress-7zip
chmod +x compress-7zip
