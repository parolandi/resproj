
import unittest
import setups.kremlingetal_bioreactor as skb

import copy
import numpy

import setups.setup_data as ssd
import workflows.experiments as we
import workflows.reporting as wr


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


    def test_protocol_calibration_and_validation(self):
        baseline = dict(we.calib_valid_baseline)
        basepoint = baseline["calib"]
        basepoint["point"]["objective_function"] = 0.30431429868139315
        basepoint["point"]["decision_variables"] = numpy.array([6.91450307e-05, 6.15859949e+06, 9.28550465e-03, 5.71289053e-02])
        basepoint["of_delta"] = 0.00000000000000001
        basepoint["dv_deltas"] = numpy.array([0.00000001e-05, 0.00000001e+06, 0.00000001e-03, 0.00000001e-02])
        basepoint = baseline["valid"]
        basepoint["point"]["objective_function"] = 0.5163698707350677
        calibrated = we.test_baseline_calibration_and_validation(self.do_experiment_setup, baseline, self)
        if self.do_plotting:
            wr.plot_tiled_calibration_and_validation_trajectories_at_point(self.do_experiment_setup(), calibrated)


if __name__ == "__main__":
    unittest.main()