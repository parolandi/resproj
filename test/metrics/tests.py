
import unittest

import numpy

import metrics.basic 

class test_metrics(unittest.TestCase):

    def test_sum_absolute_value_residuals(self):
        values = [0, 1, 2, 3, 4, 5, -1, -2, -3, -4, -5]
        self.assertEqual(metrics.basic.sum_absolute_value_residuals(values), 30)
        return
    
    def test_sum_squared_residuals(self):
        values = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        def linear(p, x):
            return x
        self.assertEqual(0, metrics.basic.sum_squared_residuals([1.0], values, linear, numpy.ones(len(values))))
        return


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(test_metrics)
    unittest.TextTestRunner(verbosity=2).run(suite)