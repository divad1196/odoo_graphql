#!/bin/bash

MODULE="$1"
DEST="$2"
PYCACHES=$(find odoo_graphql -name __pycache__)

python3 -m compileall -f $MODULE
for pycache in $PYCACHES;
do
    mkdir -p "$DEST/$(dirname $pycache)" && cp -r $pycache "$DEST/$pycache"
done
