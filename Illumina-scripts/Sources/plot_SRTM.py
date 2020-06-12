# Script pour plot le STRM
# Auteur : Julien-Pierre Houle

import numpy as np
import matplotlib.pyplot as plt
import MultiScaleData as MSD
import hdftools as hdf


srtm = MSD.Open("git/Illumina-scripts/srtm.hdf5")
hdf.plot(srtm, cmap="gist_earth", vmax = 450)
#plt.clim()
plt.colorbar(label = "Elevetion (m)")
plt.axis("off")
