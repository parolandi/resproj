
import unittest
import engine.statistical_inference as tst

import numpy.matlib


# TODO: add more tests
class TestStatisticalInference(unittest.TestCase):


    def test_compute_confidence_ellipsoid_radius(self):
        actual = tst.compute_confidence_ellipsoid_radius(2, 3, 0.5, 0.90)
        expected = 24.75
        print(actual)
        self.assertAlmostEquals(actual, expected, 6)


    def test_compute_confidence_intervals(self):
        covariance_matrix = numpy.matlib.eye(2)
        ellipsoid_radius = 1.0
        actual = tst.compute_confidence_intervals(covariance_matrix, ellipsoid_radius)
        expected = numpy.asarray([1.0, 1.0])
        [self.assertAlmostEquals(act, exp, 6) for act, exp in zip(actual, expected)]
        

if __name__ == "__main__":
    unittest.main()
