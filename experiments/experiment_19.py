
import unittest
import setups.kremlingetal_bioreactor as sekrbi

import logging
import numpy

import common.diagnostics as codi
import workflows.experiments as woex
import workflows.reporting_unlegacy as wore


'''
Kremling bioreactor
Multi-stage experiment 0-60hr interval
Splicing yes15-no5-yes10
Calibration and validation (local)
Nonlinear confidence region
'''
class TestExperiment19(unittest.TestCase):


    def __init__(self, *args, **kwargs):
        super(TestExperiment19, self).__init__(*args, **kwargs)
        self.do_plotting = True
        self.do_quick_tests_only = True
        logging.basicConfig(filename=codi.get_name_logging_file(),level=codi.get_logging_level())
        logging.info("exp-19")
        logging.info(codi.get_date_and_time())

    
    def test_calibration_and_validation(self):
        baseline = dict(woex.calib_valid_baseline)
        basepoint = baseline["calib"]
        basepoint["point"]["objective_function"] = 169.703820093
        basepoint["point"]["decision_variables"] = numpy.array( \
            [  7.22076277e-05, 6.00994312e+06, 1.11374646e-02, 2.03026444e-02])
        basepoint["of_delta"] = 0.000000001
        basepoint["dv_deltas"] = numpy.array( \
            [  0.00000001e-05,  0.00000001e+06,  0.00000001e-02,  0.00000001e-02])
        basepoint = baseline["valid"]
        basepoint["point"]["objective_function"] = 23.517155892719828
        
        experiment = sekrbi.do_experiment_setup_0_60_spliced_yes15no5yes10
        calibrated = woex.test_baseline_calibration_and_validation(experiment, baseline, self)
        if self.do_plotting:
            wore.plot_tiled_calibration_and_validation_trajectories_at_point(experiment(), calibrated)

    
    def test_calibration_and_validation_global(self):
        logging.debug("test_calibration_and_validation_global")
        baseline = dict(woex.calib_valid_baseline)
        basepoint = baseline["calib"]
        #baseline["calib"] = None
        #'''
        basepoint["point"]["objective_function"] = 169.7037979392123
        basepoint["point"]["decision_variables"] = numpy.array( \
            [  7.22075811e-05, 6.01049468e+06, 1.11079090e-02, 2.04245409e-02])
        basepoint["of_delta"] = 0.000000001
        basepoint["dv_deltas"] = numpy.array( \
            [  0.00000001e-05,  0.00000001e+06,  0.00000001e-02,  0.00000001e-02])
        basepoint = baseline["valid"]
        basepoint["point"]["objective_function"] = 23.567425043126253
        basepoint["of_delta"] = 0.000000001
        
        experiment = sekrbi.do_experiment_setup_0_60_spliced_yes15no5yes10_with_global_neldermead_100_10xpm
        calibrated = woex.test_baseline_calibration_and_validation(experiment, baseline, self)
        if self.do_plotting:
            wore.plot_tiled_calibration_and_validation_trajectories_at_point(experiment(), calibrated)


if __name__ == "__main__":
    unittest.main()