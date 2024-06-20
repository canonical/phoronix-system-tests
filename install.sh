#!/bin/sh

DEBIAN_FRONTEND=noninteractive sudo apt-get install -y git php-cli php-xml libtiff-tools libjpeg-turbo-progs
DEBIAN_FRONTEND=noninteractive sudo apt-get -y install 7zip-standalone
DEBIAN_FRONTEND=noninteractive sudo apt-get -y install zstd
DEBIAN_FRONTEND=noninteractive sudo apt-get -y install cython3
DEBIAN_FRONTEND=noninteractive sudo apt-get -y install ffmpeg dav1d
DEBIAN_FRONTEND=noninteractive sudo apt-get -y install build-essential dpkg-dev \
    rdfind symlinks gperf systemtap-sdt-dev libaudit-dev libcap-dev binutils-for-host \
    g++-multilib libgd-dev gettext quilt debhelper-compat libselinux1-dev
DEBIAN_FRONTEND=noninteractive sudo apt-get -y install john
DEBIAN_FRONTEND=noninteractive sudo apt-get -y install mariadb-server mariadb-client
DEBIAN_FRONTEND=noninteractive sudo apt-get -y install python3-scipy python3-numpy
DEBIAN_FRONTEND=noninteractive sudo apt-get -y install openssl
DEBIAN_FRONTEND=noninteractive sudo apt-get -y install povray
DEBIAN_FRONTEND=noninteractive sudo apt-get -y install redis-server redis-tools
DEBIAN_FRONTEND=noninteractive sudo apt-get -y install build-essential dpkg-dev \
    rdfind symlinks gperf systemtap-sdt-dev libaudit-dev libcap-dev binutils-for-host \
    g++-multilib libgd-dev
DEBIAN_FRONTEND=noninteractive sudo apt-get -y install sqlite3
DEBIAN_FRONTEND=noninteractive sudo apt-get -y install stockfish
DEBIAN_FRONTEND=noninteractive sudo apt-get -y install stress-ng
DEBIAN_FRONTEND=noninteractive sudo apt-get -y install sysbench
DEBIAN_FRONTEND=noninteractive sudo apt-get -y install bzip2
DEBIAN_FRONTEND=noninteractive sudo apt-get -y install gzip
DEBIAN_FRONTEND=noninteractive sudo apt-get -y install libtiff-tools
DEBIAN_FRONTEND=noninteractive sudo apt-get -y install xz-utils
DEBIAN_FRONTEND=noninteractive sudo apt-get -y install libjpeg-turbo-progs
DEBIAN_FRONTEND=noninteractive sudo apt-get -y install x265


git submodule init
git submodule update --recursive

./pts/phoronix-test-suite list-available-tests
cp -r alltests ~/.phoronix-test-suite/test-suites/local/
cp -r test-profiles/* ~/.phoronix-test-suite/test-profiles/
cp ./config/user-config.xml ~/.phoronix-test-suite/


echo !!!add deb-src to the apt sources!!!
