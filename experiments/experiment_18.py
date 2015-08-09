
import unittest
import setups.kremlingetal_bioreactor as sekrbi

import logging
import numpy

import common.diagnostics as codi
import common.environment as coen
import workflows.experiments as woex
import workflows.reporting_unlegacy as wore


'''
Kremling bioreactor
Multi-stage experiment 0-60hr interval
Splicing yes10-yes15-no5
Calibration
Nonlinear confidence region
'''
class TestExperiment18(unittest.TestCase):


    def __init__(self, *args, **kwargs):
        super(TestExperiment18, self).__init__(*args, **kwargs)
        self.do_plotting = coen.get_doing_plotting()
        self.do_quick_tests_only = coen.get_doing_quick_tests_only()
        logging.basicConfig(filename=codi.get_name_logging_file(),level=codi.get_logging_level())
        logging.info("exp-18: start")
        logging.info(codi.get_date_and_time())


    def __del__(self):
        logging.info("exp-18: finish")
        logging.info(codi.get_date_and_time())

    
    def test_calibration_and_validation(self):
        baseline = dict(woex.calib_valid_baseline)
        basepoint = baseline["calib"]
        basepoint["point"]["objective_function"] = 149.207796219
        basepoint["point"]["decision_variables"] = numpy.array( \
            [  7.12884597e-05, 5.77667582e+06, 9.31968630e-03, 4.32751249e-02])
        basepoint["of_delta"] = 0.000000001
        basepoint["dv_deltas"] = numpy.array( \
            [  0.00000001e-05,  0.00000001e+06,  0.00000001e-03,  0.00000001e-02])
        basepoint = baseline["valid"]
        basepoint["point"]["objective_function"] = 53.5921083595
        
        experiment = sekrbi.do_experiment_setup_0_60_spliced_yes10yes15no5
        calibrated = woex.test_baseline_calibration_and_validation(experiment, baseline, self)
        if self.do_plotting:
            wore.plot_tiled_calibration_and_validation_trajectories_at_point(experiment(), calibrated)

    
    def test_calibration_and_validation_global(self):
        baseline = dict(woex.calib_valid_baseline)
        basepoint = baseline["calib"]
        basepoint["point"]["objective_function"] = 149.20785325292013
        basepoint["point"]["decision_variables"] = numpy.array( \
            [  7.12866349e-05, 5.77559492e+06, 9.31849303e-03, 4.33282246e-02])
        basepoint["of_delta"] = 0.000000001
        basepoint["dv_deltas"] = numpy.array( \
            [  0.00000001e-05,  0.00000001e+06,  0.00000001e-03,  0.00000001e-02])
        basepoint = baseline["valid"]
        basepoint["point"]["objective_function"] = 53.60188061455396
        
        experiment = sekrbi.do_experiment_setup_0_60_spliced_yes10yes15no5_with_global_neldermead_100_10xpm
        calibrated = woex.test_baseline_calibration_and_validation(experiment, baseline, self)
        if self.do_plotting:
            wore.plot_tiled_calibration_and_validation_trajectories_at_point(experiment(), calibrated)

    
if __name__ == "__main__":
    unittest.main()