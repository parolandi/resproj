
import unittest
import results.plot_combinatorial as testme

import numpy

import data.generator as dage


class TestPlotCombinatorial(unittest.TestCase):


    def do_get_4x4_data(self):
        center = [  1.58183747e-04,   5.99999935e+06,   3.32956190e-02,   6.29243276e-01]
        ellipsoid = numpy.asmatrix( \
              [[  1.15263027e-06,  -2.05992587e+04,   1.63574438e-04,  -3.81288306e-01], \
               [ -2.05992587e+04,   1.39376409e+18,   1.11852245e+08,  -1.51503797e+12], \
               [  1.63574438e-04,   1.11852245e+08,   8.95632179e+00,  -1.19176214e+04], \
               [ -3.81288306e-01,  -1.51503797e+12,  -1.19176214e+04,   2.57948078e+07]])
        return center, ellipsoid

    
    def test_plot_combinatorial_region_projections(self):
        region = numpy.asarray([dage.normal_distribution(20), dage.normal_distribution(20)]) 
        testme.plot_combinatorial_region_projections(region)


    def test_plot_combinatorial_ellipsoid_projections_subset(self):
        center, ellipsoid = self.do_get_4x4_data()
        rows = 0
        cols = 1
        cntr = [center[rows],center[cols]]
        ell = ellipsoid[numpy.ix_([rows,cols],[rows,cols])]
        testme.plot_combinatorial_ellipsoid_projections(cntr, ell)

    
    def test_plot_combinatorial_ellipsoid_projections(self):
        center, ellipsoid = self.do_get_4x4_data()
        testme.plot_combinatorial_ellipsoid_projections(center, ellipsoid)
        
        
    def test_plot_combinatorial_ellipsoid_projections_2x(self):
        center = [0,1]
        ellipsoid = [[1,0],[0,9]] 
        testme.plot_combinatorial_ellipsoid_projections(center, ellipsoid)
        
    
    def test_plot_combinatorial_ellipsoid_projections_2x_corr(self):
        center = [0,1]
        ellipsoid = [[1,1*3*0.5],[1*3*0.5,9]] 
        testme.plot_combinatorial_ellipsoid_projections(center, ellipsoid)

    
    def test_plot_combinatorial_ellipsoid_projections_3x(self):
        center = [0,1,2]
        ellipsoid = [[1,0,0],[0,4,0],[0,0,9]]
        testme.plot_combinatorial_ellipsoid_projections(center, ellipsoid)


    def test_plot_combinatorial_ellipsoid_projections_3x_corr(self):
        center = [0,1,2]
        ellipsoid = [[1,1*2*0.5,0],[1*2*0.5,4,0],[0,0,9]]
        testme.plot_combinatorial_ellipsoid_projections(center, ellipsoid)


    def test_plot_combinatorial_region_projections_from_file(self):
        region = numpy.loadtxt("C:/workspace/resproj/test/mock/multiplepoints.txt",delimiter=',')
        testme.plot_combinatorial_region_projections(numpy.transpose(region))


if __name__ == "__main__":
    unittest.main()