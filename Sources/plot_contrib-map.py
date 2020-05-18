# Script d'analyse des resulats d'Illumina pour cartes de contribution
# Auteur : Julien-Pierre Houle

# Importer les librairies
import numpy as np
import matplotlib.pyplot as plt
import pytools as pt
import MultiScaleData as MSD
import hdftools as hdf
from glob import glob


# Obtenir dict longueurs d'ondes / objet
path_hdf5 = glob("*.hdf5")
print(path_hdf5)

MSD_dict = {int(s.split('_')[-1].split('.')[0]): MSD.Open(s) for s in path_hdf5}

# Initialiser un objet MSD batard vide
path = "git/Illumina-scripts/Results-Sherbrooke"

carte_total = MSD.Open(path + "/Actu_ete/elevation_angle_90-azimuth_angle_0-wavelength_397.0.hdf5")
for i, layer in enumerate(carte_total):
    carte_total[i][:] = 0 # Partout des zeros

# SPECTRES d'Integration
path_spct = "git/Illumina-scripts/Spectres"
scoto = path_spct + "/scotopic.dat"

liste_spectres = [scoto]
nom_spectres = ['scotopic']

for index3, spct in enumerate(liste_spectres):
        spectre = np.loadtxt(spct, skiprows=1)

        wl, spectre = spectre.T
        interval = (wl>= 380) & (wl <= 730)

        # Split sur 10 parties et fait la moyenne
        moy_wl = [np.mean(x) for x in np.array_split(wl[interval], 10)]
        moy_spectre = [np.mean(x) for x in np.array_split(spectre[interval], 10)]

        for wl in sorted(MSD_dict.keys()):
            for i, layer in enumerate(MSD_dict[wl]):
                #print(layer)
                #print(MSD_dict.keys())
                carte_total[i] += layer * moy_spectre[i] * (moy_wl[1]-moy_wl[0])

        #print(carte_total)
        hdf.plot(carte_total)
