
import numpy as np

class Figure00():
    
    def get_ellipsoid(self):
        pass
    
    def get_center(self):
        pass
    
    def get_variances(self):
        ell = self.get_ellipsoid()
        variance = [ell[ii,ii] for ii in range(len(ell))]
        return variance
    
 
class Figure06(Figure00):
    
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


class Figure10(Figure00):
    
    def get_ellipsoid(self):
        cvm = np.asmatrix( \
            [[  1.45525817e-09,  -2.57771994e+02,   1.95891443e-07,  -5.11725634e-06], \
             [ -2.57771994e+02,   3.35190738e+14,  -4.26625019e+05,   3.08864805e+06], \
             [  1.95891443e-07,  -4.26625019e+05,   6.50241863e-04,  -1.85254081e-02], \
             [ -5.11725634e-06,   3.08864805e+06,  -1.85254081e-02,   2.77469343e+00]])
        rad = 12.8806576533
        ell = cvm * rad
        return ell
    
    def get_center(self):
        center = np.asarray([  7.09002587e-05,   6.01415123e+06,   7.70693208e-03,   1.85838333e-01])
        return center


class Figure14(Figure00):
    """
    Corresponds to exp-17
    """
    def get_ellipsoid(self):
        cvm = np.asmatrix( \
            [[  1.46150828e-09,  -2.31549478e+02,   3.10638689e-07,  -3.48685358e-07], \
             [ -2.31549478e+02,   2.17007937e+14,  -4.86225547e+05,   1.12674772e+05], \
             [  3.10638689e-07,  -4.86225547e+05,   3.20927417e-03,  -4.55844395e-03], \
             [ -3.48685358e-07,   1.12674772e+05,  -4.55844395e-03,   9.27583716e-03]])
        rad = 11.8730271717
        ell = cvm * rad
        return ell
    
    def get_center(self):
        center = np.asarray([  7.25907845e-05,   5.90654541e+06,   1.29296870e-02,   1.44696117e-02])
        return center


class Figure18(Figure00):
    """
    Corresponds to exp-18
    """
    def get_ellipsoid(self):
        cvm = np.asmatrix( \
            [[  1.46765734e-09,  -2.34900136e+02,   2.40688171e-07,  -1.57202458e-06], \
             [ -2.34900136e+02,   2.32751745e+14,  -2.99501940e+05,  -6.14244335e+05], \
             [  2.40688171e-07,  -2.99501940e+05,   8.39065671e-04,  -6.12418282e-03], \
             [ -1.57202458e-06,  -6.14244335e+05,  -6.12418282e-03,   1.18886632e-01]])
        rad = 12.0678444163
        ell = cvm * rad
        return ell
    
    def get_center(self):
        center = np.asarray([  7.12884597e-05,   5.77667582e+06,   9.31968630e-03,   4.32751249e-02])
        return center


class Figure22(Figure00):
    """
    Corresponds to exp-19
    """
    def get_ellipsoid(self):
        cvm = np.asmatrix( \
            [[  1.46096638e-09,  -2.38182097e+02,   2.03915684e-07,  -3.05287146e-07], \
             [ -2.38182097e+02,   2.82174146e+14,  -1.32338368e+05,  -1.57971193e+06], \
             [  2.03915684e-07,  -1.32338368e+05,   2.19391111e-03,  -9.06342686e-03], \
             [ -3.05287146e-07,  -1.57971193e+06,  -9.06342686e-03,   5.55553268e-02]])
        rad = 13.1646568318
        ell = cvm * rad
        return ell
    
    def get_center(self):
        center = np.asarray([  7.22076277e-05,   6.00994312e+06,   1.11374646e-02,   2.03026444e-02])
        return center
