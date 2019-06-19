#!/bin/bash

DIST=dist.zip
rm $DIST || true
find -type f | grep -v 'build\.sh\|_test\.py\|test_utils\.py\|run_tests\.sh\|\.gitignore\|\.pyc\|\.travis.yml\|\.md\|README\|\.git\|\.pylintrc\|\testSupport\|requirements\.txt' | zip -@ $DIST 