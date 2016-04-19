
import unittest
import numpy

import metrics.algebraic_legacy


class TestAlgebraicLegacyMetrics(unittest.TestCase):

    def test_sum_absolute_value_residuals(self):
        values = [0, 1, 2, 3, 4, 5, -1, -2, -3, -4, -5]
        self.assertEqual(metrics.algebraic_legacy.sum_absolute_value_residuals(values), 30)

    
    def test_sum_squared_residuals(self):
        values = [1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
        def linear(p, x):
            return x
        self.assertEqual(40, metrics.algebraic_legacy.sum_squared_residuals([1.0], values, linear, numpy.ones(len(values))))


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAlgebraicLegacyMetrics)
    unittest.TextTestRunner(verbosity=2).run(suite)
