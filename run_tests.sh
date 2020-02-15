#!/bin/sh
set -e
PYTHONPATH=$PYTHONPATH:$PWD/testSupport python2 -m "unittest" discover -s ./resources/ -p "*_test.py"
