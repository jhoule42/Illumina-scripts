# Script makeBATCH
# Auteur : Julien-Pierre Houle
# Note: Il faut être dans le dossier expérience

#!/usr/bin/env bash

for name in Inputs_*
do
    cd $name
    makeBATCH.py .. TM_$name
    cd ..
done
