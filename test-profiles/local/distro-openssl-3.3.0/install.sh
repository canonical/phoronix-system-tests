#!/bin/sh

cd ~
echo "#!/bin/sh
cd openssl-3.3.0
LD_LIBRARY_PATH=.:\$LD_LIBRARY_PATH /usr/bin/openssl speed -multi \$NUM_CPU_CORES -seconds 30 \$@ > \$LOG_FILE 2>&1
echo \$? > ~/test-exit-status" > openssl
chmod +x openssl
