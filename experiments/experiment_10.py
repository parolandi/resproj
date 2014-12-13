
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
import experiments.experiments as ee

'''
Splicing at 000111
Covariance trace
'''
class TestExperiment10(unittest.TestCase):


    def __init__(self, *args, **kwargs):
        super(TestExperiment10, self).__init__(*args, **kwargs)
        self.do_plotting = False

    
    def do_experiment_setup(self):
        config = copy.deepcopy(ssd.experiment_setup)
        config["algorithm_setup"] = skb.do_algorithm_setup
        config["data_setup"] = skb.do_get_published_data_spliced_000111
        config["model_setup"] = skb.do_model_setup_model_B
        config["problem_setup"] = skb.do_problem_setup_with_covariance_1
        config["protocol_setup"] = skb.do_protocol_setup
        config["protocol_step"]["calib"] = "do"
        config["protocol_step"]["valid"] = "do"
        # TODO: () or not ()?
        config["sensitivity_setup"] = skb.do_sensitivity_setup()
        return config


    def test_protocol_calibration(self):
        baseline = dict(we.baseline)
        baseline["point"]["objective_function"] = 16.706323980668913
        baseline["point"]["decision_variables"] = numpy.array([7.01131196e-05, 6.36106401e+06, 1.71515507e-02, 9.79422021e-03])
        baseline["of_delta"] = 0.000000000000001
        baseline["dv_deltas"] = numpy.array([0.00000001e-05, 0.00000001e+06, 0.00000001e-02, 0.00000001e-03])
        ee.test_baseline_calibration(self.do_experiment_setup, baseline, self)

    
    def donot_test_protocol_calibration_validation(self):
        config = self.do_experiment_setup()
        # do calibration
        calibrated = wpr.do_calibration_and_compute_performance_measure(config)
        print(calibrated)
        actual = calibrated["objective_function"]
        expected = 16.706323980668913 # 0.013033454937278158
        #self.assertAlmostEquals(actual, expected, 12)
        actual = calibrated["decision_variables"]
        _ = numpy.array([6.94673782e-05, 6.89584538e+06, 6.28171859e-03, 1.80509631e+00])
        optpe = [7.01131196e-05, 6.36106401e+06, 1.71515507e-02, 9.79422021e-03]
        expected = optpe
        deltas = numpy.array([0.00000001e-05, 0.00000001e+06, 0.00000001e-03, 0.00000001e+00])
        #[self.assertAlmostEquals(act, exp, delta=diff) for act, exp, diff in zip(actual, expected, deltas)]
        # do workflow
        _ = wpr.do_basic_workflow_at_solution_point(config, calibrated)
        # do validation
        ssdu.set_next_protocol_step(config)
        validated = wpr.do_validation_and_compute_performance_measure_at_solution_point(config, calibrated)
        print(validated)
        actual = validated["decision_variables"]
        expected = optpe
        #[self.assertAlmostEquals(act, exp, delta=diff) for act, exp, diff in zip(actual, expected, deltas)]
        actual = validated["objective_function"]
        expected = 0.624555117615724 # 0.02449032032693814
        #self.assertAlmostEquals(actual, expected, 12)
        # do workflow
        _ = wpr.do_basic_workflow_at_solution_point(config, calibrated)
        if self.do_plotting:
            wr.plot_tiled_calibration_and_validation_trajectories_at_point(config, calibrated)


if __name__ == "__main__":
    unittest.main()