# Script pour Integration sur le rayon
# Auteur : Julien-Pierre Houle

def sum_circle(ds, radii):
    total = np.zeros_like(radii)
    for i in range(len(ds)):
        ny,nx = ds[i].shape
        Y0, X0 = (ny-1)/2, (nx-1)/2
        R = radii / ds.pixel_size(i)
        Y, X = np.ogrid[:ny,:nx]
        d2 = (X-X0)**2 + (Y-Y0)**2
        total += np.sum(ds[i][d2 <= R**2]) # A verifier
    return total
