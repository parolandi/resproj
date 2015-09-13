import unittest
import results.manager as testme

import workflows.workflow_data as wowoda

class TestManager(unittest.TestCase):


    def test_report_nonlinear_confidence_region_intervals_and_points(self):
        intervals = []
        points = {}
        points["decision_variables"] = None
        points["objective_function"] = None
        testme.report_nonlinear_confidence_region_intervals_and_points(intervals, points)
        self.assertTrue(True)


    def test_report_system_based_point_results(self):
        data = dict(wowoda.system_based_point_results)
        testme.report_system_based_point_results(data)
        self.assertTrue(True)


    def test_report_sensitivity_based_point_results(self):
        data = dict(wowoda.sensitivity_based_point_results)
        testme.report_sensitivity_based_point_results(data)
        self.assertTrue(True)


    def test_report_decision_variables_and_objective_function(self):
        point = {}
        point["decision_variables"] = [0.0, 1.0]
        point["objective_function"] = 0.0
        testme.report_decision_variables_and_objective_function(point)
        self.assertTrue(True)


    def test_report_date_and_time(self):
        testme.report_date_and_time()
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()