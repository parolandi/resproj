
import unittest
import setups.kremlingetal_bioreactor as skb

import logging
import numpy

import common.diagnostics as codi
import common.environment as coen
import workflows.experiments as we
import workflows.reporting as wr


'''
Kremling bioreactor
Calibration and validation
Splicing at 000111 and 111111
Covariance trace
0-20hr interval
'''
class TestExperiment10(unittest.TestCase):


    def __init__(self, *args, **kwargs):
        super(TestExperiment10, self).__init__(*args, **kwargs)
        self.do_plotting = coen.get_doing_plotting()
        logging.basicConfig(filename=codi.get_name_logging_file(),level=codi.get_logging_level())
        logging.info("exp-10: start")
        logging.info(codi.get_date_and_time())


    def __del__(self):
        logging.info("exp-10: finish")
        logging.info(codi.get_date_and_time())

    
    def do_experiment_setup_1(self):
        config = skb.do_experiment_setup_0_20()
        config["data_setup"] = skb.do_get_published_data_spliced_000111
        config["problem_setup"] = skb.do_problem_setup_with_covariance_1
        config["protocol_step"]["valid"] = "do"
        return config

    
    def do_experiment_setup_2(self):
        config = skb.do_experiment_setup_0_20()
        config["algorithm_setup"] = skb.do_algorithm_setup_using_slsqp_with_positivity
        config["data_setup"] = skb.do_get_published_data_spliced_111111
        config["problem_setup"] = skb.do_problem_setup_with_covariance_2
        return config


    def test_protocol_calibration_and_validation_setup_1(self):
        baseline = dict(we.calib_valid_baseline)
        basepoint = baseline["calib"]
        basepoint["point"]["objective_function"] = 0.30431429868139315
        basepoint["point"]["decision_variables"] = numpy.array( \
            [6.91450307e-05, 6.15859949e+06, 9.28550465e-03, 5.71289053e-02])
        basepoint["of_delta"] = 0.00000000000000001
        basepoint["dv_deltas"] = numpy.array([0.00000001e-05, 0.00000001e+06, 0.00000001e-03, 0.00000001e-02])
        basepoint = baseline["valid"]
        basepoint["point"]["objective_function"] = 0.5163698707350677
        calibrated = we.test_baseline_calibration_and_validation(self.do_experiment_setup_1, baseline, self)
        if self.do_plotting:
            wr.plot_tiled_calibration_and_validation_trajectories_at_point(self.do_experiment_setup_1(), calibrated)


    # TODO: not a very good fit!
    def test_protocol_calibration_setup_2(self):
        baseline = dict(we.calib_valid_baseline)
        basepoint = baseline["calib"]
        basepoint["point"]["objective_function"] = 10424.524182305697
        basepoint["point"]["decision_variables"] = numpy.array( \
            [1.58183747e-04, 5.99999935e+06, 3.32956190e-02, 6.29243276e-01])
        basepoint["of_delta"] = 0.000000000001
        basepoint["dv_deltas"] = numpy.array([0.00000001e-04, 0.00000001e+06, 0.00000001e-02, 0.00000001e-01])
        calibrated = we.test_baseline_calibration(self.do_experiment_setup_2, baseline["calib"], self)
        if self.do_plotting:
            wr.plot_tiled_trajectories_at_point(self.do_experiment_setup_2(), calibrated)


if __name__ == "__main__":
    unittest.main()