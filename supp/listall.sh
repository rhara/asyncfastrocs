#!/bin/sh

for f in $(ls asyncfastrocs/*.py | grep -v -e Shape -e __init__) ; do
    echo pretty --py -o $(basename $f).ps $f ;
done
for f in asyncfastrocs/templates/*.html ; do
    echo pretty --lang html -o $(basename $f).ps $f ;
done
