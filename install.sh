#!/bin/sh

for package in `cat dependencies.txt`; do 
    DEBIAN_FRONTEND=noninteractive sudo apt-get install -y ${package}
done

./pts/phoronix-test-suite list-available-tests
cp -r ubuntu-pts-selection/*.xml ~/.phoronix-test-suite/test-suites/local/
cp -r ubuntu-pts-selection/test-profiles/* ~/.phoronix-test-suite/test-profiles/
cp ./config/user-config.xml ~/.phoronix-test-suite/

