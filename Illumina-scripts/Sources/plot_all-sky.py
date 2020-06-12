# Script d'analyse des resulats d'Illumina pour cartes du ciel
# Auteur : Julien-Pierre Houle

# Importer les librairies
import numpy as np
import matplotlib.pyplot as plt
import pytools as pt
import MultiScaleData as MSD
import hdftools as hdf
import os
from math import log10, sqrt


# Elements de la Matrice

m = np.zeros((6, 12, 10))  # Matrice de (el, az, wl)
elevation = [15, 30, 45, 60, 75, 90]
azimuth = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]
wavelength = [397.0, 432.0, 467.0, 502.0, 537.0, 572.0, 607.0, 642.0, 677.0, 712.0]

listes = [elevation, azimuth, wavelength]


dict_SBbg = {"U": 22.03, "B": 22.73, "V": 21.93, "R": 21.18, "I": 20.03, "SQM": 22.0}  # (mag/arcsec^2)
dict_Rbg = {"U": 1.72e-07, "B": 2.05e-07, "V": 2.22e-07, "R": 5.10e-07, "I": 7.65e-07} # (W*sr^-1*m^-2)
dict_R0 = {"U": 111.8, "B": 254.3, "V": 131.4, "R": 151.2, "I": 78.7, "SQM": 270.0}    # (W*sr^-1*m^-2)

# SCÉNARIOS de conversions
path = "git/Illumina-scripts/Results_Sherb_R2"
S_Actu_Ete =  path + "/Actu_ete/data.txt"
S_Actu_Hiver = path + "/Actu_hiver/data.txt"
S_2200k_Ete = path + "/2200k_ete/data.txt"
S_2200k_Hiver = path + "/2200k_hiver/data.txt"
S_2700k_Ete = path + "/2700k_ete/data.txt"
S_2700k_Hiver = path + "/2700k_hiver/data.txt"
S_3000k_Ete = path + "/3000k_ete/data.txt"
S_3000k_Hiver = path + "/3000k_hiver/data.txt"
S_Ambree_Ete = path + "/Ambree_ete/data.txt"
S_Ambree_Hiver = path + "/Ambree_hiver/data.txt"

liste_scenarios1 = [S_Actu_Ete, S_Actu_Hiver]
nom_scenarios1 = ["Actu_ete", "Actu_hiver"]

liste_scenarios2 = [S_2200k_Ete, S_2200k_Hiver, S_2700k_Ete, S_2700k_Hiver,
                    S_3000k_Ete, S_3000k_Hiver, S_Ambree_Ete, S_Ambree_Hiver]
nom_scenarios2  = ["2200k_Ete", "2200k_Hiver", "2700k_Ete", "2700k_Hiver",
                   "3000k_Ete", "3000k_Hiver", "Ambree_Ete", "Ambree_Hiver"]
carte_sky_dict = {}
path = "git/Illumina-scripts/Results_Sherb_R2"

# SPECTRES d'Integration
path_spct = "git/Illumina-scripts/Spectres"
scoto = path_spct + "/scotopic.dat"
sqm = path_spct + "/sqm.dat"


liste_spectres = [sqm]
nom_spectres = ['SQM']

print("\n-------------------------------------------")
for index1, scenario in enumerate(liste_scenarios1):    # Itérations a travers scénarios
    with open(scenario) as f:
        for line in f:
            line = line.split('-', 2)
            elevation = int(line[0][16:])
            azimuth = int(line[1][14:])
            wavelength = int(line[2][11:14])
            valeur = (line[2][17:])
            #print("{}".format(line))

            # Remplir la matrice
            if elevation != 0:
                m[listes[0].index(elevation), listes[1].index(azimuth), listes[2].index(wavelength)] = valeur
                m[-1, :, :] = m[-1, 0, :]  # Lorsqu'on est au zénith


    elevation = [15, 30, 45, 60, 75, 90]  # Ouin je triche un peu my bad
    azimuth = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]

    # Intégration sur les spectres
    for index2, spct in enumerate(liste_spectres):
        spectre = np.loadtxt(spct, skiprows=1)
        wl, spectre = spectre.T
        interval = (wl >= 380) & (wl <= 730)

        # Split sur 10 parties et fait la moyenne
        moy_wl = [np.mean(x) for x in np.array_split(wl[interval], 10)]
        moy_spectre = [np.mean(x) for x in np.array_split(spectre[interval], 10)]

        # Afficher wl moyenner sur la courbe
        #plt.plot(wl[interval], spectre[interval])
        #plt.plot(moy_wl, moy_scoto,'ko')

        # Intégration sur les longueurs d'ondes
        print("\n",str(index1+1) + ". Integration de " + str(nom_scenarios1[index1]) + " sur " + str(nom_spectres[index2]))
        sky = (moy_wl[1]-moy_wl[0]) * np.dot(m, moy_spectre)

        # Caster dans dict + Somme
        carte_sky_dict.update({(nom_scenarios1[index1]): sky.copy()})
        total_carte2 = np.sum([np.sum(layer) for layer in carte_sky_dict[nom_scenarios1[index1]]])
        print("\tTotal Sky: ", total_carte2)

        # Plot dans la fonction pour la carte du ciel
        pt.plot_allsky(azimuth, elevation, sky,
                       interp="None",
                       cmap="inferno",
                       autogain=False,
                       clabel = "Sky brightness for %s band [$W/sr/m^2$]" % nom_spectres[index2],
                       showpts=False,
                       log=True,
                       vmin = 3e-6,
                       vmax = 1e-7)
        plt.savefig("/home/jhoule42/Documents/Resultats_Sherb_R2/Carte_Ciel/Ra/%s_log_none.png" % nom_scenarios1[index1], bbox_inches="tight")
        plt.close()

        # plt.imshow(a[0])
        # plt.imshow(a[0], cmap="inferno")

        # Print ZENITHS
        print("\tZenith : ", sky[-1][0])


elevation = [15, 30, 45, 60, 75, 90]  # Ouin je triche un peu my bad
azimuth = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]


# Convertir SKY BRIGHTNESS
print("\n-------------------------------------------")
for index1, scenario in enumerate(liste_scenarios1):    # Itérations a travers scénarios

    SB = []
    SB_sky = []
    print("Conversion to SB: ", nom_scenarios1[index1])

    # Convertir la brillance en magnitude
    for layer in carte_sky_dict[nom_scenarios1[index1]]:
        for valeur in layer:
            Rbg = dict_R0["SQM"] * (10 ** (-0.4*dict_SBbg["SQM"]))
            SB.append(-2.5*log10((valeur + Rbg)/dict_R0["SQM"]))

    # Split la liste en listes de listes pour plot_allsky
    nbr_elem_list = 12
    SB_sky = [SB[i:i + nbr_elem_list] for i in range(0, len(SB), nbr_elem_list)]
    print("\tZenith : ", SB_sky[-1][0])

    # APPLIQUER UN DELTA
    # for x, valeur in enumerate(SB_sky):
    #     SB[x] -= delta_mesure[index4]

    # Plot dans la fonction pour la carte du ciel
    pt.plot_allsky(azimuth, elevation, SB_sky,
                   interp="None",
                   cmap="inferno",
                   autogain=False,
                   clabel = "Sky brightness for %s band [$mag/arcsec^2$]" % nom_spectres[index2],
                   showpts=False)
    plt.savefig("/home/jhoule42/Documents/Resultats_Sherb_R2/Carte_Ciel/SB/%s_SB.png" % nom_scenarios1[index1], bbox_inches="tight")
    plt.close()

    plt.ion()   # Idealement ajouter dans le script d'initialisation
    plt.show()

print("-------------------------------------------")
print("Execution complete!")
