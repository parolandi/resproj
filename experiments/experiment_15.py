
import unittest
import setups.kremlingetal_bioreactor as sekrbi

import logging
import numpy

import common.diagnostics as codi
import workflows.experiments as woex
import workflows.reporting as wore


'''
Kremling bioreactor
Multi-stage experiment 0-60hr interval
No splicing
Calibration
Nonlinear confidence region
'''
class TestExperiment15(unittest.TestCase):


    def __init__(self, *args, **kwargs):
        super(TestExperiment15, self).__init__(*args, **kwargs)
        self.do_plotting = False
        self.do_quick_tests_only = True
        logging.basicConfig(filename=codi.get_name_logging_file(),level=codi.get_logging_level())
        logging.info("exp-15")
        logging.info(codi.get_date_and_time())

    
    def test_calibration_workflow(self):
        baseline = dict(woex.calib_valid_baseline)
        basepoint = baseline["calib"]
        basepoint["point"]["objective_function"] = 191.9159661
        basepoint["point"]["decision_variables"] = numpy.array( \
            [  7.21144459e-05,  5.92826673e+06,  1.21249611e-02,  1.71735070e-02])
        basepoint["of_delta"] = 0.0000001
        basepoint["dv_deltas"] = numpy.array( \
            [  0.00000001e-05,  0.00000001e+06,  0.00000001e-02,  0.00000001e-02])

        experiment = sekrbi.do_experiment_setup_0_60
        calibrated = woex.test_baseline_calibration(experiment, basepoint, self)
        if self.do_plotting:
            wore.plot_tiled_trajectories_at_point(experiment(), calibrated)


if __name__ == "__main__":
    unittest.main()