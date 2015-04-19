
import unittest
import setups.kremlingetal_bioreactor as sekrbi

import logging
import numpy

import common.diagnostics as codi
import results.plot_data as replda
import workflows.experiments as woex
import workflows.reporting as wore


'''
Kremling bioreactor
Multi-stage experiment 0-60hr interval
TODO
'''
class TestExperiment15(unittest.TestCase):


    def __init__(self, *args, **kwargs):
        super(TestExperiment15, self).__init__(*args, **kwargs)
        self.do_plotting = True
        logging.basicConfig(filename=codi.get_name_logging_file(),level=codi.get_logging_level())

    
    def do_experiment_setup(self):
        config = sekrbi.do_experiment_setup_0_60()
        config["algorithm_setup"] = sekrbi.do_algorithm_setup_using_slsqp_with_positivity
        return config

    
    def test_calibration_workflow(self):
        baseline = dict(woex.calib_valid_baseline)
        basepoint = baseline["calib"]
        basepoint["point"]["objective_function"] = 191.9159661
        basepoint["point"]["decision_variables"] = numpy.array( \
            [  7.21144459e-05,  5.92826673e+06,  1.21249611e-02,  1.71735070e-02])
        basepoint["of_delta"] = 0.0000001
        basepoint["dv_deltas"] = numpy.array([  0.00000001e-05,  0.00000001e+06,  0.00000001e-02,  0.00000001e-02])

        calibrated = woex.test_baseline_calibration(sekrbi.do_experiment_setup_0_60, baseline["calib"], self)
        if self.do_plotting:
            wore.plot_tiled_trajectories_at_point(sekrbi.do_experiment_setup_0_60(), calibrated)


    def test_nonlinear_confidence_region(self):
        baseline = {}
        baseline["number_of_points"] = 1
        baseline["intervals"] = [ \
            [4.721085304328252e-05, 0.00014639408975853561], \
            [5999537.6911295187, 10015366.695155494], \
            [0.0030218129834986489, 1.742703135385864], \
            [0.00041379366926754218, 2.0432561489154017]]
        baseline["plotdata"] = dict(replda.plot_data)
        baseline["plotdata"]["window_title"] = "NCR benchmark model (95%)"
        woex.test_calibration_with_nonlinear_confidence_region(self.do_experiment_setup(), baseline, self)


if __name__ == "__main__":
    unittest.main()