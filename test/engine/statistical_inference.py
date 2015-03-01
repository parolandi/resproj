
import unittest
import engine.statistical_inference as tst

import math
import numpy.matlib


# TODO: add more tests
class TestStatisticalInference(unittest.TestCase):


    def test_compute_confidence_ellipsoid_radius(self):
        actual = tst.compute_confidence_ellipsoid_radius(2, 3, 0.5, 0.90)
        expected = 24.75
        self.assertAlmostEquals(actual, expected, 6)


    def test_compute_confidence_intervals(self):
        covariance_matrix = numpy.matlib.eye(2) * 2
        t_value = 2.0
        actual = tst.compute_confidence_intervals(covariance_matrix, t_value)
        exp = 2*math.sqrt(2.0)
        expected = numpy.asarray([exp, exp])
        [self.assertAlmostEquals(act, exp, 6) for act, exp in zip(actual, expected)]


if __name__ == "__main__":
    unittest.main()
