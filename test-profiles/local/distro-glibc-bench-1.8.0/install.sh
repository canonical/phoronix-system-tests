#!/bin/sh
rm -rf glibc-2.39
apt source glibc
cd glibc-2.39
DEB_BUILD_OPTIONS=nocheck dpkg-buildpackage -b --no-sign
cd build-tree/amd64-libc
make bench-build
echo $? > ~/install-exit-status
cd ~
echo "#!/bin/sh
cd glibc-2.39/build-tree/amd64-libc/benchtests
LC_ALL=C ./\$@ > \$LOG_FILE 2>&1
echo \$? > ~/test-exit-status" > glibc-bench
chmod +x glibc-bench
