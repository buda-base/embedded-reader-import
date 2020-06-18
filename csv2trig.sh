#!/bin/bash

echo -e "update from GH"
git pull

echo -e "\n\nConverting *.csv to *.trig"
for i in input/*.csv; do 
    b=`basename $i`; 
    bnoext=${b%.*}; 
    bfirst=${bnoext% *}; 
    echo "===> Converting $i"
    python3 tsvtordf.py $i > output/$bfirst.trig; 
done
