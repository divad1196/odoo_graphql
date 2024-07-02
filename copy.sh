#!/bin/bash

MODULE="$1"
DEST="$2"
PYCACHES=$(find $MODULE -name __pycache__)

python3 -m compileall -f $MODULE
for pycache in $PYCACHES;
do
    mkdir -p "$DEST/$(dirname $pycache)"
    cp -r $pycache/* "$DEST/$(dirname $pycache)"
done


for pyc in $(find $DEST -name '*cpython-38.pyc');
do
    echo "$pyc" "$(echo $pyc | sed 's/cpython-38.//g')"
    mv "$pyc" "$(echo $pyc | sed 's/cpython-38.//g')"
done


rm "$DEST/__manifest__.pyc"
rm -r "$DEST/tests"
cp "__manifest__.py" "README.md" "COPYRIGHT" "LICENSE" "$DEST"
