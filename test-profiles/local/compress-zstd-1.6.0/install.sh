#!/bin/sh
DEBIAN_FRONTEND=noninteractive sudo apt-get -y install zstd
echo $? > ~/install-exit-status
cd ~
cat > compress-zstd <<EOT
#!/bin/sh
/usr/bin/zstd -T\$NUM_CPU_CORES \$@ silesia.tar > \$LOG_FILE 2>&1
sed -i -e "s/\r/\n/g" \$LOG_FILE 
EOT
chmod +x compress-zstd
