#!/usr/bin/env bash

for dirname in ../*_*/
do
    name=${dirname/..\//}
    mkdir $name
    cd $name
    extract-output-data.py ../../$name > data.txt
    extract-output-data.py ../../$name -p elevation_angle 90 -c > data_zenith.txt
    cd ..
done
