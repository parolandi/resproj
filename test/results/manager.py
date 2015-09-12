import unittest
import results.manager as testme


class TestManager(unittest.TestCase):


    def test_report_nonlinear_confidence_region_intervals_and_points(self):
        intervals = None
        points = None
        testme.report_nonlinear_confidence_region_intervals_and_points(intervals, points)
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()