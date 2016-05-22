
import numpy as np


class Figure06():
    
    def get_ellipsoid(self):
        cvm = np.asmatrix( \
            [[  1.46922103e-09,  -2.56787574e+02,   2.91648344e-07,  -3.02435154e-07], \
             [ -2.56787574e+02,   2.43659568e+14,  -4.44619062e+05,  -5.27153355e+03], \
             [  2.91648344e-07,  -4.44619062e+05,   2.29024568e-03,  -4.02173408e-03], \
             [ -3.02435154e-07,  -5.27153355e+03,  -4.02173408e-03,   1.17063124e-02]])
        rad = 12.8806509967
        ell = cvm * rad
        return ell
    
    def get_center(self):
        center = np.asarray([  7.21144459e-05,   5.92826673e+06,   1.21249611e-02,   1.71735070e-02])
        return center

    def get_variances(self):
        ell = self.get_ellipsoid()
        variance = [ell[ii,ii] for ii in range(len(ell))]
        return variance