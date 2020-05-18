#!/usr/bin/env bash

for fname in ../*_*/
do
    exp_name=$(cut -d'/' -f2 <<< $fname)
    echo $exp_name
    mkdir $exp_name
    cd $exp_name
    extract-output-data.py ../$fname > data.txt &
    extract-output-data.py ../$fname -c -p elevation_angle 90 > data_zenith.txt &
    cd ..
done
