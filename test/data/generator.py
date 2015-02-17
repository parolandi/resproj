
import unittest
import data.generator as testme


class TestGenerator(unittest.TestCase):


    def test_calculate_measurement_errors(self):
        cov_matrix_trace = [0.33,2]
        calib_data = [1, 2, 3, 4, 5]
        valid_data = [6, 7, 8, 9, 10]
        actual1, actual2 = testme.calculate_measurement_errors(cov_matrix_trace, calib_data, valid_data)
        self.assertEqual(len(actual1[0]), 5)
        self.assertEqual(len(actual2[1]), 5)
        self.assertAlmostEqual(actual1[0,0], 0.99, 12)
        self.assertAlmostEqual(actual1[0,1], 0.99, 12)
        self.assertAlmostEqual(actual1[1,0], 6, 12)
        self.assertAlmostEqual(actual1[1,1], 6, 12)


if __name__ == "__main__":
    unittest.main()