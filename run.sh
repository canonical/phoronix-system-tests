#!/bin/sh

host=`hostname`
export TEST_RESULTS_IDENTIFIER=$host-id
export TEST_RESULTS_NAME=$host--name
export TEST_RESULTS_DESCRIPTION="${host} result"

# Don't let the device overheat and throttle
export WATCHDOG_SENSOR=cpu.temp,gpu.temp,sys.temp,hdd.temp
export WATCHDOG_SENSOR_THRESHOLD=85
# If it's not returning to lower temps, continue after this many min
export WATCHDOG_MAXIMUM_WAIT=3
export NO_FILE_HASH_CHECKS=1
SCRIPT_DIR=$(dirname "$0")
PTS_BIN=$SCRIPT_DIR/pts/phoronix-test-suite

DISPLAY=:0 NO_FILE_HASH_CHECKS=1 PTS_SILENT_MODE=1 $PTS_BIN strict-benchmark $1
