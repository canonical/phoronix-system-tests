#!/bin/bash

cd ~
echo "#!/bin/sh
stockfish bench 4096 \$NUM_CPU_CORES 26 default depth > \$LOG_FILE 2>&1
echo \$? > ~/test-exit-status" > stockfish
chmod +x stockfish

