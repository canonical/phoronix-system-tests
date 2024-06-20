#!/bin/sh
unzip -o jpeg-test-1.zip
tar -xzvf libjpeg-turbo-2.1.0.tar.gz

echo $? > ~/install-exit-status
cd ~
echo "#!/bin/sh
cd libjpeg-turbo-2.1.0/build
/usr/bin/tjbench ../../jpeg-test-1.JPG -benchtime 20 -warmup 5 -nowrite > \$LOG_FILE
echo \$? > ~/test-exit-status" > tjbench
chmod +x tjbench
