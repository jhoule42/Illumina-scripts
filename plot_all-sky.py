# Script d'analyse des resulats d'Illumina pour cartes du ciel
# Auteur : Julien-Pierre Houle

# Importer les librairies
import numpy as np
import matplotlib.pyplot as plt
import pytools as pt
import MultiScaleData as MSD
import hdftools as hdf

# Elements de la Matrice
m = np.zeros((7, 12, 10))  # Matrice de (el, az, wl)
elevation = [5, 15, 30, 45, 60, 75, 90]
azimuth = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]
wavelength = [397.0, 432.0, 467.0, 502.0, 537.0, 572.0, 607.0, 642.0, 677.0, 712.0]

listes = [elevation, azimuth, wavelength]


# SCÉNARIOS de conversions
S_Actu_Ete = "Documents/Results_Sherbrooke/Results/ete/data.txt"
S_Actu_Hiver = "Documents/Results_Sherbrooke/Results/hiver/data.txt"
S_2200k_Ete = "Documents/Results_alt_scen/Results/2200k_ete/data.txt"
S_2200k_Hiver = "Documents/Results_alt_scen/Results/2200k_hiver/data.txt"
S_2700k_Ete = "Documents/Results_alt_scen/Results/2700k_ete/data.txt"
S_2700k_Hiver =  "Documents/Results_alt_scen/Results/2700k_hiver/data.txt"
S_3000k_Ete = "Documents/Results_alt_scen/Results/3000k_ete/data.txt"
S_3000k_Hiver = "Documents/Results_alt_scen/Results/3000k_hiver/data.txt"
S_Ambree_Ete = "Documents/Results_alt_scen/Results/Ambree_ete/data.txt"
S_Ambree_Hiver = "Documents/Results_alt_scen/Results/Ambree_hiver/data.txt"

liste_scenarios = [S_Actu_Ete, S_Actu_Hiver, S_2200k_Ete, S_2200k_Hiver, S_2700k_Ete, S_2700k_Hiver,
                       S_3000k_Ete, S_3000k_Hiver, S_Ambree_Ete, S_Ambree_Hiver]
nom_scenarios  = ["Actu_Ete", "Actu_Hiver", "2200k_Ete", "2200k_Hiver", "2700k_Ete", "2700k_Hiver",
                      "3000k_Ete", "3000k_Hiver", "Ambree_Ete", "Ambree_Hiver"]

#a = MSD.Open("Documents/Results_Sherbrooke/Results/ete/elevation_angle_90-azimuth_angle_0-wavelength_397.0.hdf5")

# SPECTRES d'Integration
scoto = "scotopic.dat"
#photo = "Documents/Spectres/photopic.dat"

liste_spectres = [scoto]
nom_spectres = ['scotopic']

for index1, scenario in enumerate(liste_scenarios):    # Itérations a travers scénarios
    with open(scenario) as f:
        for line in f:
            line = line.split('-', 2)
            elevation =int(line[0][16:])
            azimuth = int(line[1][14:])
            wavelength = int(line[2][11:14])
            valeur = (line[2][17:])

            # Remplir la matrice
            m[listes[0].index(elevation), listes[1].index(azimuth), listes[2].index(wavelength)] = valeur
            m[-1, :, :] = m[-1, 0, :]  # Lorsqu'on est au zénith


elevation = [5, 15, 30, 45, 60, 75, 90]  # Ouin je triche un peu my bad
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
    sky = (moy_wl[1]-moy_wl[0]) * np.dot(m, moy_spectre)
    carte = (moy_wl[1]-moy_wl[0]) * np.dot(a, moy_spectre)


    # Plot dans la fonction pour la carte du ciel
    pt.plot_allsky(azimuth, elevation, sky,
                   interp="cubic",
                   cmap="gist_earth",
                   autogain=True,
                   clabel = "Sky brightness for %s band [$W/sr/m^2$]" % nom_spectres[index2],
                   showpts=False)
    plt.savefig("%s_cubic.png" % nom_scenarios[index1])
    plt.close()

    pt.plot_allsky(azimuth, elevation, sky,
                   interp="None",
                   cmap="gist_earth",
                   autogain=False,
                   clabel = "Sky brightness for %s band [$W/sr/m^2$]" % nom_spectres[index2],
                   showpts=False)
    plt.savefig("%s_None.png" % nom_scenarios[index1])
    plt.close()

    plt.imshow(a[0])
    plt.imshow(a[0], cmap="inferno")

    plt.ion()   # Idealement ajouter dans le script d'initialisation
    plt.show()
