#!/bin/bash

BUILD=build
DIST=dist.zip

rm -r $BUILD || true
mkdir $BUILD
find -type f | grep -v "$BUILD\|$DIST\|build\.sh\|_test\.py\|test_utils\.py\|run_tests\.sh\|\.gitignore\|\.pyc\|\.travis.yml\|\.md\|README\|\.git\|\.pylintrc\|\testSupport\|requirements\.txt" | while read f; do cp $f $BUILD; done

rm $DIST || true
zip -r $DIST $BUILD
