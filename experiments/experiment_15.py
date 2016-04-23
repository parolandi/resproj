import unittest
import setups.kremlingetal_bioreactor as sekrbi
import experiments.baselines as exba

import logging

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
    
    def get_calibration_baseline(self):
        baseline = dict(woex.calib_valid_baseline)
        basepoint = baseline["calib"]
        basepoint = exba.set_baseline_point_0_60(basepoint)
        basepoint = exba.set_baseline_eps_0_60(basepoint) 
        return baseline
    
    def get_calibration_baseline_global(self):
        baseline = dict(woex.calib_valid_baseline)
        basepoint = baseline["calib"]
        basepoint = exba.set_baseline_point_0_60_global(basepoint)
        basepoint = exba.set_baseline_eps_0_60_global(basepoint) 
        return baseline

    
    def test_calibration_workflow(self):
        logging.debug("experiments.experiment_15.test_calibration_workflow")
        experiment = sekrbi.do_experiment_setup_0_60
        baseline = self.get_calibration_baseline()
        calibrated = woex.test_baseline_calibration(experiment, baseline["calib"], self)
        if self.do_plotting:
            wore.plot_tiled_trajectories_at_point(experiment(), calibrated)


    def dn_test_calibration_workflow_local_slsqp(self):
        experiment = sekrbi.do_experiment_setup_0_60_with_slsqp_with_positivity
        basepoint = None
        calibrated = woex.test_baseline_calibration(experiment, basepoint, self)
        self.assertTrue(True)
        if self.do_plotting:
            wore.plot_tiled_trajectories_at_point(experiment(), calibrated)

    
    def dn_test_calibration_workflow_global(self):
        if self.do_quick_tests_only:
            codi.print_and_log_return_on_quick_tests_only()
            return
        experiment = sekrbi.do_experiment_setup_0_60_with_global_neldermead_100_10xpm
        baseline = self.get_calibration_baseline_global()
        calibrated = woex.test_baseline_calibration(experiment, baseline["calib"], self)
        if self.do_plotting:
            wore.plot_tiled_trajectories_at_point(experiment(), calibrated)


if __name__ == "__main__":
    unittest.main()