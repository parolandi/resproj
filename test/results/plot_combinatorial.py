
import unittest
import results.plot_combinatorial as testme

import numpy

import data.generator as dage


class TestPlotCombinatorial(unittest.TestCase):


    def test_plot_combinatorial_region_projections(self):
        region = numpy.asarray([dage.normal_distribution(20), dage.normal_distribution(20)]) 
        testme.plot_combinatorial_region_projections(region)


    def test_plot_combinatorial_ellipsoid_projections(self):
        center = [0,0]
        ellipsoid = [[1,2],[2,9]] 
        testme.plot_combinatorial_ellipsoid_projections(center, ellipsoid)


if __name__ == "__main__":
    unittest.main()