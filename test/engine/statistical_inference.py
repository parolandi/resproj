
import unittest
import engine.statistical_inference as tst

import math
import numpy.matlib


# TODO: add more tests
class TestStatisticalInference(unittest.TestCase):


    def test_compute_measurements_standard_deviation(self):
        actual = tst.compute_measurements_variance(10, 1, 11)
        expected = 10 / (11 - 1)
        self.assertAlmostEquals(actual, expected, 12)

    
    def test_compute_confidence_ellipsoid_radius(self):
        actual = tst.compute_confidence_ellipsoid_radius(2, 3, 0.5, 0.90)
        expected = 0.5 * 2 * 49.5
        self.assertAlmostEquals(actual, expected, 12)


    def test_compute_confidence_intervals(self):
        covariance_matrix = numpy.matlib.eye(2) * 2
        t_value = 2.0
        actual = tst.compute_confidence_intervals(covariance_matrix, t_value)
        exp = 2*math.sqrt(2.0)
        expected = numpy.asarray([exp, exp])
        [self.assertAlmostEquals(act, exp, 6) for act, exp in zip(actual, expected)]


    def test_compute_one_sided_f_value(self):
        f_value = tst.compute_one_sided_f_value(0.99, 9, 1)
        self.assertAlmostEquals(11.259, f_value, 3)


if __name__ == "__main__":
    unittest.main()
