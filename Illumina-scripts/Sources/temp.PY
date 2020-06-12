# Scenario Hiver
for scen in sorted(carte_diff_dict.keys()):
    result = []
    if scen in scen_hiver:
        for r , radii in enumerate(rayon):
            result.append(sum_circle(carte_diff_dict[scen], radii))

        # Graphique de la reduction selon le rayon
        plt.plot(rayon, result)
        plt.xlabel("Radius (m)")
        plt.ylabel("Reduction intensity (W/m²/sr)")
        plt.legend(("2200k", "2700k", "3000k", "Amber"), loc="upper left")
plt.savefig("/home/jhoule42/Documents/Resultats_Sherbrooke/Diff_watt_rayon/scen_hiver")
plt.close()
