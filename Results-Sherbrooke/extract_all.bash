#!/usr/bin/env bash

cd ete
extract-output-data.py ../../Inputs_ete > data.txt 
extract-output-data.py ../../Inputs_ete -p elevation_angle 90 -c > data_zenith.txt
cd ..

cd hiver
extract-output-data.py ../../Inputs_hiver > data.txt
extract-output-data.py ../../Inputs_hiver -p elevation_angle 90 -c > data_zenith.txt
cd ..

