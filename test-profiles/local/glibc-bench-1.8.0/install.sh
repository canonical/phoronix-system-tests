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
cd glibc-2.39/build-tree/amd64-libc/
CONV_PATH=\$HOME/glibc-2.39/build-tree/amd64-libc/iconvdata LOCPATH=\$HOME/glibc-2.39/build-tree/amd64-libc/localedata LC_ALL=C   \$HOME/glibc-2.39/build-tree/amd64-libc/elf/ld.so --library-path \$HOME/glibc-2.39/build-tree/amd64-libc/:\$HOME/glibc-2.39/build-tree/amd64-libc/math:\$HOME/glibc-2.39/build-tree/amd64-libc/elf:\$HOME/glibc-2.39/build-tree/amd64-libc/dlfcn:\$HOME/glibc-2.39/build-tree/amd64-libc/nss:\$HOME/glibc-2.39/build-tree/amd64-libc/nis:\$HOME/glibc-2.39/build-tree/amd64-libc/rt:\$HOME/glibc-2.39/build-tree/amd64-libc/resolv:\$HOME/glibc-2.39/build-tree/amd64-libc/mathvec:\$HOME/glibc-2.39/build-tree/amd64-libc/support:\$HOME/glibc-2.39/build-tree/amd64-libc/crypt:\$HOME/glibc-2.39/build-tree/amd64-libc/nptl ./\$@ > \$LOG_FILE 2>&1
echo \$? > ~/test-exit-status" > glibc-bench
chmod +x glibc-bench
