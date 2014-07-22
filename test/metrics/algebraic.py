
import unittest

import numpy

import metrics.algebraic

def linear_mock(x, t, p, u):
    return p[0] * u[0]


class TestAlgebraicMetrics(unittest.TestCase):

    def test_sum_absolute_value_residuals(self):
        values = [0, 1, 2, 3, 4, 5, -1, -2, -3, -4, -5]
        self.assertEqual(metrics.algebraic.sum_absolute_value_residuals(values), 30)

    
    def test_sum_squared_residuals(self):
        values = [1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
        def linear(p, x):
            return x
        self.assertEqual(40, metrics.algebraic.sum_squared_residuals([1.0], values, linear, numpy.ones(len(values))))


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAlgebraicMetrics)
    unittest.TextTestRunner(verbosity=2).run(suite)