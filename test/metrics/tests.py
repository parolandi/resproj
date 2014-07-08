
import unittest

import metrics.basic 


class test_metrics(unittest.TestCase):

    def test_sum_absolute_value_residuals(self):
        values = [0, 1, 2, 3, 4, 5, -1, -2, -3, -4, -5]
        self.assertEqual(metrics.basic.sum_absolute_value_residuals(values), 30)
        pass


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(test_metrics)
    unittest.TextTestRunner(verbosity=2).run(suite)