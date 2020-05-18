# Script d'extraction des resulats d'Illumina
# Auteur : Julien-Pierre Houle

#!/usr/bin/env bash

for inname in Inputs_*
do
    fname=${inname/Inputs/data}        # bash string manipulation
echo $fname
extract-output-data.py $inname > Results/$fname.txt
done
