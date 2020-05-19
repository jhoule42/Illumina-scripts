# Script pour creer des fausse villes VIIRS
# Auteur : Julien-Pierre Houle


import MultiScaleData as MSD
from hdftools import from_domain

a = from_domain(“domain.ini”)
a.set_circle((0, 0), 50000, 1)
a.save(“test1”)



import MultiScaleData as MSD
from hdftools import from_domain

for radius in [0.250, 1, 5, 10, 20, 30, 40, 50]:
    for distance in [1, 5, 10, 20, 30, 40, 60, 80, 100, 150, 200, 250, 300, 400]:
    a = from_domain(“domain.ini”)
    a.set_circle((0, distance/R), radius, 50)    R = rayon équatorial terre (6 371 km)
    a.save(“stable_lights”)


subprocess.run(“~/hg/illumina/oiseaux/make_inputs.py”)
    os.rename(“Inputs”, “Inputs_%s_%s” % (radius, distance))
