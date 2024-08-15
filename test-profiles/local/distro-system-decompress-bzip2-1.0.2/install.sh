#!/bin/bash

BZIP=`which bzip2`
echo $? > ~/install-exit-status

cat > distro-system-decompress-bzip2 << EOT
#!/bin/sh
${BZIP} -dk linux-3.7.tar.bz2 --stdout > /dev/null 2>&1
EOT

chmod +x distro-system-decompress-bzip2
