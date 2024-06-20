#!/bin/sh

DEBIAN_FRONTEND=noninteractive sudo apt-get -y install stress-ng

echo $? > ~/install-exit-status
cd ~
cat << EOF > stress-ng
#!/bin/sh
/usr/bin/stress-ng \$@ > \$LOG_FILE 2>&1
echo \$? > ~/test-exit-status
EOF
chmod +x stress-ng
