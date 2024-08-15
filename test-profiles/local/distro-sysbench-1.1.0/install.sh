#!/bin/sh
cd ~/

echo "#!/bin/sh
cd sysbench-1.0.20
/usr/bin/sysbench --threads=\$NUM_CPU_CORES --time=90 \$@ > \$LOG_FILE 2>&1
echo \$? > ~/test-exit-status" > sysbench
chmod +x sysbench
