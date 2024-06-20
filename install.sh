#!/bin/sh
git submodule init
git submodule update --recursive
./pts/phoronix-test-suite list-available-tests
cp -r alltests ~/.phoronix-test-suite/test-suites/local/
cp -r test-profiles/* ~/.phoronix-test-suite/test-profiles/
