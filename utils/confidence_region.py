
import numpy as np


def regularise_ellipsoid(center, varcov, shift, scale):
    centroid = np.subtract(center, shift)
    
    diag = [np.sqrt(ii) for ii in scale]
    varcovoid = varcov
    for ii in range(len(varcov)):
        for jj in range(len(varcov)):
            varcovoid[ii,jj] = varcov[ii,jj] / diag[ii] / diag[jj]

    return [centroid, varcovoid]


def regularise_ellipsoid_standard(center, varcov):
    shift = center
    scale = [varcov[ii,ii] for ii in range(len(varcov))]
    return regularise_ellipsoid(center, varcov, shift, scale)
