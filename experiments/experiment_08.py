
import unittest
import setups.kremlingetal_bioreactor as skb

import copy
import numpy

import metrics.ordinary_differential as mod
import models.model_data as mmd
import setups.setup_data as ssd
import setups.setup_data_utils as ssdu
import workflows.protocols as wpr
import workflows.reporting as wr


'''
Splicing at 111000
Covariance trace
'''
class TestExperiment08(unittest.TestCase):


    def do_experiment_setup(self):
        config = copy.deepcopy(ssd.experiment_setup)
        config["algorithm_setup"] = skb.do_algorithm_setup
        config["data_setup"] = skb.do_get_published_data_spliced_111000
        config["model_setup"] = skb.do_model_setup_model_B
        config["problem_setup"] = skb.do_problem_setup_with_covariance_1
        config["protocol_setup"] = skb.do_protocol_setup
        config["protocol_step"]["calib"] = "do"
        config["protocol_step"]["valid"] = "do"
        # TODO: () or not ()?
        config["sensitivity_setup"] = skb.do_sensitivity_setup()
        return config


    def test_protocol_calibration(self):
        config = self.do_experiment_setup()
        actual = wpr.do_calibration_and_compute_performance_measure(config)
        expected = 0.42504827266225675
        self.assertAlmostEquals(actual["objective_function"], expected, 12)
        expected = numpy.array([7.14024687e-05, 5.78668651e+06, 7.86964385e-03, 7.94837482e-01])
        deltas = numpy.array([0.00000001e-05, 0.00000001e+06, 0.00000001e-03, 0.00000001e+01])
        [self.assertAlmostEquals(act, exp, delta=diff) for act, exp, diff in zip(actual["decision_variables"], expected, deltas)]
        

if __name__ == "__main__":
    unittest.main()