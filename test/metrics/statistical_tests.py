
import unittest

import metrics.statistical_tests


class TestStatisticalTest(unittest.TestCase):


    def test_one_sided_chi_squared_test(self):
        # chi2 = 82.358
        actual = metrics.statistical_tests.calculate_one_sided_chi_squared_test_for_mean_sum_squared_residuals(82.0, 100, 0.90)
        self.assertTrue(actual)
        actual = metrics.statistical_tests.calculate_one_sided_chi_squared_test_for_mean_sum_squared_residuals(83.0, 100, 0.90)
        self.assertFalse(actual)


    def test_two_sided_chi_squared_test(self):
        # chi2 = 77.929, 124.342
        actual = metrics.statistical_tests.calculate_two_sided_chi_squared_test_for_mean_sum_squared_residuals(77.928, 100, 0.90)
        self.assertFalse(actual)
        actual = metrics.statistical_tests.calculate_two_sided_chi_squared_test_for_mean_sum_squared_residuals(77.930, 100, 0.90)
        self.assertTrue(actual)
        actual = metrics.statistical_tests.calculate_two_sided_chi_squared_test_for_mean_sum_squared_residuals(124.341, 100, 0.90)
        self.assertTrue(actual)
        actual = metrics.statistical_tests.calculate_two_sided_chi_squared_test_for_mean_sum_squared_residuals(124.343, 100, 0.90)
        self.assertFalse(actual)
        
        
    def test_two_sided_t_student_test(self):
        # @ dof=100
        t_cutoff = 1.6602343261
        t_offset = 0.01
        actual = metrics.statistical_tests.calculate_two_sided_t_student_test_for_parameter_estimates(t_cutoff - t_offset, 1, 100, 0.90)
        self.assertFalse(actual)
        actual = metrics.statistical_tests.calculate_two_sided_t_student_test_for_parameter_estimates(t_cutoff + t_offset, 1, 100, 0.90)
        self.assertTrue(actual)


if __name__ == "__main__":
    unittest.main()
