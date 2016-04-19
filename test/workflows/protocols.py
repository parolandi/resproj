
import unittest
import workflows.protocols as testme
import test.mock.mock as testmetoo

import numpy

import workflows.workflow_data as wowoda


class TestProtools(unittest.TestCase):


    def test_do_basic_workflow_at_solution_point(self):
        config = testmetoo.do_experiment_with_protocol_as_invariant()
        sol_pnt = {}
        sol_pnt["decision_variables"] = numpy.asarray([1.0, 1.0])
        actual = testme.do_basic_workflow_at_solution_point(config, sol_pnt)
        expected = dict(wowoda.system_based_point_results)
        expected["ssr"] = 0.0
        self.assertEquals(actual["ssr"], expected["ssr"])


    def test_do_sensitivity_based_workflow_at_solution_point(self):
        config = testmetoo.do_experiment_with_protocol_and_sensitivities_as_invariant()
        sol_pnt = {}
        sol_pnt["objective_function"] = 0.01
        sol_pnt["decision_variables"] = numpy.asarray([1.0, 1.0])
        actual = testme.do_sensitivity_based_workflow_at_solution_point(config, sol_pnt)
        expected = wowoda.sensitivity_based_point_results
        expected["cov_det"] = 0.01564332730590362
        self.assertAlmostEquals(actual["cov_det"], expected["cov_det"], 1E-8)


if __name__ == "__main__":
    unittest.main()