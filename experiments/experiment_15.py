
import unittest
import setups.kremlingetal_bioreactor as sekrbi
import experiments.baselines as exba

import logging
import numpy

import common.diagnostics as codi
import common.environment as coen
import workflows.experiments as woex
import workflows.reporting as wore


'''
Kremling bioreactor
Multi-stage experiment 0-60hr interval
No splicing
Calibration (local, global)
See also: exp-20
'''
class TestExperiment15(unittest.TestCase):


    def __init__(self, *args, **kwargs):
        super(TestExperiment15, self).__init__(*args, **kwargs)
        self.do_plotting = coen.get_doing_plotting()
        self.do_quick_tests_only = coen.get_doing_quick_tests_only()
        logging.basicConfig(filename=codi.get_name_logging_file(),level=codi.get_logging_level())
        logging.info("exp-15: start")
        logging.info(codi.get_date_and_time())


    def __del__(self):
        logging.info("exp-15: finish")
        logging.info(codi.get_date_and_time())

    
    def test_calibration_workflow(self):
        baseline = dict(woex.calib_valid_baseline)
        basepoint = baseline["calib"]
        basepoint = exba.set_baseline_point_0_60(basepoint)
        basepoint = exba.set_baseline_eps_0_60(basepoint) 
        experiment = sekrbi.do_experiment_setup_0_60
        calibrated = woex.test_baseline_calibration(experiment, basepoint, self)
        if self.do_plotting:
            wore.plot_tiled_trajectories_at_point(experiment(), calibrated)


    def test_calibration_workflow_local_slsqp(self):
        baseline = dict(woex.calib_valid_baseline)
        basepoint = baseline["calib"]
        basepoint = None
        experiment = sekrbi.do_experiment_setup_0_60_with_slsqp_with_positivity
        calibrated = woex.test_baseline_calibration(experiment, basepoint, self)
        self.assertTrue(True)
        if self.do_plotting:
            wore.plot_tiled_trajectories_at_point(experiment(), calibrated)

    
    def test_calibration_workflow_global(self):
        if self.do_quick_tests_only:
            return
        baseline = dict(woex.calib_valid_baseline)
        basepoint = baseline["calib"]
        basepoint["point"]["objective_function"] = 191.915901669
        basepoint["point"]["decision_variables"] = numpy.array( \
            [  7.21063052228e-05, 5928238.02405, 0.0121129261722, 0.0172159895438])
        basepoint["of_delta"] = 0.000000001
        basepoint["dv_deltas"] = numpy.array( \
            [  0.00000001e-05,  0.00000001e+06,  0.00000001e-02,  0.00000001e-02])

        experiment = sekrbi.do_experiment_setup_0_60_with_global_neldermead_100_10xpm
        calibrated = woex.test_baseline_calibration(experiment, basepoint, self)
        if self.do_plotting:
            wore.plot_tiled_trajectories_at_point(experiment(), calibrated)


if __name__ == "__main__":
    unittest.main()