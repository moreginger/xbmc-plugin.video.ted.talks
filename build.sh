#!/bin/bash

BUILD=plugin.video.ted.talks
DIST=dist.zip

rm -r $BUILD || true
mkdir $BUILD
# find -type f | grep -v "$BUILD\|$DIST\|build\.sh\|_test\.py\|test_utils\.py\|run_tests\.sh\|\.gitignore\|\.pyc\|\.travis.yml\|\.md\|README\|\.git\|\.pylintrc\|\testSupport\|requirements\.txt" | while read f; do cp "$f" "$BUILD/$f"; done
rsync -aP\
  --exclude "$DIST"\
  --exclude "${BUILD}*"\
  --exclude 'Makefile'\
  --exclude '.git'\
  --exclude '.gitignore'\
  --exclude '.pylintrc'\
  --exclude '.github'\
  --exclude '*.sh'\
  --exclude '*.md'\
  --exclude 'requirements.txt'\
  --exclude 'README'\
  --exclude '*_test.py'\
  --exclude 'test_util.py'\
  --exclude '__init__.py'\
  --exclude '__pycache__'\
  ./ $BUILD/

rm $DIST || true
zip -r $DIST $BUILD
