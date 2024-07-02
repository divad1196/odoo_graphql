#!/bin/bash

MODULE="$1"
PYCACHES=$(find $MODULE -name __pycache__)

python3 -m compileall -f $MODULE

rm $(find -type f -name '*.py' ! -name '__manifest__.py')

for pycache in $PYCACHES;
do
    mv $pycache/* "$(dirname $pycache)"
    rmdir $pycache
done


for pyc in $(find $MODULE -name '*cpython*.pyc');
do
    NEW_NAME="$(echo $pyc | sed 's/cpython.*\.//g')"
    echo "$pyc -> $NEW_NAME"
    mv "$pyc" $NEW_NAME
done


rm "$MODULE/__manifest__.pyc" "$MODULE/copy.sh" "$MODULE/make_compile.sh"
rm -r "$MODULE/tests"
