#!/bin/sh
cd ~/
echo "#!/bin/sh
john \$@ > \$LOG_FILE 2>&1
echo \$? > ~/test-exit-status" > john-the-ripper
chmod +x john-the-ripper
