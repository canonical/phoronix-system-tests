#!/bin/sh

for package in `cat dependencies.txt`; do 
    DEBIAN_FRONTEND=noninteractive sudo apt-get install -y ${package}
done


#git submodule init
#git submodule update --recursive

./pts/phoronix-test-suite list-available-tests
cp -r alltests ~/.phoronix-test-suite/test-suites/local/
cp -r test-profiles/* ~/.phoronix-test-suite/test-profiles/
cp ./config/user-config.xml ~/.phoronix-test-suite/


echo !!!add deb-src to the apt sources!!!
