#!/bin/sh
unzip -o jpeg-test-1.zip
echo $? > ~/install-exit-status
cd ~
echo "#!/bin/sh
/usr/bin/tjbench jpeg-test-1.JPG -benchtime 20 -warmup 5 -nowrite > \$LOG_FILE
echo \$? > ~/test-exit-status" > tjbench
chmod +x tjbench
