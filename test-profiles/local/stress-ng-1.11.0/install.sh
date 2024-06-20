#!/bin/sh

cd ~
cat << EOF > stress-ng
#!/bin/sh
/usr/bin/stress-ng \$@ > \$LOG_FILE 2>&1
echo \$? > ~/test-exit-status
EOF
chmod +x stress-ng
