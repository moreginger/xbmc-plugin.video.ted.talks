#!/bin/sh
set -e
python3 -m "unittest" discover -s ./resources/ -p "*_test.py"
