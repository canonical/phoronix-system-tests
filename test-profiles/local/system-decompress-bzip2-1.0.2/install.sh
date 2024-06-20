#!/bin/bash



DEBIAN_FRONTEND=noninteractive sudo apt-get -y install bzip2
BZIP=`which bzip2`
echo $? > ~/install-exit-status

cat > system-decompress-bzip2 << EOT
#!/bin/sh
${BZIP} -dk linux-3.7.tar.bz2 --stdout > /dev/null 2>&1
EOT

chmod +x system-decompress-bzip2
